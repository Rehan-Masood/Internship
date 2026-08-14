// Authentication utilities

class Auth {
    constructor() {
        this.user = null;
        this.isAuthenticated = !!localStorage.getItem('token');
    }

    async login(email, password) {
        try {
            const response = await api.login(email, password);
            if (response.success) {
                api.setToken(response.data.access_token);
                this.user = response.data.user;
                this.isAuthenticated = true;
                localStorage.setItem('user', JSON.stringify(this.user));
                return true;
            }
            return false;
        } catch (error) {
            console.error('Login error:', error);
            return false;
        }
    }

    async register(name, email, password, passwordConfirm) {
        try {
            const response = await api.register(name, email, password, passwordConfirm);
            return response.success;
        } catch (error) {
            console.error('Registration error:', error);
            return false;
        }
    }

    async logout() {
        api.clearToken();
        this.user = null;
        this.isAuthenticated = false;
        localStorage.removeItem('user');
    }

    async loadUser() {
        if (!this.isAuthenticated) return false;

        try {
            const response = await api.getCurrentUser();
            if (response.success) {
                this.user = response.data;
                localStorage.setItem('user', JSON.stringify(this.user));
                return true;
            }
            this.logout();
            return false;
        } catch {
            this.logout();
            return false;
        }
    }

    isAdmin() {
        return this.user && this.user.role === 'admin';
    }

    requireLogin() {
        if (!this.isAuthenticated) {
            window.location.href = '/login';
        }
    }
}

const auth = new Auth();
