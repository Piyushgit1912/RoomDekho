/* ===== RoomDekho API Client ===== */
const API_BASE = 'http://localhost:8000/api';

const api = {
  token: localStorage.getItem('rd_token'),
  user: JSON.parse(localStorage.getItem('rd_user') || 'null'),

  headers(extra = {}) {
    const h = { 'Content-Type': 'application/json', ...extra };
    if (this.token) h['Authorization'] = `Token ${this.token}`;
    return h;
  },

  async request(method, endpoint, data = null, isFormData = false) {
    const opts = { method, headers: isFormData ? { Authorization: `Token ${this.token}` } : this.headers() };
    if (data) opts.body = isFormData ? data : JSON.stringify(data);
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, opts);
      const json = await res.json();
      if (!res.ok) throw json;
      return json;
    } catch(err) {
      throw err;
    }
  },

  get: (e) => api.request('GET', e),
  post: (e, d) => api.request('POST', e, d),
  put: (e, d) => api.request('PUT', e, d),
  patch: (e, d) => api.request('PATCH', e, d),
  delete: (e) => api.request('DELETE', e),
  upload: (e, fd) => api.request('POST', e, fd, true),

  setAuth(token, user) {
    this.token = token;
    this.user = user;
    localStorage.setItem('rd_token', token);
    localStorage.setItem('rd_user', JSON.stringify(user));
  },

  clearAuth() {
    this.token = null;
    this.user = null;
    localStorage.removeItem('rd_token');
    localStorage.removeItem('rd_user');
  },

  isLoggedIn() { return !!this.token; },
  isOwner() { return this.user?.user_type === 'owner'; },
  isAdmin() { return this.user?.user_type === 'admin' || this.user?.is_staff; }
};

/* ===== Toast Notifications ===== */
function toast(msg, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const el = document.createElement('div');
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${icons[type] || 'ℹ'}</span><span>${msg}</span>`;
  container.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; el.style.transform = 'translateX(40px)'; el.style.transition = 'all 0.3s'; setTimeout(() => el.remove(), 300); }, 3500);
}

/* ===== Navbar ===== */
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) navbar?.classList.add('scrolled');
    else navbar?.classList.remove('scrolled');
  });

  hamburger?.addEventListener('click', () => navLinks?.classList.toggle('open'));

  // Auth state in navbar
  const navActions = document.querySelector('.nav-actions');
  if (navActions && api.isLoggedIn()) {
    const isOwner = api.isOwner();
    const dashboardLink = `<a href="dashboard.html" class="btn btn-ghost nav-btn-desktop">Dashboard</a>`;
    const addPropertyLink = isOwner ? `<a href="add-property.html" class="btn btn-primary nav-btn-desktop">+ List Property</a>` : `<a href="#" class="btn btn-outline nav-btn-desktop" onclick="event.preventDefault(); toast('Only Property Owners can add listings. Please login with an Owner account.', 'error')">+ List Property</a>`;
    
    navActions.innerHTML = `
      ${addPropertyLink}
      ${dashboardLink}
      <div class="user-menu" id="userMenu">
        <div class="user-menu-trigger" onclick="toggleUserMenu(event)">
          <div style="width:36px;height:36px;border-radius:50%;background:var(--brand-light);color:var(--brand);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.85rem">
            ${(api.user?.name || 'U')[0].toUpperCase()}
          </div>
          <span style="font-size:0.9rem;font-weight:500;color:var(--dark)">${api.user?.name?.split(' ')[0]}</span>
          <span style="font-size:0.6rem;color:var(--mid);margin-left:2px">▼</span>
        </div>
        <div class="user-dropdown">
          <div class="user-dropdown-info">
            <div class="user-dropdown-name">${api.user?.name || 'User'}</div>
            <div class="user-dropdown-role">${api.user?.user_type || 'Tenant'}</div>
          </div>
          <a href="dashboard.html" class="user-dropdown-item">👤 My Dashboard</a>
          ${isOwner ? `<a href="add-property.html" class="user-dropdown-item">➕ Add Property</a>` : `<a href="#" class="user-dropdown-item" onclick="event.preventDefault(); toast('Only Property Owners can add listings.', 'error')">➕ Add Property</a>`}
          ${api.isAdmin() ? `<a href="superadmin.html" class="user-dropdown-item">🛡️ Superadmin Panel</a>` : ''}
          <div class="user-dropdown-item logout" onclick="handleLogout()">🚪 Log Out</div>
        </div>
      </div>
    `;

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      const userMenu = document.getElementById('userMenu');
      if (userMenu && !userMenu.contains(e.target)) {
        userMenu.classList.remove('open');
