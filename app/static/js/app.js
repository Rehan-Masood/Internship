// Main TaskFlow Application

class TaskFlow {
    constructor() {
        this.currentPage = 'dashboard';
        this.tasks = [];
        this.users = [];
        this.taskFilters = {
            page: 1,
            perPage: 10,
            status: null,
            priority: null,
            search: null
        };
        this.charts = {};
        this.init();
    }

    async init() {
        // Determine current page from URL
        const path = window.location.pathname;
        if (path === '/login') {
            this.showLoginPage();
        } else {
            await auth.loadUser();
            if (auth.isAuthenticated) {
                this.showApp();
            } else {
                window.location.href = '/login';
            }
        }
    }

    showLoginPage() {
        const app = document.getElementById('app');
        app.innerHTML = this.getLoginHTML();
        this.attachLoginEvents();
    }

    showRegisterPage() {
        const app = document.getElementById('app');
        app.innerHTML = this.getRegisterHTML();
        this.attachRegisterEvents();
    }

    showApp() {
        const app = document.getElementById('app');
        app.innerHTML = this.getAppHTML();
        this.attachAppEvents();
        this.showPage('dashboard');
    }

    getLoginHTML() {
        return `
            <div class="login-container">
                <div class="login-left">
                    <div class="login-branding">
                        <div class="login-logo">
                            <i class="fas fa-layer-group"></i> TaskFlow
                        </div>
                        <div class="login-tagline">RESTful Task Management API</div>
                    </div>
                    <div class="login-features">
                        <div class="feature">
                            <div class="feature-icon"><i class="fas fa-lock"></i></div>
                            <div class="feature-text"><strong>JWT Auth</strong> - Secure authentication</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon"><i class="fas fa-tachometer-alt"></i></div>
                            <div class="feature-text"><strong>Rate Limited</strong> - 100 req/hour</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon"><i class="fas fa-code"></i></div>
                            <div class="feature-text"><strong>RESTful</strong> - Clean API</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon"><i class="fas fa-book"></i></div>
                            <div class="feature-text"><strong>Swagger UI</strong> - Full docs</div>
                        </div>
                    </div>
                </div>
                <div class="login-right">
                    <div class="login-form">
                        <div class="login-title">Welcome Back</div>
                        <div class="login-subtitle">Sign in to your TaskFlow account</div>
                        
                        <div id="login-alert"></div>
                        
                        <form id="login-form">
                            <div class="form-group">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-input" name="email" required placeholder="your@email.com">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Password</label>
                                <input type="password" class="form-input" name="password" required placeholder="••••••••">
                            </div>
                            <div class="form-remember">
                                <input type="checkbox" class="form-checkbox" name="remember">
                                <span>Remember me</span>
                            </div>
                            <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center;">
                                <i class="fas fa-sign-in-alt"></i> Sign In
                            </button>
                        </form>
                        
                        <div class="login-signup">
                            Don't have an account? <a href="#" id="toggle-register">Sign up</a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getRegisterHTML() {
        return `
            <div class="login-container">
                <div class="login-left">
                    <div class="login-branding">
                        <div class="login-logo">
                            <i class="fas fa-layer-group"></i> TaskFlow
                        </div>
                        <div class="login-tagline">RESTful Task Management API</div>
                    </div>
                    <div class="login-features">
                        <div class="feature">
                            <div class="feature-icon"><i class="fas fa-lock"></i></div>
                            <div class="feature-text"><strong>JWT Auth</strong> - Secure authentication</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon"><i class="fas fa-tachometer-alt"></i></div>
                            <div class="feature-text"><strong>Rate Limited</strong> - 100 req/hour</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon"><i class="fas fa-code"></i></div>
                            <div class="feature-text"><strong>RESTful</strong> - Clean API</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon"><i class="fas fa-book"></i></div>
                            <div class="feature-text"><strong>Swagger UI</strong> - Full docs</div>
                        </div>
                    </div>
                </div>
                <div class="login-right">
                    <div class="login-form">
                        <div class="login-title">Create Account</div>
                        <div class="login-subtitle">Join TaskFlow today</div>
                        
                        <div id="register-alert"></div>
                        
                        <form id="register-form">
                            <div class="form-group">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-input" name="name" required placeholder="Your name">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-input" name="email" required placeholder="your@email.com">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Password</label>
                                <input type="password" class="form-input" name="password" required placeholder="••••••••" minlength="6">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Confirm Password</label>
                                <input type="password" class="form-input" name="password_confirm" required placeholder="••••••••" minlength="6">
                            </div>
                            <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center;">
                                <i class="fas fa-user-plus"></i> Create Account
                            </button>
                        </form>
                        
                        <div class="login-signup">
                            Already have an account? <a href="#" id="toggle-login">Sign in</a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getAppHTML() {
        return `
            <div class="sidebar">
                <div class="sidebar-logo">
                    <i class="fas fa-layer-group"></i> TaskFlow
                </div>
                <ul class="sidebar-menu">
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.showPage('dashboard')">
                            <i class="fas fa-home"></i> Dashboard
                        </a>
                    </li>
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.showPage('tasks')">
                            <i class="fas fa-tasks"></i> My Tasks
                        </a>
                    </li>
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.showPage('create-task')">
                            <i class="fas fa-plus-circle"></i> Create Task
                        </a>
                    </li>
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.showPage('analytics')">
                            <i class="fas fa-chart-line"></i> Analytics
                        </a>
                    </li>
                    ${auth.isAdmin() ? `
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.showPage('users')">
                            <i class="fas fa-users"></i> Users <span class="sidebar-admin-badge">Admin</span>
                        </a>
                    </li>
                    ` : ''}
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.showPage('api-documentation')">
                            <i class="fas fa-book"></i> API Documentation
                        </a>
                    </li>
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.showPage('api-auth')">
                            <i class="fas fa-key"></i> API Authentication
                        </a>
                    </li>
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.showPage('settings')">
                            <i class="fas fa-cog"></i> Settings
                        </a>
                    </li>
                    <li class="sidebar-divider"></li>
                    <li class="sidebar-menu-item">
                        <a class="sidebar-menu-link" onclick="app.logout()">
                            <i class="fas fa-sign-out-alt"></i> Logout
                        </a>
                    </li>
                </ul>
                <div class="sidebar-user">
                    <div class="sidebar-user-avatar"><i class="fas fa-user"></i></div>
                    <div class="sidebar-user-info">
                        <div class="sidebar-user-name">${auth.user.name}</div>
                        <div class="sidebar-user-role">${auth.user.role}</div>
                    </div>
                </div>
            </div>

            <div class="main-content">
                <div class="header">
                    <div class="header-left">
                        <div>
                            <div class="header-title">Dashboard</div>
                            <div class="header-subtitle" id="header-subtitle">Welcome back, ${auth.user.name}! Here's what's happening with your tasks.</div>
                        </div>
                    </div>
                    <div class="header-right">
                        <span class="header-badge"><i class="fas fa-lock"></i> JWT Auth</span>
                        <span class="header-badge"><i class="fas fa-tachometer-alt"></i> Rate Limited</span>
                        <span class="header-badge"><i class="fas fa-code"></i> RESTful</span>
                        <span class="header-badge"><i class="fas fa-book"></i> Swagger UI</span>
                        <div class="notification-bell">
                            <i class="fas fa-bell"></i>
                            <span class="notification-badge">1</span>
                        </div>
                    </div>
                </div>

                <div class="content">
                    ${this.getPagesHTML()}
                </div>
            </div>

            ${this.getModalsHTML()}
        `;
    }

    getPagesHTML() {
        return `
            <div id="dashboard" class="page active">
                ${this.getDashboardHTML()}
            </div>

            <div id="tasks" class="page">
                ${this.getTasksPageHTML()}
            </div>

            <div id="create-task" class="page">
                ${this.getCreateTaskHTML()}
            </div>

            <div id="analytics" class="page">
                ${this.getAnalyticsHTML()}
            </div>

            ${auth.isAdmin() ? `
            <div id="users" class="page">
                ${this.getUsersPageHTML()}
            </div>
            ` : ''}

            <div id="api-documentation" class="page">
                ${this.getAPIDocumentationHTML()}
            </div>

            <div id="api-auth" class="page">
                ${this.getAPIAuthHTML()}
            </div>

            <div id="settings" class="page">
                ${this.getSettingsHTML()}
            </div>
        `;
    }

    getDashboardHTML() {
        return `
            <div class="card">
                <div class="card-header">
                    <div class="card-title">Dashboard</div>
                    <select class="date-selector" id="date-filter">
                        <option value="month">This Month</option>
                        <option value="week">This Week</option>
                        <option value="all">All Time</option>
                    </select>
                </div>
            </div>

            <div class="stats-grid" id="stats-grid">
                <div class="stat-card">
                    <div class="stat-content">
                        <div class="stat-label">Total Tasks</div>
                        <div class="stat-value" id="stat-total-tasks">0</div>
                        <div class="stat-change positive"><i class="fas fa-arrow-up"></i> 12% from last month</div>
                    </div>
                    <div class="stat-icon purple"><i class="fas fa-tasks"></i></div>
                </div>

                <div class="stat-card">
                    <div class="stat-content">
                        <div class="stat-label">Pending Tasks</div>
                        <div class="stat-value" id="stat-pending-tasks">0</div>
                        <div class="stat-change negative"><i class="fas fa-arrow-down"></i> 8% from last month</div>
                    </div>
                    <div class="stat-icon orange"><i class="fas fa-clock"></i></div>
                </div>

                <div class="stat-card">
                    <div class="stat-content">
                        <div class="stat-label">Completed Tasks</div>
                        <div class="stat-value" id="stat-completed-tasks">0</div>
                        <div class="stat-change positive"><i class="fas fa-arrow-up"></i> 16% from last month</div>
                    </div>
                    <div class="stat-icon green"><i class="fas fa-check-circle"></i></div>
                </div>

                <div class="stat-card">
                    <div class="stat-content">
                        <div class="stat-label">Total Users</div>
                        <div class="stat-value" id="stat-total-users">0</div>
                        <div class="stat-change positive"><i class="fas fa-arrow-up"></i> 5% from last month</div>
                    </div>
                    <div class="stat-icon blue"><i class="fas fa-users"></i></div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">Recent Tasks</div>
                        <a class="card-action" onclick="app.showPage('tasks')">View All</a>
                    </div>
                    <div id="recent-tasks-list"></div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <div class="card-title">Tasks Overview</div>
                        <select class="date-selector" id="chart-type">
                            <option value="bar">Bar Chart</option>
                        </select>
                    </div>
                    <div class="chart-container">
                        <canvas id="overview-chart"></canvas>
                    </div>
                </div>
            </div>
        `;
    }

    getTasksPageHTML() {
        return `
            <div class="card">
                <div class="card-header">
                    <div class="card-title">My Tasks</div>
                    <div style="display: flex; gap: 12px;">
                        <input type="text" class="form-input" placeholder="Search tasks..." id="search-input" style="width: 200px; padding: 8px;">
                        <select class="form-select" id="status-filter" style="width: 150px;">
                            <option value="">All Statuses</option>
                            <option value="Pending">Pending</option>
                            <option value="In Progress">In Progress</option>
                            <option value="Completed">Completed</option>
                        </select>
                        <select class="form-select" id="priority-filter" style="width: 150px;">
                            <option value="">All Priorities</option>
                            <option value="Low">Low</option>
                            <option value="Medium">Medium</option>
                            <option value="High">High</option>
                        </select>
                    </div>
                </div>

                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Task</th>
                                <th>Priority</th>
                                <th>Status</th>
                                <th>Assigned To</th>
                                <th>Due Date</th>
                                <th>Created</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="tasks-table-body">
                            <tr><td colspan="7" style="text-align: center; padding: 40px;">Loading tasks...</td></tr>
                        </tbody>
                    </table>
                </div>

                <div id="tasks-pagination" class="pagination"></div>
            </div>
        `;
    }

    getCreateTaskHTML() {
        return `
            <div style="max-width: 600px;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">Create Task</div>
                    </div>

                    <form id="create-task-form">
                        <div class="form-group">
                            <label class="form-label">Title *</label>
                            <input type="text" class="form-input" name="title" required>
                        </div>

                        <div class="form-group">
                            <label class="form-label">Description</label>
                            <textarea class="form-textarea" name="description"></textarea>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                            <div class="form-group">
                                <label class="form-label">Priority</label>
                                <select class="form-select" name="priority" required>
                                    <option value="Low">Low</option>
                                    <option value="Medium" selected>Medium</option>
                                    <option value="High">High</option>
                                </select>
                            </div>

                            <div class="form-group">
                                <label class="form-label">Status</label>
                                <select class="form-select" name="status" required>
                                    <option value="Pending" selected>Pending</option>
                                    <option value="In Progress">In Progress</option>
                                    <option value="Completed">Completed</option>
                                </select>
                            </div>
                        </div>

                        <div class="form-group">
                            <label class="form-label">Due Date</label>
                            <input type="datetime-local" class="form-input" name="due_date">
                        </div>

                        <div class="form-group">
                            <label class="form-label">Assign To</label>
                            <select class="form-select" name="assigned_to" id="assign-user-select">
                                <option value="">Select a user...</option>
                            </select>
                        </div>

                        <div id="form-alert"></div>

                        <div style="display: flex; gap: 12px;">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Create Task
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="app.showPage('tasks')">
                                <i class="fas fa-times"></i> Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        `;
    }

    getAnalyticsHTML() {
        return `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">Tasks by Status</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="status-chart"></canvas>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <div class="card-title">Tasks by Priority</div>
                    </div>
                    <div class="chart-container">
                        <canvas id="priority-chart"></canvas>
                    </div>
                </div>

                <div class="card" style="grid-column: 1 / -1;">
                    <div class="card-header">
                        <div class="card-title">Weekly Task Creation</div>
                    </div>
                    <div class="chart-container" style="height: 350px;">
                        <canvas id="weekly-chart"></canvas>
                    </div>
                </div>
            </div>
        `;
    }

    getUsersPageHTML() {
        return `
            <div class="card">
                <div class="card-header">
                    <div class="card-title">Users Management</div>
                </div>

                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>User</th>
                                <th>Email</th>
                                <th>Role</th>
                                <th>Joined</th>
                                <th>Tasks</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="users-table-body">
                            <tr><td colspan="6" style="text-align: center; padding: 40px;">Loading users...</td></tr>
                        </tbody>
                    </table>
                </div>

                <div id="users-pagination" class="pagination"></div>
            </div>
        `;
    }

    getAPIDocumentationHTML() {
        return `
            <div style="max-width: 900px;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">API Documentation</div>
                        <a class="btn btn-primary btn-sm" href="/api/docs" target="_blank">
                            <i class="fas fa-book"></i> Open Swagger UI
                        </a>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">Base URL</h3>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block;">
                            ${window.location.origin}/api
                        </code>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">Authentication</h3>
                        <p>All endpoints (except /auth/register and /auth/login) require Bearer token authentication.</p>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block;">
                            Authorization: Bearer YOUR_JWT_TOKEN
                        </code>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">Rate Limiting</h3>
                        <p>API is rate limited to 100 requests per hour per IP address.</p>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">Endpoints</h3>
                        <div style="background: var(--primary-dark); border-radius: 6px; padding: 16px; max-height: 400px; overflow-y: auto;">
                            <table class="table" style="margin-bottom: 0;">
                                <thead>
                                    <tr>
                                        <th>Method</th>
                                        <th>Endpoint</th>
                                        <th>Description</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(59, 130, 246, 0.2); color: var(--accent-blue);">POST</span></td>
                                        <td>/auth/register</td>
                                        <td>Register new user</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(59, 130, 246, 0.2); color: var(--accent-blue);">POST</span></td>
                                        <td>/auth/login</td>
                                        <td>Login user</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(59, 130, 246, 0.2); color: var(--accent-blue);">GET</span></td>
                                        <td>/auth/me</td>
                                        <td>Get current user</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(59, 130, 246, 0.2); color: var(--accent-blue);">GET</span></td>
                                        <td>/tasks</td>
                                        <td>Get tasks with filtering & pagination</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(59, 130, 246, 0.2); color: var(--accent-blue);">GET</span></td>
                                        <td>/tasks/{id}</td>
                                        <td>Get single task</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(34, 197, 94, 0.2); color: var(--success-color);">POST</span></td>
                                        <td>/tasks</td>
                                        <td>Create task</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(245, 158, 11, 0.2); color: var(--accent-orange);">PUT</span></td>
                                        <td>/tasks/{id}</td>
                                        <td>Update task</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(239, 68, 68, 0.2); color: var(--error-color);">DELETE</span></td>
                                        <td>/tasks/{id}</td>
                                        <td>Delete task</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(59, 130, 246, 0.2); color: var(--accent-blue);">GET</span></td>
                                        <td>/users</td>
                                        <td>Get users (Admin)</td>
                                    </tr>
                                    <tr>
                                        <td><span class="badge" style="background: rgba(59, 130, 246, 0.2); color: var(--accent-blue);">GET</span></td>
                                        <td>/dashboard/stats</td>
                                        <td>Get dashboard stats</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getAPIAuthHTML() {
        return `
            <div style="max-width: 900px;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">API Authentication</div>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">JWT Bearer Token</h3>
                        <p>TaskFlow uses JWT (JSON Web Tokens) for API authentication.</p>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">1. Register</h3>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block; margin-bottom: 12px;">
                            POST /api/auth/register
                        </code>
                        <p style="margin-bottom: 12px;">Request body:</p>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block; font-size: 12px;">
                            {
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "password_confirm": "securepassword"
}
                        </code>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">2. Login</h3>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block; margin-bottom: 12px;">
                            POST /api/auth/login
                        </code>
                        <p style="margin-bottom: 12px;">Request body:</p>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block; font-size: 12px;">
                            {
  "email": "john@example.com",
  "password": "securepassword"
}
                        </code>
                        <p style="margin-top: 12px; margin-bottom: 12px;">Response:</p>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block; font-size: 12px;">
                            {
  "success": true,
  "message": "Login successful",
  "data": {
    "user": { ... },
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
                        </code>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">3. Use Token</h3>
                        <p>Include the token in the Authorization header for all subsequent requests:</p>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block;">
                            Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
                        </code>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">4. Get Current User</h3>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block; margin-bottom: 12px;">
                            GET /api/auth/me
                        </code>
                        <p style="margin-bottom: 12px;">Headers:</p>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block;">
                            Authorization: Bearer YOUR_TOKEN
                        </code>
                    </div>

                    <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid var(--accent-purple); border-radius: 8px; padding: 16px;">
                        <strong style="color: var(--accent-purple);">💡 Tip:</strong> You can test all API endpoints directly from the 
                        <a href="/api/docs" target="_blank" style="color: var(--accent-blue); text-decoration: underline;">Swagger UI</a>
                    </div>
                </div>
            </div>
        `;
    }

    getSettingsHTML() {
        return `
            <div style="max-width: 600px;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">Settings</div>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <h3 style="margin-bottom: 12px;">User Profile</h3>
                        <div class="form-group">
                            <label class="form-label">Name</label>
                            <div style="padding: 12px; background: var(--primary-dark); border-radius: 6px;">${auth.user.name}</div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Email</label>
                            <div style="padding: 12px; background: var(--primary-dark); border-radius: 6px;">${auth.user.email}</div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Role</label>
                            <div style="padding: 12px; background: var(--primary-dark); border-radius: 6px;">
                                <span class="badge" style="background: rgba(139, 92, 246, 0.2); color: var(--accent-purple);">
                                    ${auth.user.role.toUpperCase()}
                                </span>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Member Since</label>
                            <div style="padding: 12px; background: var(--primary-dark); border-radius: 6px;">
                                ${new Date(auth.user.created_at).toLocaleDateString()}
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid var(--accent-purple); border-radius: 8px; padding: 16px;">
                        <h4 style="margin-bottom: 8px;">API Token</h4>
                        <p style="font-size: 12px; margin-bottom: 12px;">Your current authentication token:</p>
                        <code style="background: var(--primary-dark); padding: 12px; border-radius: 6px; display: block; font-size: 11px; word-break: break-all;">
                            ${api.token || 'No token'}
                        </code>
                    </div>
                </div>
            </div>
        `;
    }

    getModalsHTML() {
        return `
            <div id="delete-modal" class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2 class="modal-title">Delete Task?</h2>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to permanently delete this task? This action cannot be undone.</p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="app.closeModal('delete-modal')">Cancel</button>
                        <button class="btn btn-danger" onclick="app.confirmDelete()">Delete Task</button>
                    </div>
                </div>
            </div>

            <div id="edit-modal" class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2 class="modal-title">Edit Task</h2>
                    </div>
                    <div class="modal-body">
                        <form id="edit-task-form">
                            <div class="form-group">
                                <label class="form-label">Title</label>
                                <input type="text" class="form-input" name="title">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Status</label>
                                <select class="form-select" name="status">
                                    <option value="Pending">Pending</option>
                                    <option value="In Progress">In Progress</option>
                                    <option value="Completed">Completed</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Priority</label>
                                <select class="form-select" name="priority">
                                    <option value="Low">Low</option>
                                    <option value="Medium">Medium</option>
                                    <option value="High">High</option>
                                </select>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="app.closeModal('edit-modal')">Cancel</button>
                        <button class="btn btn-primary" onclick="app.submitEditTask()">Save Changes</button>
                    </div>
                </div>
            </div>
        `;
    }

    attachLoginEvents() {
        const form = document.getElementById('login-form');
        const alertDiv = document.getElementById('login-alert');
        const toggleRegister = document.getElementById('toggle-register');

        // Handle toggle to register
        if (toggleRegister) {
            toggleRegister.addEventListener('click', (e) => {
                e.preventDefault();
                this.showRegisterPage();
            });
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = form.email.value;
            const password = form.password.value;

            try {
                const success = await auth.login(email, password);
                if (success) {
                    this.showApp();
                } else {
                    alertDiv.innerHTML = `
                        <div class="alert alert-error">
                            <i class="fas fa-exclamation-circle"></i>
                            <div class="alert-content">Invalid email or password</div>
                        </div>
                    `;
                }
            } catch (error) {
                alertDiv.innerHTML = `
                    <div class="alert alert-error">
                        <i class="fas fa-exclamation-circle"></i>
                        <div class="alert-content">${error.message}</div>
                    </div>
                `;
            }
        });
    }

    attachRegisterEvents() {
        const form = document.getElementById('register-form');
        const alertDiv = document.getElementById('register-alert');
        const toggleLogin = document.getElementById('toggle-login');

        // Handle toggle back to login
        if (toggleLogin) {
            toggleLogin.addEventListener('click', (e) => {
                e.preventDefault();
                this.showLoginPage();
            });
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = form.name.value;
            const email = form.email.value;
            const password = form.password.value;
            const passwordConfirm = form.password_confirm.value;

            // Client-side validation
            if (password !== passwordConfirm) {
                alertDiv.innerHTML = `
                    <div class="alert alert-error">
                        <i class="fas fa-exclamation-circle"></i>
                        <div class="alert-content">Passwords do not match</div>
                    </div>
                `;
                return;
            }

            if (password.length < 6) {
                alertDiv.innerHTML = `
                    <div class="alert alert-error">
                        <i class="fas fa-exclamation-circle"></i>
                        <div class="alert-content">Password must be at least 6 characters</div>
                    </div>
                `;
                return;
            }

            try {
                const success = await auth.register(name, email, password, passwordConfirm);
                if (success) {
                    alertDiv.innerHTML = `
                        <div class="alert alert-success">
                            <i class="fas fa-check-circle"></i>
                            <div class="alert-content">Account created successfully! Redirecting to login...</div>
                        </div>
                    `;
                    setTimeout(() => {
                        this.showLoginPage();
                    }, 2000);
                } else {
                    alertDiv.innerHTML = `
                        <div class="alert alert-error">
                            <i class="fas fa-exclamation-circle"></i>
                            <div class="alert-content">Registration failed. Please try again.</div>
                        </div>
                    `;
                }
            } catch (error) {
                // Parse error message from API response
                let errorMsg = error.message;
                if (error.message.includes('409')) {
                    errorMsg = 'Email already registered';
                } else if (error.message.includes('422') || error.message.includes('Validation')) {
                    errorMsg = error.message.includes('match') ? 'Passwords do not match' : 'Validation error. Please check your input.';
                }
                
                alertDiv.innerHTML = `
                    <div class="alert alert-error">
                        <i class="fas fa-exclamation-circle"></i>
                        <div class="alert-content">${errorMsg}</div>
                    </div>
                `;
            }
        });
    }

    attachAppEvents() {
        // Create Task Form
        const createTaskForm = document.getElementById('create-task-form');
        if (createTaskForm) {
            createTaskForm.addEventListener('submit', (e) => this.handleCreateTask(e));
        }

        // Search and Filter
        const searchInput = document.getElementById('search-input');
        const statusFilter = document.getElementById('status-filter');
        const priorityFilter = document.getElementById('priority-filter');

        if (searchInput) {
            searchInput.addEventListener('input', () => {
                this.taskFilters.page = 1;
                this.taskFilters.search = searchInput.value;
                this.loadTasks();
            });
        }

        if (statusFilter) {
            statusFilter.addEventListener('change', () => {
                this.taskFilters.page = 1;
                this.taskFilters.status = statusFilter.value;
                this.loadTasks();
            });
        }

        if (priorityFilter) {
            priorityFilter.addEventListener('change', () => {
                this.taskFilters.page = 1;
                this.taskFilters.priority = priorityFilter.value;
                this.loadTasks();
            });
        }
    }

    async showPage(pageName) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));

        // Show selected page
        const page = document.getElementById(pageName);
        if (page) {
            page.classList.add('active');
        }

        // Update sidebar active link
        document.querySelectorAll('.sidebar-menu-link').forEach(link => {
            link.classList.remove('active');
        });

        // Load page-specific content
        switch (pageName) {
            case 'dashboard':
                await this.loadDashboard();
                break;
            case 'tasks':
                await this.loadTasks();
                break;
            case 'create-task':
                await this.loadCreateTaskForm();
                break;
            case 'analytics':
                await this.loadAnalytics();
                break;
            case 'users':
                await this.loadUsers();
                break;
        }
    }

    async loadDashboard() {
        try {
            const stats = await api.getDashboardStats();
            const chartData = await api.getChartData();

            if (stats.success) {
                document.getElementById('stat-total-tasks').textContent = stats.data.total_tasks;
                document.getElementById('stat-pending-tasks').textContent = stats.data.pending_tasks;
                document.getElementById('stat-completed-tasks').textContent = stats.data.completed_tasks;
                if (stats.data.total_users !== undefined) {
                    document.getElementById('stat-total-users').textContent = stats.data.total_users;
                }

                // Recent tasks
                const recentTasksList = document.getElementById('recent-tasks-list');
                if (stats.data.recent_tasks.length > 0) {
                    recentTasksList.innerHTML = `
                        <div class="table-container">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Task</th>
                                        <th>Status</th>
                                        <th>Priority</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${stats.data.recent_tasks.map(task => `
                                        <tr>
                                            <td><strong>${task.title}</strong></td>
                                            <td><span class="badge badge-${task.status.toLowerCase().replace(' ', '-')}">${task.status}</span></td>
                                            <td><span class="badge badge-${task.priority.toLowerCase()}">${task.priority}</span></td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    `;
                } else {
                    recentTasksList.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 20px;">No tasks yet</p>';
                }
            }

            // Chart
            if (chartData.success) {
                this.createChart('overview-chart', chartData.data.status_chart, 'bar');
            }
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }

    async loadTasks() {
        try {
            const response = await api.getTasks(this.taskFilters);

            if (response.success) {
                const tbody = document.getElementById('tasks-table-body');
                if (response.data.length > 0) {
                    tbody.innerHTML = response.data.map(task => `
                        <tr>
                            <td><strong>${task.title}</strong></td>
                            <td><span class="badge badge-${task.priority.toLowerCase()}">${task.priority}</span></td>
                            <td><span class="badge badge-${task.status.toLowerCase().replace(' ', '-')}">${task.status}</span></td>
                            <td>${task.assignee ? task.assignee.name : '-'}</td>
                            <td>${task.due_date ? new Date(task.due_date).toLocaleDateString() : '-'}</td>
                            <td>${new Date(task.created_at).toLocaleDateString()}</td>
                            <td>
                                <button class="btn btn-sm btn-secondary" onclick="app.editTask(${task.id})"><i class="fas fa-edit"></i></button>
                                <button class="btn btn-sm btn-danger" onclick="app.deleteTask(${task.id})"><i class="fas fa-trash"></i></button>
                            </td>
                        </tr>
                    `).join('');
                } else {
                    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 40px;">No tasks found</td></tr>';
                }

                // Pagination
                this.renderPagination('tasks-pagination', response.pagination);
            }
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    }

    async loadCreateTaskForm() {
        // Clear any previous success/error messages from previous form submission
        const alertDiv = document.getElementById('form-alert');
        if (alertDiv) {
            alertDiv.innerHTML = '';
        }
        
        try {
            const users = await api.getAssignableUsers(1, 100);
            if (users.success) {
                const select = document.getElementById('assign-user-select');
                select.innerHTML = `
                    <option value="">Select a user...</option>
                    ${users.data.map(user => `<option value="${user.id}">${user.name}</option>`).join('')}
                `;
            }
        } catch (error) {
            console.error('Error loading users:', error);
        }
    }

    async handleCreateTask(e) {
        e.preventDefault();
        const form = e.target;
        const alertDiv = document.getElementById('form-alert');

        try {
            const data = {
                title: form.title.value,
                description: form.description.value,
                priority: form.priority.value,
                status: form.status.value,
                assigned_to: form.assigned_to.value ? parseInt(form.assigned_to.value) : null,
                due_date: form.due_date.value ? new Date(form.due_date.value).toISOString() : null
            };

            const response = await api.createTask(data);

            if (response.success) {
                alertDiv.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i>
                        <div class="alert-content">Task created successfully!</div>
                    </div>
                `;
                form.reset();
                setTimeout(() => this.showPage('tasks'), 1500);
            }
        } catch (error) {
            alertDiv.innerHTML = `
                <div class="alert alert-error">
                    <i class="fas fa-exclamation-circle"></i>
                    <div class="alert-content">${error.message}</div>
                </div>
            `;
        }
    }

    async loadAnalytics() {
        try {
            const chartData = await api.getChartData();

            if (chartData.success) {
                this.createChart('status-chart', chartData.data.status_chart, 'doughnut');
                this.createChart('priority-chart', chartData.data.priority_chart, 'doughnut');
                this.createChart('weekly-chart', chartData.data.weekly_data, 'line');
            }
        } catch (error) {
            console.error('Error loading analytics:', error);
        }
    }

    async loadUsers() {
        try {
            const response = await api.getUsers(1, 50);

            if (response.success) {
                const tbody = document.getElementById('users-table-body');
                if (response.data.length > 0) {
                    tbody.innerHTML = response.data.map(user => `
                        <tr>
                            <td><strong>${user.name}</strong></td>
                            <td>${user.email}</td>
                            <td><span class="badge badge-${user.role}">${user.role.toUpperCase()}</span></td>
                            <td>${new Date(user.created_at).toLocaleDateString()}</td>
                            <td>-</td>
                            <td>
                                <button class="btn btn-sm btn-secondary" onclick="app.editUser(${user.id})"><i class="fas fa-edit"></i></button>
                                <button class="btn btn-sm btn-danger" onclick="app.deleteUserConfirm(${user.id})"><i class="fas fa-trash"></i></button>
                            </td>
                        </tr>
                    `).join('');
                } else {
                    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 40px;">No users found</td></tr>';
                }
            }
        } catch (error) {
            console.error('Error loading users:', error);
        }
    }

    createChart(canvasId, data, type = 'bar') {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        // Destroy existing chart if it exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        const ctx = canvas.getContext('2d');
        const labels = Object.keys(data);
        const values = Object.values(data);

        const chartConfig = {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: 'Count',
                    data: values,
                    backgroundColor: [
                        'rgba(139, 92, 246, 0.8)',
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ],
                    borderColor: [
                        'rgba(139, 92, 246, 1)',
                        'rgba(59, 130, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#a0aec0'
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            color: '#a0aec0'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#a0aec0'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        };

        this.charts[canvasId] = new Chart(ctx, chartConfig);
    }

    renderPagination(containerId, pagination) {
        const container = document.getElementById(containerId);
        if (!container) return;

        let html = '';

        // Previous button
        if (pagination.has_prev) {
            html += `<button class="pagination-btn" onclick="app.goToPage(${pagination.page - 1})">← Previous</button>`;
        }

        // Page numbers
        for (let i = 1; i <= pagination.pages; i++) {
            if (i === pagination.page) {
                html += `<button class="pagination-btn active">${i}</button>`;
            } else {
                html += `<button class="pagination-btn" onclick="app.goToPage(${i})">${i}</button>`;
            }
        }

        // Next button
        if (pagination.has_next) {
            html += `<button class="pagination-btn" onclick="app.goToPage(${pagination.page + 1})">Next →</button>`;
        }

        container.innerHTML = html;
    }

    goToPage(page) {
        this.taskFilters.page = page;
        this.loadTasks();
        document.querySelector('.table-container').scrollIntoView({ behavior: 'smooth' });
    }

    editTask(taskId) {
        this.editingTaskId = taskId;
        this.openModal('edit-modal');
    }

    async submitEditTask() {
        const form = document.getElementById('edit-task-form');
        const data = {
            title: form.title.value,
            status: form.status.value,
            priority: form.priority.value
        };

        try {
            const response = await api.updateTask(this.editingTaskId, data);
            if (response.success) {
                this.closeModal('edit-modal');
                this.loadTasks();
                this.showAlert('Task updated successfully', 'success');
            }
        } catch (error) {
            this.showAlert(error.message, 'error');
        }
    }

    deleteTask(taskId) {
        this.deletingTaskId = taskId;
        this.openModal('delete-modal');
    }

    async confirmDelete() {
        try {
            const response = await api.deleteTask(this.deletingTaskId);
            if (response.success) {
                this.closeModal('delete-modal');
                this.loadTasks();
                this.showAlert('Task deleted successfully', 'success');
            }
        } catch (error) {
            this.showAlert(error.message, 'error');
        }
    }

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
        }
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
        }
    }

    showAlert(message, type = 'info') {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <div class="alert-content">${message}</div>
        `;

        const container = document.querySelector('.content');
        if (container) {
            container.insertBefore(alert, container.firstChild);
            setTimeout(() => alert.remove(), 5000);
        }
    }

    async logout() {
        await auth.logout();
        window.location.href = '/login';
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TaskFlow();
});
