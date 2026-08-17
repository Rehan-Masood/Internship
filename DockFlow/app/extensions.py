import logging
import sqlite3
import time
from pathlib import Path
from flask import current_app, g, request


class Database:
    def init_app(self, app):
        app.teardown_appcontext(self.close)
        app.before_request(self.request_started)
        app.after_request(self.request_finished)

    def connection(self):
        if "db" not in g:
            path = Path(current_app.config["DB_PATH"])
            path.parent.mkdir(parents=True, exist_ok=True)
            g.db = sqlite3.connect(path, timeout=10)
            g.db.row_factory = sqlite3.Row
        return g.db

    def close(self, _error=None):
        conn = g.pop("db", None)
        if conn is not None:
            conn.close()

    def ensure_schema(self):
        conn = self.connection()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS deployments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commit_hash TEXT NOT NULL,
                branch TEXT NOT NULL,
                status TEXT NOT NULL,
                environment TEXT NOT NULL,
                deployed_at TEXT,
                duration_seconds INTEGER DEFAULT 0,
                message TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                title TEXT NOT NULL,
                detail TEXT DEFAULT '',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS request_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at REAL NOT NULL,
                duration_ms REAL NOT NULL,
                status_code INTEGER NOT NULL,
                path TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS app_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                level TEXT NOT NULL,
                service TEXT NOT NULL,
                message TEXT NOT NULL
            );
            """
        )
        conn.commit()

    def query(self, sql, params=()):
        return [dict(row) for row in self.connection().execute(sql, params).fetchall()]

    def execute(self, sql, params=()):
        cur = self.connection().execute(sql, params)
        self.connection().commit()
        return cur.lastrowid

    def request_started(self):
        g.request_started = time.perf_counter()

    def request_finished(self, response):
        started = getattr(g, "request_started", None)
        if started is None or request.path.startswith("/static"):
            return response

        duration = (time.perf_counter() - started) * 1000
        try:
            self.execute(
                "INSERT INTO request_metrics(created_at,duration_ms,status_code,path) VALUES(?,?,?,?)",
                (time.time(), duration, response.status_code, request.path),
            )
        except Exception:
            # Metrics must never break a normal HTTP response.
            pass

        # Create a useful application log entry for every non-static request.
        # The DBLogHandler below also records explicit app.logger messages.
        try:
            level = "ERROR" if response.status_code >= 500 else "WARNING" if response.status_code >= 400 else "INFO"
            self.execute(
                "INSERT INTO app_logs(created_at,level,service,message) VALUES(datetime('now'),?,?,?)",
                (
                    level,
                    "HTTP",
                    f"{request.method} {request.path} -> {response.status_code} ({duration:.2f} ms)",
                ),
            )
        except Exception:
            pass

        return response


db = Database()


class DBLogHandler(logging.Handler):
    """Persist Flask/Python log records in DockFlow's app_logs table."""

    def emit(self, record):
        try:
            message = self.format(record)
            level = record.levelname.upper()
            service = record.name or "DockFlow"
            db.execute(
                "INSERT INTO app_logs(created_at,level,service,message) VALUES(datetime('now'),?,?,?)",
                (level, service, message),
            )
        except Exception:
            # Logging must never crash the application.
            pass


def init_logging(app):
    log_path = Path(app.config["LOG_PATH"])
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # File logs: useful for Docker volume /app/logs and docker exec inspection.
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Database logs: used by the DockFlow Logs page.
    db_handler = DBLogHandler()
    db_handler.setFormatter(formatter)
    db_handler.setLevel(logging.INFO)

    app.logger.handlers.clear()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(db_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = False

    # Also capture useful Werkzeug request logs without depending on the
    # built-in development server.
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
