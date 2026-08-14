#!/usr/bin/env python
"""TaskFlow Application Entry Point"""

import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Task

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Add models to shell context"""
    return {'db': db, 'User': User, 'Task': Task}


@app.cli.command()
def init_db():
    """Initialize database with sample data"""
    db.create_all()
    print('Database initialized')


@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    # Check if data already exists
    if User.query.first():
        print('Database already seeded')
        return

    # Create admin user
    admin = User(
        name='Admin User',
        email='admin@taskflow.com',
        role='admin'
    )
    admin.set_password('admin123')

    # Create regular user
    user = User(
        name='Rehan Ahmed',
        email='rehan@taskflow.com',
        role='user'
    )
    user.set_password('user123')

    # Create another user
    user2 = User(
        name='Ali Raza',
        email='ali@taskflow.com',
        role='user'
    )
    user2.set_password('user123')

    db.session.add_all([admin, user, user2])
    db.session.commit()

    # Create sample tasks
    tasks = [
        Task(
            title='Build authentication API',
            description='Implement JWT-based authentication system',
            status=Task.STATUS_PENDING,
            priority=Task.PRIORITY_HIGH,
            created_by=user.id,
            assigned_to=user.id
        ),
        Task(
            title='Database migration',
            description='Set up PostgreSQL database and migrations',
            status=Task.STATUS_COMPLETED,
            priority=Task.PRIORITY_MEDIUM,
            created_by=admin.id,
            assigned_to=user2.id
        ),
        Task(
            title='API documentation',
            description='Write Swagger/OpenAPI documentation',
            status=Task.STATUS_IN_PROGRESS,
            priority=Task.PRIORITY_MEDIUM,
            created_by=admin.id,
            assigned_to=user.id
        ),
        Task(
            title='Fix user roles bug',
            description='Admin users should not be able to delete other admins',
            status=Task.STATUS_PENDING,
            priority=Task.PRIORITY_HIGH,
            created_by=user.id,
            assigned_to=admin.id
        ),
        Task(
            title='UI improvements',
            description='Enhance the dashboard with better styling',
            status=Task.STATUS_PENDING,
            priority=Task.PRIORITY_LOW,
            created_by=user.id,
            assigned_to=user2.id
        ),
    ]

    db.session.add_all(tasks)
    db.session.commit()

    print('Database seeded with sample data')
    print(f'Created 3 users: admin@taskflow.com, rehan@taskflow.com, ali@taskflow.com')
    print(f'Created 5 sample tasks')
    print(f'Default password for all users: user123 / admin123')


if __name__ == '__main__':
    app.run(debug=True)
