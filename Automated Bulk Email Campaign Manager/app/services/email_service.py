import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

from flask import current_app

from app import db
from app.models import EmailLog, Suppression, SMTPSetting
from app.utils.email_utils import personalize


def get_smtp():
    return SMTPSetting.query.order_by(
        SMTPSetting.id.desc()
    ).first()


def sent_count_last_hour():
    cutoff = datetime.utcnow() - timedelta(hours=1)

    return EmailLog.query.filter(
        EmailLog.status == "Sent",
        EmailLog.sent_at >= cutoff
    ).count()


def send_one(campaign, contact):

    if not contact.subscribed:
        return "Skipped", "Contact is unsubscribed."

    if Suppression.query.filter_by(
        email=contact.email
    ).first():
        return "Skipped", "Recipient is on suppression list."

    if sent_count_last_hour() >= current_app.config[
        "RATE_LIMIT_PER_HOUR"
    ]:
        return "Pending", "Hourly rate limit reached."

    setting = get_smtp()

    if not setting:
        return "Failed", "SMTP settings are not configured."

    subject = personalize(
        campaign.template.subject,
        contact
    )

    html = personalize(
        campaign.template.html_body,
        contact
    )

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = (
        f"{setting.from_name} <{setting.username}>"
    )
    msg["To"] = contact.email

    msg.set_content(
        "This email requires an HTML-capable email client."
    )

    msg.add_alternative(
        html,
        subtype="html"
    )

    try:

        if setting.use_tls:

            with smtplib.SMTP(
                setting.host,
                setting.port,
                timeout=30
            ) as server:

                server.ehlo()
                server.starttls()
                server.ehlo()

                server.login(
                    setting.username,
                    setting.password
                )

                server.send_message(msg)

        else:

            with smtplib.SMTP(
                setting.host,
                setting.port,
                timeout=30
            ) as server:

                server.ehlo()

                server.login(
                    setting.username,
                    setting.password
                )

                server.send_message(msg)

        return "Sent", "SMTP accepted the message."

    except smtplib.SMTPAuthenticationError:
        return (
            "Failed",
            "SMTP authentication failed. "
            "Check your email and app password."
        )

    except smtplib.SMTPConnectError:
        return (
            "Failed",
            "Could not connect to the SMTP server."
        )

    except smtplib.SMTPException as exc:
        return (
            "Failed",
            f"SMTP error: {exc}"
        )

    except Exception as exc:
        return (
            "Failed",
            str(exc)
        )


def process_campaign(campaign):

    from app.models import Contact

    campaign.status = "Sending"
    campaign.started_at = datetime.utcnow()

    db.session.commit()

    contacts = Contact.query.filter_by(
        group_id=campaign.group_id,
        subscribed=True
    ).all()

    if not contacts:
        campaign.status = "Completed"
        campaign.completed_at = datetime.utcnow()
        db.session.commit()
        return

    for contact in contacts:

        status, message = send_one(
            campaign,
            contact
        )

        log = EmailLog(
            campaign_id=campaign.id,
            contact_id=contact.id,
            recipient=contact.email,
            status=status,
            provider_message=(
                message
                if status == "Sent"
                else None
            ),
            error_message=(
                message
                if status in (
                    "Failed",
                    "Skipped",
                    "Pending"
                )
                else None
            ),
            sent_at=(
                datetime.utcnow()
                if status == "Sent"
                else None
            ),
        )

        db.session.add(log)
        db.session.commit()

        if status == "Pending":
            campaign.status = "Scheduled"
            db.session.commit()
            break

    else:
        campaign.status = "Completed"
        campaign.completed_at = datetime.utcnow()
        db.session.commit()