/* ═══ BusTrack Shared Utilities ═══ */

/* ── Toast Notifications ── */
function ensureToastContainer() {
    let c = document.getElementById('toast-container');
    if (!c) {
        c = document.createElement('div');
        c.id = 'toast-container';
        document.body.appendChild(c);
    }
    return c;
}

function showToast(message, type = 'success') {
    const container = ensureToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <span class="toast-msg">${message}</span>
        <div class="toast-progress"></div>
    `;
    container.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('toast-show'));
    setTimeout(() => {
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hide');
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}

/* ── Loading Spinner ── */
function showSpinner() {
    let overlay = document.getElementById('spinner-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'spinner-overlay';
        overlay.innerHTML = '<div class="spinner"></div>';
        document.body.appendChild(overlay);
    }
    overlay.classList.add('active');
}

function hideSpinner() {
    const overlay = document.getElementById('spinner-overlay');
    if (overlay) overlay.classList.remove('active');
}

/* ── API Fetch Wrapper ── */
async function apiFetch(endpoint, options = {}) {
    const token = getToken();
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
    
    const res = await fetch(url, { ...options, headers });
    
    if (res.status === 401) {
        removeToken();
        window.location.href = '/frontend/index.html';
        return null;
    }
    
    const data = await res.json();
    
    if (!res.ok) {
        throw new Error(data.detail || data.msg || 'Something went wrong');
    }
    return data;
}

/* ── Button Loading State ── */
function setButtonLoading(btn, loading) {
    if (loading) {
        btn.disabled = true;
        btn.dataset.originalText = btn.innerHTML;
        btn.innerHTML = '<span class="btn-spinner"></span> Loading...';
        btn.classList.add('btn-loading');
    } else {
        btn.disabled = false;
        btn.innerHTML = btn.dataset.originalText || btn.innerHTML;
        btn.classList.remove('btn-loading');
    }
}

/* ── Render Navbar ── */
function renderNavbar(containerId) {
    const username = getUsername();
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `
        <nav class="navbar">
            <a href="/frontend/index.html" class="nav-brand">
                <span class="nav-logo">🚌</span>
                <span class="nav-title">BusTrack</span>
            </a>
            <div class="nav-right">
                <span class="nav-user"><span class="nav-user-icon">👤</span> ${username}</span>
                <button class="btn btn-sm btn-outline" onclick="logout()">Logout</button>
            </div>
        </nav>
    `;
}

/* ── Render Admin Sidebar ── */
function renderAdminSidebar(activeId) {
    const sidebar = document.getElementById('admin-sidebar');
    if (!sidebar) return;
    const links = [
        { id: 'dashboard', label: 'Dashboard', icon: '📊', href: '/frontend/admin/dashboard.html' },
        { id: 'buses', label: 'Buses', icon: '🚌', href: '/frontend/admin/buses.html' },
        { id: 'routes', label: 'Routes', icon: '🗺️', href: '/frontend/admin/routes.html' },
        { id: 'schedules', label: 'Schedules', icon: '📅', href: '/frontend/admin/schedules.html' },
        { id: 'users', label: 'Users', icon: '👥', href: '/frontend/admin/users.html' },
    ];
    sidebar.innerHTML = `
        <div class="sidebar-header">
            <span class="nav-logo">🚌</span>
            <span class="nav-title">BusTrack</span>
            <span class="sidebar-badge">Admin</span>
        </div>
        <ul class="sidebar-nav">
            ${links.map(l => `
                <li>
                    <a href="${l.href}" class="sidebar-link ${l.id === activeId ? 'active' : ''}">
                        <span class="sidebar-icon">${l.icon}</span>
                        <span>${l.label}</span>
                    </a>
                </li>
            `).join('')}
        </ul>
        <div class="sidebar-footer">
            <button class="btn btn-outline btn-block" onclick="logout()">🚪 Logout</button>
        </div>
    `;
}

function toggleSidebar() {
    const sidebar = document.getElementById('admin-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    sidebar.classList.toggle('open');
    if (overlay) overlay.classList.toggle('active');
}

/* ── Empty State ── */
function renderEmptyState(containerId, message = 'No data found') {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">
                <div class="empty-bus">🚌</div>
                <div class="empty-road"></div>
            </div>
            <p class="empty-text">${message}</p>
        </div>
    `;
}

/* ── Form Validation ── */
function validateField(input, rule) {
    const value = input.value.trim();
    let errorEl = input.parentElement.querySelector('.field-error');
    if (!errorEl) {
        errorEl = document.createElement('span');
        errorEl.className = 'field-error';
        input.parentElement.appendChild(errorEl);
    }
    let error = '';
    if (rule.required && !value) error = `${rule.label || 'Field'} is required`;
    else if (rule.minLength && value.length < rule.minLength) error = `Min ${rule.minLength} characters`;
    else if (rule.email && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) error = 'Invalid email';
    
    if (error) {
        errorEl.textContent = error;
        input.classList.add('input-error');
        return false;
    } else {
        errorEl.textContent = '';
        input.classList.remove('input-error');
        return true;
    }
}

/* ── Format datetime for display ── */
function formatDateTime(dateStr) {
    if (!dateStr) return '—';
    const d = new Date(dateStr);
    return d.toLocaleString('en-IN', {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit', hour12: true
    });
}
