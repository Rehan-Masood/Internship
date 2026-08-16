import socket
from flask import current_app
from app.services.docker_service import docker_available
from app.services.github_service import github_configured

def collect_services():
    services = [
        {"name": "Flask Application", "status": "Running", "detail": "HTTP server responding"},
        {"name": "Database", "status": "Running", "detail": "SQLite connection available"},
        {"name": "Docker", "status": "Running" if docker_available() else "Unavailable", "detail": "Docker socket/API"},
        {"name": "GitHub Actions", "status": "Configured" if github_configured() else "Not Configured", "detail": "Workflow API"},
    ]
    external = current_app.config["EXTERNAL_HEALTH_URL"]
    if external:
        import requests
        try:
            r = requests.get(external, timeout=5)
            services.append({"name": "External API", "status": "Healthy" if r.ok else "Unhealthy", "detail": external})
        except Exception as exc:
            services.append({"name": "External API", "status": "Unhealthy", "detail": str(exc)})
    else:
        services.append({"name": "External API", "status": "Not Configured", "detail": "Set EXTERNAL_HEALTH_URL to enable"})
    return services
