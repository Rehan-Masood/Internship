from flask import Blueprint, render_template
from sqlalchemy import func
from app import db
from app.models import Contact, Campaign, EmailLog, EmailTemplate, Suppression

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.get("/")
def index():
    total_contacts = Contact.query.count()
    total_campaigns = Campaign.query.count()
    sent = EmailLog.query.filter_by(status="Sent").count()
    failed = EmailLog.query.filter_by(status="Failed").count()
    pending = EmailLog.query.filter_by(status="Pending").count()
    skipped = EmailLog.query.filter_by(status="Skipped").count()
    total = sent + failed
    success_rate = round((sent / total) * 100, 2) if total else 0

    recent = Campaign.query.order_by(Campaign.created_at.desc()).limit(8).all()

    return render_template(
        "dashboard.html",
        total_contacts=total_contacts,
        total_campaigns=total_campaigns,
        sent=sent,
        failed=failed,
        pending=pending,
        skipped=skipped,
        success_rate=success_rate,
        recent_campaigns=recent,
    )
