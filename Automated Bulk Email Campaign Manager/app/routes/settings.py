from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import SMTPSetting

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/", methods=["GET", "POST"])
def index():
    setting = SMTPSetting.query.order_by(SMTPSetting.id.desc()).first()

    if request.method == "POST":
        if not setting:
            setting = SMTPSetting()
            db.session.add(setting)

        setting.host = request.form.get("host", "").strip()
        setting.port = request.form.get("port", type=int) or 587
        setting.username = request.form.get("username", "").strip()
        setting.password = request.form.get("password", "")
        setting.use_tls = request.form.get("use_tls") == "on"
        setting.from_name = request.form.get("from_name", "MailFlow").strip()

        db.session.commit()
        flash("SMTP settings saved.", "success")
        return redirect(url_for("settings.index"))

    return render_template("settings.html", setting=setting)
