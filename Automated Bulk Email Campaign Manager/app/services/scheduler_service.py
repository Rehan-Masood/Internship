from datetime import datetime
from zoneinfo import ZoneInfo

from app import db
from app.models import Campaign
from app.services.email_service import process_campaign


# Pakistan Standard Time
PAKISTAN_TZ = ZoneInfo("Asia/Karachi")


def pakistan_now():
    """
    Return the current Pakistan time as a naive datetime.

    Campaign datetime-local values are stored without timezone
    information, so we compare them against the same naive
    Pakistan-local time.
    """
    return datetime.now(PAKISTAN_TZ).replace(tzinfo=None)


def run_scheduled_campaigns():
    now = pakistan_now()

    print(
        f"[Scheduler] Checking campaigns at "
        f"{now.strftime('%Y-%m-%d %H:%M:%S')} PKT"
    )

    campaigns = Campaign.query.filter(
        Campaign.status == "Scheduled",
        Campaign.scheduled_at.isnot(None),
        Campaign.scheduled_at <= now
    ).all()

    if not campaigns:
        return

    for campaign in campaigns:

        print(
            f"[Scheduler] Running campaign #{campaign.id}: "
            f"{campaign.name}"
        )

        try:

            process_campaign(campaign)

            print(
                f"[Scheduler] Campaign #{campaign.id} "
                f"finished with status: {campaign.status}"
            )

        except Exception as exc:

            campaign.status = "Failed"
            db.session.commit()

            print(
                f"[Scheduler] Campaign #{campaign.id} failed: "
                f"{exc}"
            )


def register_jobs(app):

    from app import scheduler

    if not scheduler.get_job("mailflow-scheduler"):

        scheduler.add_job(
            id="mailflow-scheduler",
            func=lambda: run_in_app_context(app),
            trigger="interval",
            minutes=1,
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

        print(
            "[Scheduler] MailFlow scheduler started."
        )


def run_in_app_context(app):

    with app.app_context():
        run_scheduled_campaigns()