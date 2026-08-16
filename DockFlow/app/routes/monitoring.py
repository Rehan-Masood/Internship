from flask import Blueprint, render_template
monitoring_bp = Blueprint("monitoring", __name__, url_prefix="/monitoring")
@monitoring_bp.get("/")
def index():
    return render_template("monitoring.html", page="Monitoring")
