from flask import Blueprint, jsonify, current_app, request

from app.extensions import db

from app.services.metrics_service import collect_metrics
from app.services.docker_service import list_containers
from app.services.github_service import get_ci_status
from app.services.health_service import collect_health
from app.services.monitoring_service import collect_system
from app.services.service_health import collect_services


api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api",
)


# =========================================================
# Dashboard
# =========================================================

@api_bp.get("/dashboard")
def dashboard():

    # -----------------------------------------------------
    # Date range
    # -----------------------------------------------------

    days = request.args.get(
        "days",
        30,
        type=int,
    )

    # Only allow the dashboard ranges that the UI supports.
    if days not in (7, 30, 90):
        days = 30

    metrics = collect_metrics(days=days)

    deployments = db.query(
        "SELECT * FROM deployments "
        "ORDER BY id DESC LIMIT 8"
    )

    activities = db.query(
        "SELECT * FROM activities "
        "ORDER BY id DESC LIMIT 8"
    )

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

            "poll": current_app.config[
                "METRICS_POLL_SECONDS"
            ],

            "deployment_provider":
                current_app.config[
                    "DEPLOYMENT_PROVIDER"
                ],

            "deployment_webhook_configured":
                bool(
                    current_app.config[
                        "DEPLOYMENT_WEBHOOK_URL"
                    ].strip()
                ),

            "metrics_days": days,
        },
    })


# =========================================================
# Notifications
# =========================================================

@api_bp.get("/notifications")
def notifications():

    """
    Return recent DockFlow activities for the
    notification bell.

    Deployment events are already recorded in the
    activities table by deployment_service.py.
    """

    rows = db.query(
        """
        SELECT
            id,
            kind,
            title,
            detail,
            created_at
        FROM activities
        ORDER BY id DESC
        LIMIT 15
        """
    )

    return jsonify({
        "notifications": rows,
        "count": len(rows),
    })


# =========================================================
# Health
# =========================================================

@api_bp.get("/health")
def health_api():
    return jsonify(
        collect_health()
    )


# =========================================================
# Metrics
# =========================================================

@api_bp.get("/metrics")
def metrics():

    days = request.args.get(
        "days",
        30,
        type=int,
    )

    if days not in (7, 30, 90):
        days = 30

    return jsonify(
        collect_metrics(days=days)
    )


# =========================================================
# Containers
# =========================================================

@api_bp.get("/containers")
def containers():
    return jsonify({
        "containers": list_containers()
    })


# =========================================================
# CI/CD
# =========================================================

@api_bp.get("/ci-status")
def ci_status():
    return jsonify(
        get_ci_status()
    )


# =========================================================
# Deployments
# =========================================================

@api_bp.get("/deployments")
def deployments():

    return jsonify({
        "deployments": db.query(
            """
            SELECT *
            FROM deployments
            ORDER BY id DESC
            LIMIT 50
            """
        )
    })


# =========================================================
# Logs
# =========================================================

@api_bp.get("/logs")
def logs():

    limit = min(
        max(
            request.args.get(
                "limit",
                100,
                type=int,
            ),
            1,
        ),
        500,
    )

    rows = db.query(
        """
        SELECT
            id,
            created_at,
            level,
            service,
            message
        FROM app_logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    return jsonify({
        "logs": rows,
        "count": len(rows),
    })


# =========================================================
# Monitoring
# =========================================================

@api_bp.get("/monitoring")
def monitoring():
    return jsonify(
        collect_system()
    )


# =========================================================
# Services
# =========================================================

@api_bp.get("/services")
def services():

    return jsonify({
        "services": collect_services()
    })