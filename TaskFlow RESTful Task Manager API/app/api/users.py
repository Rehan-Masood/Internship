from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Task
from app.schemas import UserSchema
from app.utils.decorators import admin_required

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_bp.route('', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """
    Get all users (Admin only)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Users retrieved successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden (not admin)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10
    
    paginated = User.query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'success': True,
        'message': 'Users retrieved successfully',
        'data': users_schema.dump(paginated.items),
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    }), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: User retrieved successfully
      401:
        description: Unauthorized
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'NOT_FOUND',
            'message': 'User not found'
        }), 404
    
    # Get user's task count
    user_dict = user.to_dict(include_email=True)
    user_dict['task_count'] = Task.query.filter(
        (Task.created_by == user_id) | (Task.assigned_to == user_id)
    ).count()
    
    return jsonify({
        'success': True,
        'message': 'User retrieved successfully',
        'data': user_dict
    }), 200


@users_bp.route('/assignable/list', methods=['GET'])
@jwt_required()
def get_assignable_users():
    """
    Get all users available for task assignment (accessible to all authenticated users)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 100
    responses:
      200:
        description: Users retrieved successfully
      401:
        description: Unauthorized
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 100
    
    paginated = User.query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'success': True,
        'message': 'Users retrieved successfully',
        'data': users_schema.dump(paginated.items),
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    }), 200


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """
    Update user (Admin only)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            role:
              type: string
              enum: [user, admin]
    responses:
      200:
        description: User updated successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden (not admin)
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'NOT_FOUND',
            'message': 'User not found'
        }), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    
    if 'role' in data and data['role'] in ['user', 'admin']:
        user.role = data['role']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User updated successfully',
        'data': user.to_dict(include_email=True)
    }), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """
    Delete user (Admin only)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: User deleted successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden (not admin)
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'NOT_FOUND',
            'message': 'User not found'
        }), 404
    
    # Delete all tasks created by user
    Task.query.filter_by(created_by=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User deleted successfully'
    }), 200
