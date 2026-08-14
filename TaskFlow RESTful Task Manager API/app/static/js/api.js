// API client for TaskFlow

class API {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('token');
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        const token = this.token || localStorage.getItem('token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            let data;
            try {
                data = await response.json();
            } catch {
                data = { success: false, message: 'Invalid response' };
            }

            if (!response.ok) {
                throw new Error(data.message || `HTTP ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('token');
    }

    // Auth endpoints
    async register(name, email, password, passwordConfirm) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({
                name,
                email,
                password,
                password_confirm: passwordConfirm
            })
        });
    }

    async login(email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    }

    async getCurrentUser() {
        return this.request('/auth/me', { method: 'GET' });
    }

    // Task endpoints
    async getTasks(options = {}) {
        const params = new URLSearchParams();
        if (options.page) params.append('page', options.page);
        if (options.perPage) params.append('per_page', options.perPage);
        if (options.status) params.append('status', options.status);
        if (options.priority) params.append('priority', options.priority);
        if (options.search) params.append('search', options.search);
        if (options.assignedTo) params.append('assigned_to', options.assignedTo);
        if (options.createdBy) params.append('created_by', options.createdBy);

        const url = params.toString() ? `/tasks?${params.toString()}` : '/tasks';
        return this.request(url, { method: 'GET' });
    }

    async getTask(id) {
        return this.request(`/tasks/${id}`, { method: 'GET' });
    }

    async createTask(data) {
        return this.request('/tasks', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateTask(id, data) {
        return this.request(`/tasks/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteTask(id) {
        return this.request(`/tasks/${id}`, { method: 'DELETE' });
    }

    // User endpoints
    async getUsers(page = 1, perPage = 10) {
        return this.request(`/users?page=${page}&per_page=${perPage}`, { method: 'GET' });
    }

    async getAssignableUsers(page = 1, perPage = 100) {
        return this.request(`/users/assignable/list?page=${page}&per_page=${perPage}`, { method: 'GET' });
    }

    async getUser(id) {
        return this.request(`/users/${id}`, { method: 'GET' });
    }

    async updateUser(id, data) {
        return this.request(`/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteUser(id) {
        return this.request(`/users/${id}`, { method: 'DELETE' });
    }

    // Dashboard endpoints
    async getDashboardStats() {
        return this.request('/dashboard/stats', { method: 'GET' });
    }

    async getChartData() {
        return this.request('/dashboard/chart-data', { method: 'GET' });
    }
}

const api = new API();
