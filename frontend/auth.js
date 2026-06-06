/* ═══ BusTrack Auth Helpers ═══ */

function getToken() {
    return localStorage.getItem('bustrack_token');
}

function setToken(token) {
    localStorage.setItem('bustrack_token', token);
}

function removeToken() {
    localStorage.removeItem('bustrack_token');
}

function decodeToken() {
    const token = getToken();
    if (!token) return null;
    try {
        const payload = token.split('.')[1];
        const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
        return JSON.parse(decoded);
    } catch (e) {
        return null;
    }
}

function getUsername() {
    const payload = decodeToken();
    return payload ? payload.username : 'User';
}

function getUserRole() {
    const payload = decodeToken();
    return payload ? payload.role : null;
}

function redirectByRole(role) {
    const basePath = window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/') + '/'.length) || '/';
    switch (role) {
        case 'admin':
            window.location.href = '/admin/dashboard.html';
            break;
        case 'driver':
            window.location.href = '/driver/dashboard.html';
            break;
        case 'passenger':
            window.location.href = '/passenger/dashboard.html';
            break;
        default:
            window.location.href = '/index.html';
    }
}

function guardPage(allowedRoles) {
    const token = getToken();
    if (!token) {
        window.location.href = '/index.html';
        return false;
    }
    const payload = decodeToken();
    if (!payload || !allowedRoles.includes(payload.role)) {
        window.location.href = '/index.html';
        return false;
    }
    return true;
}

function logout() {
    removeToken();
    window.location.href = '/index.html';
}
