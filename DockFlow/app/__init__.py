from flask import Flask, render_template
from .config import Config
from .extensions import db, init_logging

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .routes.main import main_bp
    from .routes.dashboard import dashboard_bp
    from .routes.health import health_bp
    from .routes.services import services_bp
    from .routes.containers import containers_bp
    from .routes.cicd import cicd_bp
    from .routes.deployments import deployments_bp
    from .routes.logs import logs_bp
    from .routes.monitoring import monitoring_bp
    from .routes.settings import settings_bp
    from .routes.documentation import documentation_bp
    from .routes.api import api_bp

    for bp in [
        main_bp, dashboard_bp, health_bp, services_bp, containers_bp,
        cicd_bp, deployments_bp, logs_bp, monitoring_bp, settings_bp,
        documentation_bp, api_bp
    ]:
        app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(_):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_):
        return render_template("errors/500.html"), 500

    # Create the database tables before any logging handler writes to app_logs.
    with app.app_context():
        db.ensure_schema()
        init_logging(app)
        app.logger.info("DockFlow application started")

    return app
