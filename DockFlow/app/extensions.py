import json
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
        conn.executescript("""
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
        """)
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
        if started is not None and not request.path.startswith("/static"):
            duration = (time.perf_counter() - started) * 1000
            try:
                self.execute(
                    "INSERT INTO request_metrics(created_at,duration_ms,status_code,path) VALUES(?,?,?,?)",
                    (time.time(), duration, response.status_code, request.path),
                )
            except Exception:
                pass
        return response

db = Database()

def init_logging(app):
    log_path = Path(app.config["LOG_PATH"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    original_log = app.logger.info
    def log_info(message, *args, **kwargs):
        try:
            db.execute(
                "INSERT INTO app_logs(created_at,level,service,message) VALUES(datetime('now'),?,?,?)",
                ("INFO", "DockFlow", message % args if args else message),
            )
        except Exception:
            pass
        return original_log(message, *args, **kwargs)
    app.logger.info = log_info
