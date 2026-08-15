import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler


db = SQLAlchemy()
scheduler = APScheduler()


def create_app():

    app = Flask(
        __name__,
        instance_relative_config=True
    )

    # Required directories
    os.makedirs(
        app.instance_path,
        exist_ok=True
    )

    os.makedirs(
        os.path.join(app.root_path, "uploads"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(app.root_path, "logs"),
        exist_ok=True
    )

    # Load configuration
    app.config.from_object("config.Config")

    # Initialize database
    db.init_app(app)

    # Initialize scheduler
    scheduler.init_app(app)

    if not scheduler.running:
        scheduler.start()

    # Register routes
    from app.routes.dashboard import dashboard_bp
    from app.routes.contacts import contacts_bp
    from app.routes.templates import templates_bp
    from app.routes.campaigns import campaigns_bp
    from app.routes.logs import logs_bp
    from app.routes.settings import settings_bp

    app.register_blueprint(
        dashboard_bp
    )

    app.register_blueprint(
        contacts_bp,
        url_prefix="/contacts"
    )

    app.register_blueprint(
        templates_bp,
        url_prefix="/templates"
    )

    app.register_blueprint(
        campaigns_bp,
        url_prefix="/campaigns"
    )

    app.register_blueprint(
        logs_bp,
        url_prefix="/logs"
    )

    app.register_blueprint(
        settings_bp,
        url_prefix="/settings"
    )

    # Database initialization
    with app.app_context():

        from app.models import (
            Contact,
            ContactGroup,
            EmailTemplate,
            Campaign,
            EmailLog,
            SMTPSetting,
            Suppression,
        )

        db.create_all()

        # Automatically create SMTP database configuration
        # from environment variables if no SMTP record exists.
        smtp_exists = SMTPSetting.query.first()

        if not smtp_exists:

            smtp_host = app.config.get("SMTP_HOST")
            smtp_port = app.config.get("SMTP_PORT")
            smtp_username = app.config.get("SMTP_USERNAME")
            smtp_password = app.config.get("SMTP_PASSWORD")
            smtp_use_tls = app.config.get("SMTP_USE_TLS")
            smtp_from_name = app.config.get("SMTP_FROM_NAME")

            if (
                smtp_host
                and smtp_username
                and smtp_password
            ):

                smtp_setting = SMTPSetting(
                    host=smtp_host,
                    port=smtp_port,
                    username=smtp_username,
                    password=smtp_password,
                    use_tls=smtp_use_tls,
                    from_name=smtp_from_name,
                )

                db.session.add(
                    smtp_setting
                )

                db.session.commit()

                print(
                    "[SMTP] SMTP configuration "
                    "loaded from environment."
                )

            else:

                print(
                    "[SMTP] SMTP configuration "
                    "is incomplete."
                )

    # Register scheduler jobs
    from app.services.scheduler_service import register_jobs

    register_jobs(app)

    return app