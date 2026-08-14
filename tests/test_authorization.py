"""Authorization and role-based access tests"""
import pytest


class TestAdminAccess:
    def test_admin_can_access_users(self, client, admin_token):
        """Test admin can access users endpoint"""
        response = client.get('/api/users',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code == 200

    def test_user_cannot_access_users(self, client, user_token):
        """Test regular user cannot access users endpoint"""
        response = client.get('/api/users',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 403

    def test_user_cannot_delete_user(self, client, user_token, admin_token, app):
        """Test regular user cannot delete users"""
        with app.app_context():
            from app.models import User
            admin = User.query.filter_by(email='admin@test.com').first()

        response = client.delete(f'/api/users/{admin.id}',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 403

    def test_admin_can_delete_user(self, client, admin_token, app):
        """Test admin can delete users"""
        with app.app_context():
            from app.models import User
            from app import db
            user = User(
                name='To Delete',
                email='todelete@test.com',
                role='user'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        response = client.delete(f'/api/users/{user_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code == 200

    def test_admin_can_update_user_role(self, client, admin_token, app):
        """Test admin can update user roles"""
        with app.app_context():
            from app.models import User
            user = User.query.filter_by(email='user@test.com').first()

        response = client.put(f'/api/users/{user.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'role': 'admin'}
        )
        assert response.status_code == 200
        assert response.json['data']['role'] == 'admin'


class TestTaskAuthorization:
    def test_user_cannot_edit_others_task(self, client, user_token, admin_token, app):
        """Test user cannot edit another user's task"""
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

        response = client.put(f'/api/tasks/{task_id}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'title': 'Hacked'}
        )
        assert response.status_code == 403

    def test_admin_can_edit_any_task(self, client, admin_token, app):
        """Test admin can edit any task"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            user = User.query.filter_by(email='user@test.com').first()
            task = Task(
                title='User Task',
                status='Pending',
                priority='High',
                created_by=user.id
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.put(f'/api/tasks/{task_id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'title': 'Admin Modified'}
        )
        assert response.status_code == 200

    def test_user_can_view_assigned_task(self, client, user_token, app):
        """Test user can view tasks assigned to them"""
        with app.app_context():
            from app.models import User, Task
            from app import db
            user = User.query.filter_by(email='user@test.com').first()
            admin = User.query.filter_by(email='admin@test.com').first()
            task = Task(
                title='Assigned Task',
                status='Pending',
                priority='High',
                created_by=admin.id,
                assigned_to=user.id
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.get(f'/api/tasks/{task_id}',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 200

    def test_user_cannot_delete_others_task(self, client, user_token, admin_token, app):
        """Test user cannot delete another user's task"""
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

        response = client.delete(f'/api/tasks/{task_id}',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 403
