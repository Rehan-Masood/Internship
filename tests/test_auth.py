"""Authentication tests"""
import pytest


class TestRegister:
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register', json={
            'name': 'New User',
            'email': 'new@test.com',
            'password': 'password123',
            'password_confirm': 'password123'
        })
        assert response.status_code == 201
        assert response.json['success'] is True
        assert response.json['data']['email'] == 'new@test.com'

    def test_register_duplicate_email(self, client, regular_user):
        """Test registration with duplicate email"""
        response = client.post('/api/auth/register', json={
            'name': 'Another User',
            'email': 'user@test.com',
            'password': 'password123',
            'password_confirm': 'password123'
        })
        assert response.status_code == 409
        assert response.json['success'] is False
        assert 'already registered' in response.json['message']

    def test_register_password_mismatch(self, client):
        """Test registration with mismatched passwords"""
        response = client.post('/api/auth/register', json={
            'name': 'User',
            'email': 'user@test.com',
            'password': 'password123',
            'password_confirm': 'different123'
        })
        assert response.status_code == 422
        assert response.json['success'] is False

    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post('/api/auth/register', json={
            'name': 'User',
            'email': 'not-an-email',
            'password': 'password123',
            'password_confirm': 'password123'
        })
        assert response.status_code == 422

    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/auth/register', json={
            'name': 'User',
            'email': 'user@test.com',
            'password': 'short',
            'password_confirm': 'short'
        })
        assert response.status_code == 422


class TestLogin:
    def test_login_success(self, client, regular_user):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'email': 'user@test.com',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert response.json['success'] is True
        assert 'access_token' in response.json['data']

    def test_login_wrong_password(self, client, regular_user):
        """Test login with wrong password"""
        response = client.post('/api/auth/login', json={
            'email': 'user@test.com',
            'password': 'wrong_password'
        })
        assert response.status_code == 401
        assert response.json['success'] is False

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@test.com',
            'password': 'password123'
        })
        assert response.status_code == 401
        assert response.json['success'] is False

    def test_login_invalid_email(self, client):
        """Test login with invalid email format"""
        response = client.post('/api/auth/login', json={
            'email': 'not-an-email',
            'password': 'password123'
        })
        assert response.status_code == 422


class TestGetCurrentUser:
    def test_get_current_user_success(self, client, user_token):
        """Test getting current user with valid token"""
        response = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {user_token}'
        })
        assert response.status_code == 200
        assert response.json['success'] is True
        assert response.json['data']['email'] == 'user@test.com'

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get('/api/auth/me')
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get('/api/auth/me', headers={
            'Authorization': 'Bearer invalid_token_here'
        })
        assert response.status_code == 401
