from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app import db, limiter
from app.models import User
from app.schemas import UserSchema, UserRegisterSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()
register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5/hour")
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
              format: email
            password:
              type: string
              minLength: 6
            password_confirm:
              type: string
              minLength: 6
    responses:
      201:
        description: User registered successfully
      400:
        description: Validation error
      409:
        description: Email already registered
    """
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({
            'success': False,
            'error': 'VALIDATION_ERROR',
            'message': 'Validation failed',
            'details': err.messages
        }), 422
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'success': False,
            'error': 'CONFLICT',
            'message': 'Email already registered'
        }), 409
    
    # Create new user
    user = User(
        name=data['name'],
        email=data['email'],
        role='user'
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'data': user_schema.dump(user)
    }), 201


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10/hour")
def login():
    """
    Login user and get JWT token
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
      422:
        description: Validation error
    """
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({
            'success': False,
            'error': 'VALIDATION_ERROR',
            'message': 'Validation failed',
            'details': err.messages
        }), 422
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({
            'success': False,
            'error': 'UNAUTHORIZED',
            'message': 'Invalid email or password'
        }), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'data': {
            'user': user_schema.dump(user),
            'access_token': access_token
        }
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Current user info
      401:
        description: Unauthorized
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'UNAUTHORIZED',
            'message': 'User not found'
        }), 401
    
    return jsonify({
        'success': True,
        'message': 'User info retrieved',
        'data': user_schema.dump(user)
    }), 200
