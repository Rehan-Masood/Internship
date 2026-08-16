from flask import Blueprint, render_template
logs_bp = Blueprint("logs", __name__, url_prefix="/logs")
@logs_bp.get("/")
def index():
    return render_template("logs.html", page="Logs")
