from datetime import datetime
from app import db

class ContactGroup(db.Model):
    __tablename__ = "contact_groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    contacts = db.relationship("Contact", backref="group", lazy=True)

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False, index=True)
    group_id = db.Column(db.Integer, db.ForeignKey("contact_groups.id"), nullable=True)
    subscribed = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Suppression(db.Model):
    __tablename__ = "suppressions"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False, index=True)
    reason = db.Column(db.String(255), default="Unsubscribed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class EmailTemplate(db.Model):
    __tablename__ = "email_templates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    html_body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Campaign(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey("email_templates.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("contact_groups.id"), nullable=False)
    status = db.Column(db.String(30), default="Draft", nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    template = db.relationship("EmailTemplate")
    group = db.relationship("ContactGroup")

class EmailLog(db.Model):
    __tablename__ = "email_logs"
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False)
    recipient = db.Column(db.String(320), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    provider_message = db.Column(db.Text, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    campaign = db.relationship("Campaign", backref="logs")
    contact = db.relationship("Contact")

class SMTPSetting(db.Model):
    __tablename__ = "smtp_settings"
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer, nullable=False, default=587)
    username = db.Column(db.String(320), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    use_tls = db.Column(db.Boolean, default=True, nullable=False)
    from_name = db.Column(db.String(160), default="MailFlow")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
