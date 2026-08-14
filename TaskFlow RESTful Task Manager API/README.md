# TaskFlow - RESTful Task Management API

A premium, production-ready task management system with a modern web interface, built with Flask, SQLAlchemy, PostgreSQL, and JWT authentication.

![TaskFlow](https://img.shields.io/badge/TaskFlow-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-3.0.0-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

## Demo Video
<video src="https://github.com/user-attachments/assets/535cd38d-5557-47a8-925a-94c7192b0c81" controls width="600"></video>

## Features

- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Role-Based Access Control** - Admin and User roles with proper authorization
- ✅ **RESTful API** - Clean, standards-compliant API design
- ✅ **Task Management** - Complete CRUD operations for tasks
- ✅ **Advanced Filtering** - Filter by status, priority, assignee, creator, search text
- ✅ **Pagination** - Efficient pagination for large datasets
- ✅ **Rate Limiting** - 100 requests per IP per hour
- ✅ **Dashboard Analytics** - Real-time statistics and charts
- ✅ **Swagger/OpenAPI** - Interactive API documentation
- ✅ **PostgreSQL** - Production-grade database
- ✅ **Premium UI** - Modern, responsive dashboard interface
- ✅ **User Management** - Admin controls for user administration
- ✅ **Real-time Updates** - Live dashboard data from API

## Technology Stack

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **Flask-RESTful 0.3.10** - RESTful API extension
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-JWT-Extended 4.5.3** - JWT authentication
- **Flask-Limiter 3.5.0** - Rate limiting
- **PostgreSQL 14+** - Database
- **Marshmallow 3.20.1** - Serialization/validation
- **Flasgger 0.9.7.1** - Swagger UI

### Frontend
- **HTML5**
- **CSS3** - Custom premium styling
- **JavaScript (Vanilla)** - No dependencies
- **Chart.js 4.4.0** - Analytics charts

### Testing
- **pytest 7.4.3**
- **pytest-cov 4.1.0**

## Project Structure

```
taskflow/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models/               # Database models
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/              # Marshmallow schemas
│   │   ├── user.py
│   │   └── task.py
│   ├── api/                  # API blueprints
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── tasks.py          # Task CRUD
│   │   ├── users.py          # User management
│   │   └── dashboard.py      # Dashboard stats
│   ├── utils/                # Utilities
│   │   ├── errors.py         # Error handlers
│   │   └── decorators.py     # Custom decorators
│   ├── templates/            # HTML templates
│   │   └── index.html
│   ├── static/               # Static files
│   │   ├── css/style.css     # Premium UI styles
│   │   └── js/               # JavaScript
│   │       ├── api.js        # API client
│   │       ├── auth.js       # Authentication
│   │       └── app.js        # Main application
│   └── routes.py             # Frontend routes
├── tests/                    # Test suite
│   ├── test_auth.py
│   ├── test_tasks.py
│   ├── test_authorization.py
│   └── test_api_responses.py
├── migrations/               # Database migrations
├── config.py                 # Configuration
├── run.py                    # Application entry point
├── requirements.txt          # Dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 14+
- pip or conda

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd taskflow

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. PostgreSQL Setup

```bash
# Create database
createdb taskflow_db

# Create test database
createdb taskflow_test_db
```

### 3. Environment Variables

```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your settings
# Required:
# - FLASK_ENV=development
# - DATABASE_URL=postgresql://user:password@localhost:5432/taskflow_db
# - JWT_SECRET_KEY=your-secret-key-here
# - SECRET_KEY=your-flask-secret-key
```

### 4. Database Migrations

```bash
# Initialize migrations (first time only)
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade

# Seed sample data (optional)
flask seed-db
```

## Running Locally

### Development Server

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Start Flask development server
python run.py

# Application will be available at http://localhost:5000
```

### Access the Application

- **Dashboard**: http://localhost:5000
- **API Base**: http://localhost:5000/api
- **Swagger UI**: http://localhost:5000/api/docs
- **Login**: http://localhost:5000/login

### Default Credentials (After seed-db)

```
Admin:
  Email: admin@taskflow.com
  Password: admin123

User 1:
  Email: rehan@taskflow.com
  Password: user123

User 2:
  Email: ali@taskflow.com
  Password: user123
```

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication

All endpoints except `/auth/register` and `/auth/login` require Bearer token authentication.

```bash
# Request header
Authorization: Bearer YOUR_JWT_TOKEN
```

### Authentication Endpoints

#### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "password_confirm": "securepassword"
}

# Response
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-08-13T10:30:00",
    "updated_at": "2024-08-13T10:30:00"
  }
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}

# Response
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": { ... },
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

#### Get Current User
```bash
GET /api/auth/me
Authorization: Bearer YOUR_TOKEN

# Response
{
  "success": true,
  "message": "User info retrieved",
  "data": { ... }
}
```

### Task Endpoints

#### Get Tasks (with filtering, search, pagination)
```bash
GET /api/tasks?page=1&per_page=10&status=Pending&priority=High&search=auth

# Response
{
  "success": true,
  "message": "Tasks retrieved successfully",
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 128,
    "pages": 13,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Single Task
```bash
GET /api/tasks/{id}
```

#### Create Task
```bash
POST /api/tasks
Content-Type: application/json

{
  "title": "Build authentication system",
  "description": "Implement JWT-based auth",
  "priority": "High",
  "status": "Pending",
  "assigned_to": 2,
  "due_date": "2024-08-20T17:00:00"
}
```

#### Update Task
```bash
PUT /api/tasks/{id}
PATCH /api/tasks/{id}
Content-Type: application/json

{
  "title": "Updated title",
  "status": "Completed",
  "priority": "High"
}
```

#### Delete Task
```bash
DELETE /api/tasks/{id}
```

### User Endpoints (Admin Only)

#### Get Users
```bash
GET /api/users?page=1&per_page=10
```

#### Get User
```bash
GET /api/users/{id}
```

#### Update User
```bash
PUT /api/users/{id}
{
  "name": "New Name",
  "role": "admin"
}
```

#### Delete User
```bash
DELETE /api/users/{id}
```

### Dashboard Endpoints

#### Get Dashboard Statistics
```bash
GET /api/dashboard/stats

# Response
{
  "success": true,
  "data": {
    "total_tasks": 128,
    "pending_tasks": 42,
    "in_progress_tasks": 0,
    "completed_tasks": 86,
    "overdue_tasks": 5,
    "high_priority_tasks": 12,
    "total_users": 24,
    "priority_stats": { ... },
    "status_stats": { ... },
    "recent_tasks": [ ... ]
  }
}
```

#### Get Chart Data
```bash
GET /api/dashboard/chart-data

# Response
{
  "success": true,
  "data": {
    "status_chart": { ... },
    "priority_chart": { ... },
    "weekly_data": { ... }
  }
}
```

## Filtering & Search

### Task Filtering

```bash
# By Status
GET /api/tasks?status=Pending
GET /api/tasks?status=In%20Progress
GET /api/tasks?status=Completed

# By Priority
GET /api/tasks?priority=Low
GET /api/tasks?priority=Medium
GET /api/tasks?priority=High

# By Assignee
GET /api/tasks?assigned_to=2

# By Creator
GET /api/tasks?created_by=1

# By Search
GET /api/tasks?search=authentication

# Combined
GET /api/tasks?status=Pending&priority=High&search=api
```

## Pagination

All list endpoints support pagination:

```bash
GET /api/tasks?page=1&per_page=10

# Parameters:
# page: Page number (default: 1)
# per_page: Items per page (default: 10, max: 100)
```

## Rate Limiting

The API is rate-limited to **100 requests per IP per hour**.

When the limit is exceeded, you'll receive:

```json
{
  "success": false,
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Maximum 100 requests per hour allowed"
}
```

HTTP Status: **429 Too Many Requests**

## Testing

### Run All Tests
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_auth.py -v
```

### Run with Coverage
```bash
pytest --cov=app tests/
```

### Test Categories

- **Authentication** (`test_auth.py`)
  - User registration
  - Login/logout
  - Token validation
  - Password security

- **Task Management** (`test_tasks.py`)
  - CRUD operations
  - Filtering
  - Pagination
  - Search

- **Authorization** (`test_authorization.py`)
  - Role-based access
  - Permission checks
  - Admin privileges

- **API Responses** (`test_api_responses.py`)
  - Response format
  - HTTP status codes
  - Error handling

## Security Features

- ✅ **Password Hashing** - Werkzeug bcrypt
- ✅ **JWT Tokens** - Secure token-based auth
- ✅ **CORS** - Cross-origin resource sharing
- ✅ **SQL Injection Protection** - SQLAlchemy ORM
- ✅ **Input Validation** - Marshmallow schemas
- ✅ **Rate Limiting** - Flask-Limiter
- ✅ **Error Handling** - No sensitive data exposure
- ✅ **Secret Management** - Environment variables

## Deployment

### Vercel Deployment

The application is configured for deployment on Vercel:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# - DATABASE_URL
# - JWT_SECRET_KEY
# - SECRET_KEY
# - FLASK_ENV=production
```

### Environment Variables for Production

```
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET_KEY=use-a-strong-random-key
SECRET_KEY=use-a-strong-random-key
RATELIMIT_STORAGE_URL=redis://localhost:6379
```

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `JWT_SECRET_KEY` and `SECRET_KEY`
- [ ] Configure PostgreSQL with proper backups
- [ ] Enable HTTPS
- [ ] Set up logging and monitoring
- [ ] Configure rate limiting with Redis
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Configure CORS properly
- [ ] Enable security headers
- [ ] Regular security audits

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {}  // Only for validation errors
}
```

### Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `VALIDATION_ERROR` | 422 | Input validation failed |
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Duplicate resource |
| `RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded |
| `INTERNAL_ERROR` | 500 | Server error |

## Database Schema

### Users Table
```sql
id (INTEGER, PK)
name (VARCHAR)
email (VARCHAR, UNIQUE)
password_hash (VARCHAR)
role (VARCHAR: 'user', 'admin')
created_at (DATETIME)
updated_at (DATETIME)
```

### Tasks Table
```sql
id (INTEGER, PK)
title (VARCHAR)
description (TEXT)
status (VARCHAR: 'Pending', 'In Progress', 'Completed')
priority (VARCHAR: 'Low', 'Medium', 'High')
created_by (INTEGER, FK -> users.id)
assigned_to (INTEGER, FK -> users.id)
due_date (DATETIME)
created_at (DATETIME)
updated_at (DATETIME)
```

## Troubleshooting

### Database Connection Error
```
Check DATABASE_URL in .env
Ensure PostgreSQL is running
Verify credentials and database name
```

### JWT Token Expired
```
Log in again to get a new token
Tokens expire after 1 hour by default
```

### Rate Limit Hit
```
Wait 1 hour or use a different IP
Configure Redis for distributed rate limiting
```

### Port Already in Use
```
Change port: python run.py --port 5001
Or kill process: lsof -ti:5000 | xargs kill -9
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Email: support@taskflow.local

## Changelog

### Version 1.0.0 (2024-08-13)
- Initial release
- Complete task management system
- User authentication and authorization
- Admin dashboard
- API documentation
- Rate limiting
- Comprehensive test suite

---

**Made with ❤️ by the TaskFlow Team**
