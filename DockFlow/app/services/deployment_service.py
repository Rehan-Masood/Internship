# Deployment Service — Docker Local Deployment

import datetime as dt

from flask import current_app

from app.extensions import db
from app.services.docker_service import docker_client, get_container


# ---------------------------------------------------------
# Deployment database helpers
# ---------------------------------------------------------

def _record_deployment(
    commit,
    branch,
    status,
    environment,
    message,
):
    """
    Save a deployment record and activity entry.

    IMPORTANT:
    These records belong to the main DockFlow application
    database. The deployed release container does not use
    this database.
    """

    db.execute(
        """
        INSERT INTO deployments(
            commit_hash,
            branch,
            status,
            environment,
            deployed_at,
            message
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            commit,
            branch,
            status,
            environment,
            dt.datetime.now(dt.timezone.utc).isoformat(),
            message,
        ),
    )

    db.execute(
        """
        INSERT INTO activities(
            kind,
            title,
            detail,
            created_at
        )
        VALUES (?, ?, ?, datetime('now'))
        """,
        (
            "deployment",
            "Deployment triggered",
            message,
        ),
    )


# ---------------------------------------------------------
# Docker deployment
# ---------------------------------------------------------

def _docker_deployment(payload):
    """
    Perform a local Docker deployment.

    DockFlow itself runs in the protected container:

        dockflow

    Deploy Now creates/replaces only:

        dockflow-release

    The release application is exposed on:

        http://localhost:5001

    The main DockFlow application remains available on:

        http://localhost:5000

    The main DockFlow database remains the source of truth
    for deployment history.
    """

    client = docker_client()

    if not client:
        return {
            "ok": False,
            "message": (
                "Docker is unavailable. Make sure Docker Desktop "
                "is running and DockFlow has access to the Docker socket."
            ),
        }

    # -----------------------------------------------------
    # Deployment configuration
    # -----------------------------------------------------

    container_name = "dockflow-release"

    image_name = (
        payload.get("image")
        or "dockflow-dockflow:latest"
    )

    host_port = int(
        payload.get("port")
        or 5001
    )

    container_port = 5000

    commit = (
        payload.get("commit")
        or "manual"
    )[:40]

    branch = (
        payload.get("branch")
        or "main"
    )

    environment = (
        payload.get("environment")
        or "Production"
    )

    # -----------------------------------------------------
    # Safety protection
    # -----------------------------------------------------

    protected_names = {
        "dockflow",
        "dockflow-dockflow",
        "dockflow_app",
        "dockflow-app",
    }

    if container_name in protected_names:
        return {
            "ok": False,
            "message": (
                "Deployment target is protected. "
                "DockFlow cannot deploy over its own container."
            ),
        }

    # Never allow Deploy Now to use the main DockFlow port.
    if host_port == 5000:
        return {
            "ok": False,
            "message": (
                "Port 5000 is reserved for the main DockFlow "
                "application. Use port 5001 for the release."
            ),
        }

    # -----------------------------------------------------
    # Check image
    # -----------------------------------------------------

    try:
        client.images.get(image_name)

    except Exception:
        return {
            "ok": False,
            "message": (
                f"Docker image '{image_name}' was not found. "
                "Build the DockFlow image first with "
                "'docker compose build'."
            ),
        }

    # -----------------------------------------------------
    # Remove previous release container only
    # -----------------------------------------------------

    existing = get_container(container_name)

    if existing:

        try:
            existing.reload()

            existing_status = existing.status

            if existing_status == "running":
                existing.stop(timeout=10)

            existing.remove(force=True)

        except Exception as exc:

            return {
                "ok": False,
                "message": (
                    "Could not replace the previous deployment "
                    f"container: {exc}"
                ),
            }

    # -----------------------------------------------------
    # Start new release container
    # -----------------------------------------------------

    try:

        container = client.containers.run(
            image=image_name,

            name=container_name,

            # Main DockFlow:
            #     localhost:5000
            #
            # Release:
            #     localhost:5001
            ports={
                f"{container_port}/tcp": host_port
            },

            environment={
                "FLASK_ENV": "production",
                "APP_ENV": "Production",
                "APP_VERSION": (
                    current_app.config.get(
                        "APP_VERSION",
                        "1.0.0",
                    )
                ),

                # Clearly identify this container as a
                # deployed release.
                "DOCKFLOW_RELEASE": "true",
                "DOCKFLOW_DEPLOYMENT_BRANCH": branch,
                "DOCKFLOW_DEPLOYMENT_COMMIT": commit,
                "DOCKFLOW_DEPLOYMENT_ENVIRONMENT": environment,
            },

            # Docker SDK access is preserved for the deployed
            # application, exactly as in your existing setup.
            volumes={
                "/var/run/docker.sock": {
                    "bind": "/var/run/docker.sock",
                    "mode": "rw",
                }
            },

            restart_policy={
                "Name": "unless-stopped",
            },

            detach=True,
        )

    except Exception as exc:

        error_message = (
            f"Docker deployment failed: {exc}"
        )

        try:

            _record_deployment(
                commit=commit,
                branch=branch,
                status="FAILED",
                environment=environment,
                message=error_message,
            )

        except Exception:
            pass

        return {
            "ok": False,
            "message": error_message,
            "provider": "docker",
        }

    # -----------------------------------------------------
    # Record successful deployment
    # -----------------------------------------------------

    release_url = (
        f"http://localhost:{host_port}"
    )

    message = (
        "Docker deployment completed successfully. "
        f"Release container '{container_name}' is running "
        f"on port {host_port}."
    )

    try:

        _record_deployment(
            commit=commit,
            branch=branch,
            status="DEPLOYED",
            environment=environment,
            message=message,
        )

    except Exception:
        # The actual Docker deployment succeeded even if
        # database recording fails.
        pass

    # -----------------------------------------------------
    # Return complete deployment information
    # -----------------------------------------------------

    return {
        "ok": True,

        "message": message,

        "provider": "docker",

        "container": container_name,

        "image": image_name,

        "container_id": container.short_id,

        "port": host_port,

        "environment": environment,

        "branch": branch,

        "commit": commit,

        "url": release_url,

        "deployment": {
            "status": "DEPLOYED",
            "container": container_name,
            "url": release_url,
            "port": host_port,
            "branch": branch,
            "commit": commit,
            "environment": environment,
        },
    }


# ---------------------------------------------------------
# Main deployment entry point
# ---------------------------------------------------------

def deploy_now(payload):
    """
    Main deployment entry point.

    Currently supported provider:

        docker
    """

    payload = payload or {}

    provider = (
        current_app.config.get(
            "DEPLOYMENT_PROVIDER",
            "",
        )
        or ""
    ).strip().lower()

    # -----------------------------------------------------
    # No provider configured
    # -----------------------------------------------------

    if not provider:

        return {
            "ok": False,
            "message": (
                "Deployment provider is not configured."
            ),
        }

    # -----------------------------------------------------
    # Docker provider
    # -----------------------------------------------------

    if provider == "docker":

        return _docker_deployment(payload)

    # -----------------------------------------------------
    # Unsupported provider
    # -----------------------------------------------------

    return {
        "ok": False,
        "message": (
            f"Provider '{provider}' is not supported "
            "by the current local deployment integration."
        ),
    }

