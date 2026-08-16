import time
from flask import current_app
from app.extensions import db

START_TIME = time.time()

def collect_health():
    checks = {}
    checks["flask"] = {"status": "healthy", "label": "Flask Application"}

    try:
        db.connection().execute("SELECT 1")
        checks["database"] = {"status": "healthy", "label": "Database"}
    except Exception as exc:
        current_app.logger.exception("Database health check failed: %s", exc)
        checks["database"] = {"status": "unhealthy", "label": "Database"}

    from app.services.docker_service import docker_available
    checks["docker"] = {"status": "healthy" if docker_available() else "unavailable", "label": "Docker"}

    from app.services.github_service import github_configured
    checks["github"] = {"status": "healthy" if github_configured() else "not_configured", "label": "GitHub Actions"}

    statuses = [v["status"] for v in checks.values()]
    overall = "healthy" if all(s == "healthy" or s in {"unavailable", "not_configured"} for s in statuses) else "degraded"

    return {
        "status": overall,
        "service": "DockFlow",
        "version": current_app.config["APP_VERSION"],
        "environment": current_app.config["APP_ENV"],
        "uptime_seconds": int(time.time() - START_TIME),
        "checks": checks,
        "timestamp": time.time(),
    }
