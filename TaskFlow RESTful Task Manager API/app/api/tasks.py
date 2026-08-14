from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import or_
from app import db, limiter
from app.models import Task, User
from app.schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema

tasks_bp = Blueprint('tasks', __name__)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
task_create_schema = TaskCreateSchema()
task_update_schema = TaskUpdateSchema()


@tasks_bp.route('', methods=['GET'])
@jwt_required()
@limiter.limit("100/hour")
def get_tasks():
    """
    Get all tasks with filtering, search, and pagination
    ---
    tags:
      - Tasks
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
      - name: status
        in: query
        type: string
        enum: [Pending, In Progress, Completed]
      - name: priority
        in: query
        type: string
        enum: [Low, Medium, High]
      - name: search
        in: query
        type: string
      - name: assigned_to
        in: query
        type: integer
      - name: created_by
        in: query
        type: integer
    responses:
      200:
        description: Tasks retrieved successfully
      401:
        description: Unauthorized
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'UNAUTHORIZED',
            'message': 'User not found'
        }), 401
    
    # Build query
    query = Task.query
    
    # Admins see all tasks, users see only their tasks
    if not user.is_admin():
        query = query.filter(
            (Task.created_by == user_id) | (Task.assigned_to == user_id)
        )
    
    # Filtering
    status = request.args.get('status')
    if status and status in Task.STATUSES:
        query = query.filter_by(status=status)
    
    priority = request.args.get('priority')
    if priority and priority in Task.PRIORITIES:
        query = query.filter_by(priority=priority)
    
    assigned_to = request.args.get('assigned_to', type=int)
    if assigned_to:
        query = query.filter_by(assigned_to=assigned_to)
    
    created_by = request.args.get('created_by', type=int)
    if created_by:
        query = query.filter_by(created_by=created_by)
    
    # Search
    search = request.args.get('search')
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f'%{search}%'),
                Task.description.ilike(f'%{search}%')
            )
        )
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10
    
    paginated = query.order_by(Task.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'success': True,
        'message': 'Tasks retrieved successfully',
        'data': tasks_schema.dump(paginated.items),
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    }), 200


@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
@limiter.limit("100/hour")
def get_task(task_id):
    """
    Get a single task by ID
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task retrieved successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({
            'success': False,
            'error': 'NOT_FOUND',
            'message': 'Task not found'
        }), 404
    
    # Check authorization
    if not user.is_admin() and task.created_by != user_id and task.assigned_to != user_id:
        return jsonify({
            'success': False,
            'error': 'FORBIDDEN',
            'message': 'You do not have permission to view this task'
        }), 403
    
    return jsonify({
        'success': True,
        'message': 'Task retrieved successfully',
        'data': task_schema.dump(task)
    }), 200


@tasks_bp.route('', methods=['POST'])
@jwt_required()
@limiter.limit("50/hour")
def create_task():
    """
    Create a new task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            priority:
              type: string
              enum: [Low, Medium, High]
            status:
              type: string
              enum: [Pending, In Progress, Completed]
            assigned_to:
              type: integer
            due_date:
              type: string
              format: date-time
    responses:
      201:
        description: Task created successfully
      401:
        description: Unauthorized
      422:
        description: Validation error
    """
    user_id = int(get_jwt_identity())
    
    try:
        data = task_create_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({
            'success': False,
            'error': 'VALIDATION_ERROR',
            'message': 'Validation failed',
            'details': err.messages
        }), 422
    
    # Create task
    task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', Task.STATUS_PENDING),
        priority=data.get('priority', Task.PRIORITY_MEDIUM),
        created_by=user_id,
        assigned_to=data.get('assigned_to'),
        due_date=data.get('due_date')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Task created successfully',
        'data': task_schema.dump(task)
    }), 201


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50/hour")
def update_task(task_id):
    """
    Update a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            priority:
              type: string
              enum: [Low, Medium, High]
            status:
              type: string
              enum: [Pending, In Progress, Completed]
            assigned_to:
              type: integer
            due_date:
              type: string
              format: date-time
    responses:
      200:
        description: Task updated successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
      422:
        description: Validation error
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({
            'success': False,
            'error': 'NOT_FOUND',
            'message': 'Task not found'
        }), 404
    
    # Check authorization
    if not user.is_admin() and task.created_by != user_id:
        return jsonify({
            'success': False,
            'error': 'FORBIDDEN',
            'message': 'You do not have permission to update this task'
        }), 403
    
    try:
        data = task_update_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({
            'success': False,
            'error': 'VALIDATION_ERROR',
            'message': 'Validation failed',
            'details': err.messages
        }), 422
    
    # Update fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
    if 'priority' in data:
        task.priority = data['priority']
    if 'assigned_to' in data:
        task.assigned_to = data['assigned_to']
    if 'due_date' in data:
        task.due_date = data['due_date']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Task updated successfully',
        'data': task_schema.dump(task)
    }), 200


@tasks_bp.route('/<int:task_id>', methods=['PATCH'])
@jwt_required()
@limiter.limit("50/hour")
def partial_update_task(task_id):
    """
    Partially update a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
    responses:
      200:
        description: Task updated successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
    """
    # PATCH is same as PUT in this implementation
    return update_task(task_id)


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50/hour")
def delete_task(task_id):
    """
    Delete a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task deleted successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({
            'success': False,
            'error': 'NOT_FOUND',
            'message': 'Task not found'
        }), 404
    
    # Check authorization - only creator or admin can delete
    if not user.is_admin() and task.created_by != user_id:
        return jsonify({
            'success': False,
            'error': 'FORBIDDEN',
            'message': 'You do not have permission to delete this task'
        }), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Task deleted successfully'
    }), 200
