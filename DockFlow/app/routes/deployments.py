from flask import Blueprint, render_template, jsonify, request
from app.extensions import db
from app.services.deployment_service import deploy_now
deployments_bp = Blueprint("deployments", __name__, url_prefix="/deployments")

@deployments_bp.get("/")
def index():
    return render_template("deployments.html", page="Deployments")

@deployments_bp.post("/deploy")
def deploy():
    result = deploy_now(request.get_json(silent=True) or {})
    return jsonify(result), (200 if result.get("ok") else 400)
