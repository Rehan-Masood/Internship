from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import EmailTemplate

templates_bp = Blueprint("templates", __name__)

@templates_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        subject = request.form.get("subject", "").strip()
        html_body = request.form.get("html_body", "").strip()

        if not name or not subject or not html_body:
            flash("All template fields are required.", "danger")
        else:
            db.session.add(EmailTemplate(
                name=name, subject=subject, html_body=html_body
            ))
            db.session.commit()
            flash("Template created.", "success")
            return redirect(url_for("templates.index"))

    templates = EmailTemplate.query.order_by(EmailTemplate.created_at.desc()).all()
    return render_template("templates.html", templates=templates)
