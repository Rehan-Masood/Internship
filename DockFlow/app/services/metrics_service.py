import time

from app.extensions import db


# =========================================================
# Metrics Collection
# =========================================================

def collect_metrics(days=30):
    """
    Collect dashboard metrics for the requested period.

    Supported dashboard periods:

        7 days
        30 days
        90 days

    The frontend sends the selected period to:

        /api/dashboard?days=7
        /api/dashboard?days=30
        /api/dashboard?days=90
    """

    # -----------------------------------------------------
    # Validate period
    # -----------------------------------------------------

    try:
        days = int(days)
    except (TypeError, ValueError):
        days = 30

    if days not in (7, 30, 90):
        days = 30

    # -----------------------------------------------------
    # Time window
    # -----------------------------------------------------

    now = time.time()

    since = now - (
        days * 24 * 60 * 60
    )

    # -----------------------------------------------------
    # Request metrics
    # -----------------------------------------------------

    rows = db.query(
        """
        SELECT
            duration_ms,
            status_code,
            created_at
        FROM request_metrics
        WHERE created_at >= ?
        """,
        (since,),
    )

    total = len(rows)

    errors = sum(
        1
        for r in rows
        if int(r["status_code"] or 0) >= 400
    )

    avg = (
        round(
            sum(
                float(r["duration_ms"] or 0)
                for r in rows
            ) / total,
            1,
        )
        if total
        else 0
    )

    # -----------------------------------------------------
    # Deployment statistics
    #
    # Keep deployment totals based on the deployment
    # history, just like the existing dashboard.
    # -----------------------------------------------------

    deployments = db.query(
        """
        SELECT COUNT(*) AS c
        FROM deployments
        """
    )[0]["c"]

    failed_builds = db.query(
        """
        SELECT COUNT(*) AS c
        FROM deployments
        WHERE status IN ('FAILED', 'CANCELLED')
        """
    )[0]["c"]

    # -----------------------------------------------------
    # Success rate
    # -----------------------------------------------------

    success_rate = (
        round(
            (
                (total - errors)
                / total
            ) * 100,
            2,
        )
        if total
        else 100
    )

    # -----------------------------------------------------
    # Bucketed history
    #
    # The chart always contains 12 buckets.
    #
    # Examples:
    #
    # 7 days  → approximately 14-hour buckets
    # 30 days → approximately 2.5-day buckets
    # 90 days → approximately 7.5-day buckets
    # -----------------------------------------------------

    bucket_count = 12

    period_seconds = (
        days * 24 * 60 * 60
    )

    bucket_seconds = (
        period_seconds / bucket_count
    )

    buckets = []

    for i in range(
        bucket_count,
        0,
        -1,
    ):

        start = (
            now
            - (i * bucket_seconds)
        )

        end = (
            now
            - ((i - 1) * bucket_seconds)
        )

        bucket_rows = [
            r
            for r in rows
            if start
            <= float(r["created_at"])
            < end
        ]

        bucket_requests = len(
            bucket_rows
        )

        bucket_errors = sum(
            1
            for r in bucket_rows
            if int(r["status_code"] or 0) >= 400
        )

        # Use a readable label depending on the selected
        # period.
        if days <= 7:
            label = time.strftime(
                "%b %d %H:%M",
                time.localtime(end),
            )
        else:
            label = time.strftime(
                "%b %d",
                time.localtime(end),
            )

        buckets.append({
            "label": label,
            "requests": bucket_requests,
            "errors": bucket_errors,
        })

    # -----------------------------------------------------
    # Return dashboard metrics
    # -----------------------------------------------------

    return {
        "period_days": days,

        "total_requests": total,

        "avg_response_ms": avg,

        "error_count": errors,

        "deployments": deployments,

        "failed_builds": failed_builds,

        "success_rate": success_rate,

        "history": buckets,
    }