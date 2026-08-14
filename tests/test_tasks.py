"""Task tests"""
import pytest
from datetime import datetime, timedelta


class TestGetTasks:
    def test_get_tasks_success(self, client, user_token, app):
        """Test getting tasks"""
        with app.app_context():
            from app.models import User, Task
            user = User.query.filter_by(email='user@test.com').first()
            task = Task(
                title='Test Task',
                description='Test',
                status='Pending',
                priority='High',
                created_by=user.id,
                assigned_to=user.id
            )
            from app import db
            db.session.add(task)
            db.session.commit()

        response = client.get('/api/tasks', headers={
            'Authorization': f'Bearer {user_token}'
        })
        assert response.status_code == 200
        assert response.json['success'] is True
        assert len(response.json['data']) == 1

    def test_get_tasks_pagination(self, client, user_token, app):
        """Test task pagination"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            user = User.query.filter_by(email='user@test.com').first()
            for i in range(15):
                task = Task(
                    title=f'Task {i}',
                    status='Pending',
                    priority='Medium',
                    created_by=user.id
                )
                db.session.add(task)
            db.session.commit()

        response = client.get('/api/tasks?page=1&per_page=10', headers={
            'Authorization': f'Bearer {user_token}'
        })
        assert response.status_code == 200
        assert len(response.json['data']) == 10
        assert response.json['pagination']['page'] == 1
        assert response.json['pagination']['total'] == 15

    def test_get_tasks_filter_status(self, client, user_token, app):
        """Test task filtering by status"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            user = User.query.filter_by(email='user@test.com').first()
            task1 = Task(
                title='Pending Task',
                status='Pending',
                priority='Medium',
                created_by=user.id
            )
            task2 = Task(
                title='Completed Task',
                status='Completed',
                priority='Medium',
                created_by=user.id
            )
            db.session.add_all([task1, task2])
            db.session.commit()

        response = client.get('/api/tasks?status=Pending', headers={
            'Authorization': f'Bearer {user_token}'
        })
        assert response.status_code == 200
        assert len(response.json['data']) == 1
        assert response.json['data'][0]['status'] == 'Pending'

    def test_get_tasks_search(self, client, user_token, app):
        """Test task search"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            user = User.query.filter_by(email='user@test.com').first()
            task = Task(
                title='Authentication System',
                description='Build JWT auth',
                status='Pending',
                priority='High',
                created_by=user.id
            )
            db.session.add(task)
            db.session.commit()

        response = client.get('/api/tasks?search=authentication', headers={
            'Authorization': f'Bearer {user_token}'
        })
        assert response.status_code == 200
        assert len(response.json['data']) == 1

    def test_get_tasks_no_token(self, client):
        """Test getting tasks without authentication"""
        response = client.get('/api/tasks')
        assert response.status_code == 401


class TestGetTask:
    def test_get_task_success(self, client, user_token, app):
        """Test getting single task"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            user = User.query.filter_by(email='user@test.com').first()
            task = Task(
                title='Test Task',
                status='Pending',
                priority='High',
                created_by=user.id
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.get(f'/api/tasks/{task_id}', headers={
            'Authorization': f'Bearer {user_token}'
        })
        assert response.status_code == 200
        assert response.json['data']['id'] == task_id

    def test_get_task_not_found(self, client, user_token):
        """Test getting non-existent task"""
        response = client.get('/api/tasks/999', headers={
            'Authorization': f'Bearer {user_token}'
        })
        assert response.status_code == 404

    def test_get_task_unauthorized(self, client, user_token, admin_token, app):
        """Test accessing another user's task without permission"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            admin = User.query.filter_by(email='admin@test.com').first()
            task = Task(
                title='Admin Task',
                status='Pending',
                priority='High',
                created_by=admin.id
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.get(f'/api/tasks/{task_id}', headers={
            'Authorization': f'Bearer {user_token}'
        })
        assert response.status_code == 403


class TestCreateTask:
    def test_create_task_success(self, client, user_token):
        """Test creating task"""
        response = client.post('/api/tasks', 
            headers={'Authorization': f'Bearer {user_token}'},
            json={
                'title': 'New Task',
                'description': 'Test task',
                'priority': 'High',
                'status': 'Pending'
            }
        )
        assert response.status_code == 201
        assert response.json['success'] is True
        assert response.json['data']['title'] == 'New Task'

    def test_create_task_missing_title(self, client, user_token):
        """Test creating task without title"""
        response = client.post('/api/tasks',
            headers={'Authorization': f'Bearer {user_token}'},
            json={
                'priority': 'High'
            }
        )
        assert response.status_code == 422

    def test_create_task_invalid_priority(self, client, user_token):
        """Test creating task with invalid priority"""
        response = client.post('/api/tasks',
            headers={'Authorization': f'Bearer {user_token}'},
            json={
                'title': 'Task',
                'priority': 'InvalidPriority'
            }
        )
        assert response.status_code == 422


class TestUpdateTask:
    def test_update_task_success(self, client, user_token, app):
        """Test updating task"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            user = User.query.filter_by(email='user@test.com').first()
            task = Task(
                title='Original Title',
                status='Pending',
                priority='High',
                created_by=user.id
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.put(f'/api/tasks/{task_id}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={
                'title': 'Updated Title',
                'status': 'Completed'
            }
        )
        assert response.status_code == 200
        assert response.json['data']['title'] == 'Updated Title'
        assert response.json['data']['status'] == 'Completed'

    def test_update_task_not_found(self, client, user_token):
        """Test updating non-existent task"""
        response = client.put('/api/tasks/999',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'title': 'Updated'}
        )
        assert response.status_code == 404


class TestDeleteTask:
    def test_delete_task_success(self, client, user_token, app):
        """Test deleting task"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            user = User.query.filter_by(email='user@test.com').first()
            task = Task(
                title='To Delete',
                status='Pending',
                priority='High',
                created_by=user.id
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.delete(f'/api/tasks/{task_id}',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 200
        assert response.json['success'] is True

    def test_delete_task_not_found(self, client, user_token):
        """Test deleting non-existent task"""
        response = client.delete('/api/tasks/999',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 404
