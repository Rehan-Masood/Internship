from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flasgger import Swagger
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://"
)
swagger = Swagger()


def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = 'development'
    
    # Validate production config DATABASE_URL when production config is selected
    if config_name == 'production':
        import os
        if not os.getenv('DATABASE_URL'):
            raise ValueError("DATABASE_URL environment variable is required in production")
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize Swagger
    swagger.init_app(app)
    
    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.tasks import tasks_bp
    from app.api.users import users_bp
    from app.api.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Register frontend routes
    from app.routes import frontend_bp
    app.register_blueprint(frontend_bp)
    
    # Error handlers
    from app.utils.errors import register_error_handlers
    register_error_handlers(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
