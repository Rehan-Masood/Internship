from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from app import db
from app.models import Campaign, EmailTemplate, ContactGroup
from app.services.email_service import process_campaign


campaigns_bp = Blueprint(
    "campaigns",
    __name__
)


@campaigns_bp.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        template_id = request.form.get(
            "template_id",
            type=int
        )

        group_id = request.form.get(
            "group_id",
            type=int
        )

        scheduled_raw = request.form.get(
            "scheduled_at",
            ""
        ).strip()

        if not name or not template_id or not group_id:
            flash(
                "Campaign name, template and group are required.",
                "danger"
            )

            return redirect(
                url_for("campaigns.index")
            )

        scheduled_at = None
        status = "Draft"

        if scheduled_raw:

            try:
                scheduled_at = datetime.fromisoformat(
                    scheduled_raw
                )

                status = "Scheduled"

            except ValueError:

                flash(
                    "Invalid scheduled date/time.",
                    "danger"
                )

                return redirect(
                    url_for("campaigns.index")
                )

        campaign = Campaign(
            name=name,
            template_id=template_id,
            group_id=group_id,
            scheduled_at=scheduled_at,
            status=status
        )

        db.session.add(campaign)
        db.session.commit()

        flash(
            "Campaign created successfully.",
            "success"
        )

        return redirect(
            url_for("campaigns.index")
        )

    campaigns = Campaign.query.order_by(
        Campaign.created_at.desc()
    ).all()

    templates = EmailTemplate.query.order_by(
        EmailTemplate.name
    ).all()

    groups = ContactGroup.query.order_by(
        ContactGroup.name
    ).all()

    return render_template(
        "campaigns.html",
        campaigns=campaigns,
        templates=templates,
        groups=groups
    )


@campaigns_bp.post("/<int:campaign_id>/send")
def send(campaign_id):

    campaign = Campaign.query.get_or_404(
        campaign_id
    )

    if campaign.status == "Sending":
        flash(
            "Campaign is already being processed.",
            "warning"
        )

        return redirect(
            url_for("campaigns.index")
        )

    if campaign.status == "Completed":
        flash(
            "This campaign has already been completed.",
            "warning"
        )

        return redirect(
            url_for("campaigns.index")
        )

    try:

        process_campaign(campaign)

        if campaign.status == "Completed":

            flash(
                "Campaign sent successfully. "
                "Check Logs for delivery results.",
                "success"
            )

        elif campaign.status == "Scheduled":

            flash(
                "Campaign is pending because the hourly "
                "sending limit was reached.",
                "warning"
            )

        else:

            flash(
                "Campaign processing finished. "
                "Check Logs for any failed emails.",
                "info"
            )

    except Exception as exc:

        campaign.status = "Failed"
        db.session.commit()

        flash(
            f"Campaign failed: {exc}",
            "danger"
        )

    return redirect(
        url_for("campaigns.index")
    )