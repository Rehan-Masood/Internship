from flask import Blueprint, jsonify, current_app
from app.extensions import db
from app.services.metrics_service import collect_metrics
from app.services.docker_service import list_containers
from app.services.github_service import get_ci_status
from app.services.health_service import collect_health
from app.services.monitoring_service import collect_system
from app.services.service_health import collect_services

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.get("/dashboard")
def dashboard():
    metrics = collect_metrics()
    deployments = db.query("SELECT * FROM deployments ORDER BY id DESC LIMIT 8")
    activities = db.query("SELECT * FROM activities ORDER BY id DESC LIMIT 8")
    return jsonify({
        "metrics": metrics,
        "deployments": deployments,
        "activities": activities,
        "health": collect_health(),
        "containers": list_containers(),
        "ci": get_ci_status(),
        "services": collect_services(),
        "system": collect_system(),
        "config": {
            "version": current_app.config["APP_VERSION"],
            "environment": current_app.config["APP_ENV"],
            "poll": current_app.config["METRICS_POLL_SECONDS"],
        }
    })

@api_bp.get("/health")
def health_api():
    return jsonify(collect_health())

@api_bp.get("/metrics")
def metrics():
    return jsonify(collect_metrics())

@api_bp.get("/containers")
def containers():
    return jsonify({"containers": list_containers()})

@api_bp.get("/ci-status")
def ci_status():
    return jsonify(get_ci_status())

@api_bp.get("/deployments")
def deployments():
    return jsonify({"deployments": db.query("SELECT * FROM deployments ORDER BY id DESC LIMIT 50")})

@api_bp.get("/logs")
def logs():
    rows = db.query("SELECT * FROM app_logs ORDER BY id DESC LIMIT 100")
    return jsonify({"logs": rows})

@api_bp.get("/monitoring")
def monitoring():
    return jsonify(collect_system())

@api_bp.get("/services")
def services():
    return jsonify({"services": collect_services()})
