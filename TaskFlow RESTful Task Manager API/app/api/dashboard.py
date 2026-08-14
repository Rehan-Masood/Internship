from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.models import Task, User
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """
    Get dashboard statistics
    ---
    tags:
      - Dashboard
    security:
      - Bearer: []
    responses:
      200:
        description: Dashboard statistics retrieved successfully
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
    
    # Base query based on user role
    if user.is_admin():
        task_query = Task.query
    else:
        task_query = Task.query.filter(
            (Task.created_by == user_id) | (Task.assigned_to == user_id)
        )
    
    # Calculate statistics
    total_tasks = task_query.count()
    pending_tasks = task_query.filter_by(status=Task.STATUS_PENDING).count()
    in_progress_tasks = task_query.filter_by(status=Task.STATUS_IN_PROGRESS).count()
    completed_tasks = task_query.filter_by(status=Task.STATUS_COMPLETED).count()
    
    # Overdue tasks (due date in past and not completed)
    now = datetime.utcnow()
    overdue_tasks = task_query.filter(
        Task.due_date < now,
        Task.status != Task.STATUS_COMPLETED
    ).count()
    
    # High priority tasks
    high_priority_tasks = task_query.filter_by(priority=Task.PRIORITY_HIGH).count()
    
    # Total users (admin only)
    total_users = User.query.count() if user.is_admin() else None
    
    # Tasks by priority
    priority_stats = {}
    for priority in Task.PRIORITIES:
        count = task_query.filter_by(priority=priority).count()
        priority_stats[priority] = count
    
    # Tasks by status
    status_stats = {}
    for status in Task.STATUSES:
        count = task_query.filter_by(status=status).count()
        status_stats[status] = count
    
    # Recent tasks (last 5)
    recent_tasks = task_query.order_by(Task.created_at.desc()).limit(5).all()
    
    stats = {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'high_priority_tasks': high_priority_tasks,
        'priority_stats': priority_stats,
        'status_stats': status_stats,
        'recent_tasks': [task.to_dict() for task in recent_tasks]
    }
    
    if total_users is not None:
        stats['total_users'] = total_users
    
    return jsonify({
        'success': True,
        'message': 'Dashboard statistics retrieved successfully',
        'data': stats
    }), 200


@dashboard_bp.route('/chart-data', methods=['GET'])
@jwt_required()
def get_chart_data():
    """
    Get chart data for analytics
    ---
    tags:
      - Dashboard
    security:
      - Bearer: []
    responses:
      200:
        description: Chart data retrieved successfully
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
    
    # Base query based on user role
    if user.is_admin():
        task_query = Task.query
    else:
        task_query = Task.query.filter(
            (Task.created_by == user_id) | (Task.assigned_to == user_id)
        )
    
    # Tasks by status for chart
    status_chart = {}
    for status in Task.STATUSES:
        count = task_query.filter_by(status=status).count()
        status_chart[status] = count
    
    # Tasks by priority for chart
    priority_chart = {}
    for priority in Task.PRIORITIES:
        count = task_query.filter_by(priority=priority).count()
        priority_chart[priority] = count
    
    # Weekly task creation (last 4 weeks)
    now = datetime.utcnow()
    weekly_data = {}
    
    for week in range(4):
        week_start = now - timedelta(weeks=week+1)
        week_end = now - timedelta(weeks=week)
        
        count = task_query.filter(
            Task.created_at >= week_start,
            Task.created_at < week_end
        ).count()
        
        week_label = f'Week {4-week}'
        weekly_data[week_label] = count
    
    # Reverse to show chronological order
    weekly_data = dict(reversed(weekly_data.items()))
    
    return jsonify({
        'success': True,
        'message': 'Chart data retrieved successfully',
        'data': {
            'status_chart': status_chart,
            'priority_chart': priority_chart,
            'weekly_data': weekly_data
        }
    }), 200
