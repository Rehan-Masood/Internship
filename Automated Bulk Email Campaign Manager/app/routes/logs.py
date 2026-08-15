from flask import Blueprint, render_template, request
from app import db
from app.models import EmailLog

logs_bp = Blueprint("logs", __name__)

@logs_bp.get("/")
def index():
    status = request.args.get("status")
    query = EmailLog.query.order_by(EmailLog.created_at.desc())
    if status:
        query = query.filter_by(status=status)
    logs = query.limit(500).all()
    return render_template("logs.html", logs=logs)
