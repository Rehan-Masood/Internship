def docker_client():
    """
    Create and return a Docker SDK client.

    Returns:
        DockerClient | None
    """
    try:
        import docker

        client = docker.from_env()
        client.ping()
        return client
    except Exception:
        return None


def docker_available():
    """
    Check whether Docker is available and accessible.
    """
    client = docker_client()

    if not client:
        return False

    try:
        client.ping()
        return True
    except Exception:
        return False


def list_containers():
    """
    Return all Docker containers with useful monitoring information.
    """
    client = docker_client()

    if not client:
        return {
            "available": False,
            "reason": "Docker SDK/socket unavailable",
            "items": [],
        }

    try:
        items = []

        for c in client.containers.list(all=True):
            attrs = c.attrs

            state = attrs.get("State", {}) or {}
            health_data = state.get("Health", {}) or {}

            ports = attrs.get("NetworkSettings", {}).get("Ports") or {}

            items.append({
                "id": c.short_id,
                "name": c.name,
                "image": (
                    attrs.get("Config", {}).get("Image")
                    or ""
                ),
                "status": c.status,
                "health": health_data.get(
                    "Status",
                    "not_reported"
                ),
                "ports": list(ports.keys()),
                "created": attrs.get("Created"),
            })

        return {
            "available": True,
            "items": items,
        }

    except Exception as exc:
        return {
            "available": False,
            "reason": str(exc),
            "items": [],
        }


def get_container(container_name):
    """
    Get a specific Docker container by name or ID.
    """
    client = docker_client()

    if not client:
        return None

    try:
        return client.containers.get(container_name)
    except Exception:
        return None


def stop_container(container_name):
    """
    Stop a running container.
    """
    container = get_container(container_name)

    if not container:
        return {
            "ok": False,
            "message": f"Container '{container_name}' was not found.",
        }

    try:
        container.stop()

        return {
            "ok": True,
            "message": f"Container '{container_name}' stopped successfully.",
        }

    except Exception as exc:
        return {
            "ok": False,
            "message": str(exc),
        }


def remove_container(container_name):
    """
    Remove a Docker container.
    """
    container = get_container(container_name)

    if not container:
        return {
            "ok": False,
            "message": f"Container '{container_name}' was not found.",
        }

    try:
        container.remove(force=True)

        return {
            "ok": True,
            "message": f"Container '{container_name}' removed successfully.",
        }

    except Exception as exc:
        return {
            "ok": False,
            "message": str(exc),
        }


def container_logs(container_name, tail=100):
    """
    Return logs from a Docker container.
    """
    container = get_container(container_name)

    if not container:
        return {
            "ok": False,
            "message": f"Container '{container_name}' was not found.",
            "logs": "",
        }

    try:
        logs = container.logs(
            tail=tail,
            timestamps=True,
        ).decode("utf-8", errors="replace")

        return {
            "ok": True,
            "message": "Container logs retrieved successfully.",
            "logs": logs,
        }

    except Exception as exc:
        return {
            "ok": False,
            "message": str(exc),
            "logs": "",
        }