from flask import Blueprint, jsonify, current_app
from app.services.health_service import collect_health
health_bp = Blueprint("health", __name__)

@health_bp.get("/health")
def health():
    result = collect_health()
    code = 200 if result["status"] == "healthy" else 503
    return jsonify(result), code
