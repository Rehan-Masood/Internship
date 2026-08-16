def docker_client():
    try:
        import docker
        return docker.from_env()
    except Exception:
        return None

def docker_available():
    client = docker_client()
    if not client:
        return False
    try:
        client.ping()
        return True
    except Exception:
        return False

def list_containers():
    client = docker_client()
    if not client:
        return {"available": False, "reason": "Docker SDK/socket unavailable", "items": []}
    try:
        items = []
        for c in client.containers.list(all=True):
            attrs = c.attrs
            items.append({
                "id": c.short_id,
                "name": c.name,
                "image": (attrs.get("Config", {}).get("Image") or ""),
                "status": c.status,
                "health": (attrs.get("State", {}).get("Health", {}) or {}).get("Status", "not_reported"),
                "ports": list((attrs.get("NetworkSettings", {}).get("Ports") or {}).keys()),
                "created": attrs.get("Created"),
            })
        return {"available": True, "items": items}
    except Exception as exc:
        return {"available": False, "reason": str(exc), "items": []}
