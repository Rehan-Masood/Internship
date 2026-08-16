import datetime as dt
import requests
from flask import current_app
from app.extensions import db

def deploy_now(payload):
    provider = current_app.config["DEPLOYMENT_PROVIDER"].strip().lower()
    webhook = current_app.config["DEPLOYMENT_WEBHOOK_URL"].strip()

    if not provider and not webhook:
        return {"ok": False, "message": "Deployment provider is not configured. No deployment was started."}

    if webhook:
        try:
            r = requests.post(webhook, json=payload or {}, timeout=10)
            if r.ok:
                commit = (payload.get("commit") or "manual")[:40]
                branch = payload.get("branch") or "main"
                env = payload.get("environment") or "Production"
                db.execute(
                    "INSERT INTO deployments(commit_hash,branch,status,environment,deployed_at,message) VALUES(?,?,?,?,?,?)",
                    (commit, branch, "TRIGGERED", env, dt.datetime.now(dt.timezone.utc).isoformat(), "Deployment webhook accepted")
                )
                db.execute(
                    "INSERT INTO activities(kind,title,detail,created_at) VALUES(?,?,?,datetime('now'))",
                    ("deployment", "Deployment triggered", f"{provider or 'Webhook'} accepted the request")
                )
                return {"ok": True, "message": "Deployment trigger accepted by the configured webhook."}
            return {"ok": False, "message": f"Deployment provider returned HTTP {r.status_code}."}
        except Exception as exc:
            return {"ok": False, "message": str(exc)}

    return {"ok": False, "message": f"Provider '{provider}' is named but no deployment integration is configured."}
