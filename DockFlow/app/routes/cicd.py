from flask import Blueprint, render_template, request, jsonify
from app.services.github_service import get_ci_status, trigger_workflow
cicd_bp = Blueprint("cicd", __name__, url_prefix="/cicd")

@cicd_bp.get("/")
def index():
    return render_template("cicd.html", page="CI/CD Pipeline")

@cicd_bp.post("/trigger")
def trigger():
    result = trigger_workflow()
    return jsonify(result), (200 if result.get("ok") else 400)
