import pytest
import os
from app import create_app, db
from app.models import User, Task


@pytest.fixture(scope='session')
def app():
    """Create and configure test app"""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Clean database before each test"""
    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture
def admin_user(app):
    """Create admin user"""
    with app.app_context():
        user = User(
            name='Admin',
            email='admin@test.com',
            role='admin'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def regular_user(app):
    """Create regular user"""
    with app.app_context():
        user = User(
            name='User',
            email='user@test.com',
            role='user'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def admin_token(client, admin_user):
    """Get admin JWT token"""
    response = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'password123'
    })
    return response.json['data']['access_token']


@pytest.fixture
def user_token(client, regular_user):
    """Get regular user JWT token"""
    response = client.post('/api/auth/login', json={
        'email': 'user@test.com',
        'password': 'password123'
    })
    return response.json['data']['access_token']
