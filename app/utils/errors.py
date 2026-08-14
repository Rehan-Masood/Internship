from flask import jsonify
from marshmallow import ValidationError
from flask_jwt_extended.exceptions import InvalidHeaderError, RevokedTokenError
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 'BAD_REQUEST',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 'UNAUTHORIZED',
            'message': 'Authentication required or invalid credentials'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 'FORBIDDEN',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'NOT_FOUND',
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            'success': False,
            'error': 'CONFLICT',
            'message': str(error)
        }), 409
    
    @app.errorhandler(422)
    def validation_error(error):
        return jsonify({
            'success': False,
            'error': 'VALIDATION_ERROR',
            'message': str(error)
        }), 422
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({
            'success': False,
            'error': 'RATE_LIMIT_EXCEEDED',
            'message': 'Maximum 100 requests per hour allowed'
        }), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {error}')
        return jsonify({
            'success': False,
            'error': 'INTERNAL_ERROR',
            'message': 'An internal server error occurred'
        }), 500
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            'success': False,
            'error': 'VALIDATION_ERROR',
            'message': 'Validation failed',
            'details': error.messages
        }), 422
    
    @app.errorhandler(InvalidHeaderError)
    def handle_auth_error(error):
        return jsonify({
            'success': False,
            'error': 'AUTH_ERROR',
            'message': str(error)
        }), 401
    
    @app.errorhandler(RevokedTokenError)
    def handle_revoked_token(error):
        return jsonify({
            'success': False,
            'error': 'TOKEN_REVOKED',
            'message': 'Token has been revoked'
        }), 401
