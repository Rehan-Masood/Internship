from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User


def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or not user.is_admin():
            return jsonify({
                'success': False,
                'error': 'FORBIDDEN',
                'message': 'Admin privileges required'
            }), 403
        
        return fn(*args, **kwargs)
    
    return wrapper


def token_required(fn):
    """Decorator to require valid JWT token"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'UNAUTHORIZED',
                'message': 'Invalid token'
            }), 401
        
        return fn(*args, **kwargs)
    
    return wrapper
