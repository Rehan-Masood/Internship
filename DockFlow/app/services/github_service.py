import requests
from flask import current_app

def github_configured():
    c = current_app.config
    return bool(c["GITHUB_TOKEN"] and c["GITHUB_OWNER"] and c["GITHUB_REPO"])

def headers():
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {current_app.config['GITHUB_TOKEN']}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

def get_ci_status():
    if not github_configured():
        return {"available": False, "status": "not_configured", "message": "GitHub Actions integration not configured."}
    c = current_app.config
    url = f"https://api.github.com/repos/{c['GITHUB_OWNER']}/{c['GITHUB_REPO']}/actions/runs"
    try:
        r = requests.get(url, headers=headers(), params={"per_page": 10}, timeout=8)
        r.raise_for_status()
        runs = []
        for x in r.json().get("workflow_runs", []):
            runs.append({
                "id": x["id"],
                "name": x.get("name"),
                "status": x.get("status"),
                "conclusion": x.get("conclusion"),
                "branch": x.get("head_branch"),
                "sha": x.get("head_sha", "")[:7],
                "created_at": x.get("created_at"),
                "updated_at": x.get("updated_at"),
                "html_url": x.get("html_url"),
            })
        return {"available": True, "status": "healthy", "runs": runs}
    except Exception as exc:
        return {"available": False, "status": "error", "message": str(exc)}

def trigger_workflow():
    if not github_configured():
        return {"ok": False, "message": "GitHub Actions integration not configured."}
    c = current_app.config
    url = (
        f"https://api.github.com/repos/{c['GITHUB_OWNER']}/"
        f"{c['GITHUB_REPO']}/actions/workflows/{c['GITHUB_WORKFLOW']}/dispatches"
    )
    try:
        r = requests.post(
            url, headers=headers(),
            json={"ref": c["GITHUB_REF"]},
            timeout=8
        )
        if r.status_code == 204:
            return {"ok": True, "message": "Workflow dispatch accepted by GitHub Actions."}
        return {"ok": False, "message": f"GitHub returned HTTP {r.status_code}: {r.text[:200]}"}
    except Exception as exc:
        return {"ok": False, "message": str(exc)}
