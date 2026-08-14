from flask import Blueprint, render_template, send_from_directory
import os

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    """Serve main dashboard"""
    return render_template('index.html')


@frontend_bp.route('/login')
def login():
    """Serve login page"""
    return render_template('index.html')


@frontend_bp.route('/dashboard')
def dashboard():
    """Serve dashboard"""
    return render_template('index.html')


@frontend_bp.route('/tasks')
def my_tasks():
    """Serve my tasks page"""
    return render_template('index.html')


@frontend_bp.route('/create-task')
def create_task():
    """Serve create task page"""
    return render_template('index.html')


@frontend_bp.route('/analytics')
def analytics():
    """Serve analytics page"""
    return render_template('index.html')


@frontend_bp.route('/users')
def users():
    """Serve users management page"""
    return render_template('index.html')


@frontend_bp.route('/api-documentation')
def api_documentation():
    """Serve API documentation page"""
    return render_template('index.html')


@frontend_bp.route('/settings')
def settings():
    """Serve settings page"""
    return render_template('index.html')


@frontend_bp.route('/api/docs')
def swagger_docs():
    """Redirect to Swagger UI"""
    return render_template('swagger.html')
