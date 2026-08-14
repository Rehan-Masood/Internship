"""API response format tests"""
import pytest


class TestResponseFormat:
    def test_success_response_format(self, client, user_token):
        """Test that success responses follow the correct format"""
        response = client.get('/api/auth/me',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 200
        assert 'success' in response.json
        assert 'message' in response.json
        assert 'data' in response.json
        assert response.json['success'] is True

    def test_error_response_format(self, client):
        """Test that error responses follow the correct format"""
        response = client.get('/api/auth/me')
        assert response.status_code == 401
        assert 'success' in response.json
        assert response.json['success'] is False
        assert 'error' in response.json
        assert 'message' in response.json

    def test_pagination_response_format(self, client, user_token):
        """Test that paginated responses include pagination info"""
        response = client.get('/api/tasks',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 200
        assert 'pagination' in response.json
        assert 'page' in response.json['pagination']
        assert 'per_page' in response.json['pagination']
        assert 'total' in response.json['pagination']
        assert 'pages' in response.json['pagination']
        assert 'has_next' in response.json['pagination']
        assert 'has_prev' in response.json['pagination']

    def test_validation_error_response(self, client, user_token):
        """Test validation error response format"""
        response = client.post('/api/tasks',
            headers={'Authorization': f'Bearer {user_token}'},
            json={}
        )
        assert response.status_code == 422
        assert response.json['success'] is False
        assert response.json['error'] == 'VALIDATION_ERROR'

    def test_not_found_response(self, client, user_token):
        """Test 404 response format"""
        response = client.get('/api/tasks/999',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 404
        assert response.json['error'] == 'NOT_FOUND'

    def test_forbidden_response(self, client, user_token):
        """Test 403 response format"""
        response = client.get('/api/users',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 403
        assert response.json['error'] == 'FORBIDDEN'


class TestHTTPStatusCodes:
    def test_201_created(self, client, user_token):
        """Test 201 Created response"""
        response = client.post('/api/tasks',
            headers={'Authorization': f'Bearer {user_token}'},
            json={
                'title': 'New Task',
                'priority': 'High',
                'status': 'Pending'
            }
        )
        assert response.status_code == 201

    def test_200_ok(self, client, user_token):
        """Test 200 OK response"""
        response = client.get('/api/tasks',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 200

    def test_400_bad_request(self, client):
        """Test 400 Bad Request"""
        response = client.post('/api/auth/login', json={})
        assert response.status_code in [400, 422]

    def test_401_unauthorized(self, client):
        """Test 401 Unauthorized"""
        response = client.get('/api/tasks')
        assert response.status_code == 401

    def test_403_forbidden(self, client, user_token):
        """Test 403 Forbidden"""
        response = client.get('/api/users',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 403

    def test_404_not_found(self, client, user_token):
        """Test 404 Not Found"""
        response = client.get('/api/tasks/999',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 404

    def test_409_conflict(self, client, regular_user):
        """Test 409 Conflict"""
        response = client.post('/api/auth/register', json={
            'name': 'User',
            'email': 'user@test.com',
            'password': 'password123',
            'password_confirm': 'password123'
        })
        assert response.status_code == 409

    def test_422_unprocessable_entity(self, client, user_token):
        """Test 422 Unprocessable Entity"""
        response = client.post('/api/tasks',
            headers={'Authorization': f'Bearer {user_token}'},
            json={
                'priority': 'InvalidPriority'
            }
        )
        assert response.status_code == 422
