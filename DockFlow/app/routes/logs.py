from flask import Blueprint, jsonify, render_template, request
from app.extensions import db

logs_bp = Blueprint("logs", __name__, url_prefix="/logs")


@logs_bp.get("/")
def index():
    return render_template("logs.html", page="Logs")


@logs_bp.get("/data")
def data():
    """Return recent application logs for the Logs page."""
    try:
        limit = min(max(request.args.get("limit", 100, type=int), 1), 500)
        rows = db.query(
            """
            SELECT id, created_at, level, service, message
            FROM app_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return jsonify({"logs": rows, "count": len(rows)})
    except Exception as exc:
        return jsonify({"logs": [], "count": 0, "error": str(exc)}), 500
