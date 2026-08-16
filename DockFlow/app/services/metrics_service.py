import time
from app.extensions import db

def collect_metrics():
    now = time.time()
    since = now - 30 * 24 * 3600
    rows = db.query(
        "SELECT duration_ms,status_code,created_at FROM request_metrics WHERE created_at >= ?",
        (since,)
    )
    total = len(rows)
    errors = sum(1 for r in rows if r["status_code"] >= 400)
    avg = round(sum(r["duration_ms"] for r in rows) / total, 1) if total else 0
    deployments = db.query("SELECT COUNT(*) AS c FROM deployments")[0]["c"]
    failed_builds = db.query(
        "SELECT COUNT(*) AS c FROM deployments WHERE status IN ('FAILED','CANCELLED')"
    )[0]["c"]

    # Real bucketed history from stored request data; empty buckets remain zero.
    buckets = []
    for i in range(12, 0, -1):
        start = now - i * 30 * 24 * 3600 / 12
        end = now - (i - 1) * 30 * 24 * 3600 / 12
        bucket_rows = [r for r in rows if start <= r["created_at"] < end]
        buckets.append({
            "label": time.strftime("%b %d", time.localtime(end)),
            "requests": len(bucket_rows),
            "errors": sum(1 for r in bucket_rows if r["status_code"] >= 400)
        })

    return {
        "total_requests": total,
        "avg_response_ms": avg,
        "error_count": errors,
        "deployments": deployments,
        "failed_builds": failed_builds,
        "success_rate": round(((total - errors) / total) * 100, 2) if total else 100,
        "history": buckets,
    }
