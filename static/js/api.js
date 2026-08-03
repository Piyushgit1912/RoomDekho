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
      }
    });
  }
}

window.toggleUserMenu = function(event) {
  event.stopPropagation();
  const userMenu = document.getElementById('userMenu');
  if (userMenu) {
    userMenu.classList.toggle('open');
  }
};

async function handleLogout() {
  try { await api.post('/logout/'); } catch(e) {}
  api.clearAuth();
  toast('Logged out successfully', 'success');
  setTimeout(() => window.location.href = 'index.html', 800);
}

/* ===== Favorites ===== */
async function toggleFavorite(propertyId, btn) {
  if (!api.isLoggedIn()) {
    toast('Please login to save favorites', 'error');
    return;
  }
  try {
    const res = await api.post('/favorites/', { property_id: propertyId });
    btn.classList.toggle('active', res.favorited);
    btn.textContent = res.favorited ? '❤️' : '🤍';
    toast(res.message, 'success');
  } catch(e) {
    toast('Failed to update favorites', 'error');
  }
}

/* ===== Currency Formatter ===== */
function formatPrice(price) {
  const n = Number(price);
  if (n >= 100000) return `₹${(n/100000).toFixed(1)}L`;
  if (n >= 1000) return `₹${(n/1000).toFixed(0)}K`;
  return `₹${n}`;
}

/* ===== Property Card HTML ===== */
function propertyCardHTML(p) {
  const img = p.primary_image || 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400&q=80';
  const stars = '★'.repeat(Math.round(p.avg_rating || 0)) + '☆'.repeat(5 - Math.round(p.avg_rating || 0));
  const typeLabel = p.room_type?.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase()) || 'Room';
  const tags = [
    p.furnished_status ? p.furnished_status.charAt(0).toUpperCase() + p.furnished_status.slice(1) : null,
    p.gender_preference !== 'any' ? (p.gender_preference === 'male' ? 'Boys' : 'Girls') : null,
    p.wifi ? 'WiFi' : null,
    p.ac ? 'AC' : null,
    p.parking ? 'Parking' : null,
  ].filter(Boolean).slice(0, 4);

  const photoCount = p.image_count || 0;

  return `
    <div class="property-card fade-in" onclick="window.location.href='property-details.html?id=${p.id}'">
      <div class="card-image">
        <img src="${img}" alt="${p.title}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&q=80'">
        <span class="card-badge">${typeLabel}</span>
        <button class="card-fav" onclick="event.stopPropagation(); toggleFavorite(${p.id}, this)">🤍</button>
        ${photoCount > 1 ? `<span class="card-photo-count">📷 ${photoCount} Photos</span>` : ''}
      </div>
      <div class="card-body">
        <div class="card-price">${formatPrice(p.price)} <span>/ month</span></div>
        <div class="card-title">${p.title}</div>
        <div class="card-location">📍 ${p.location}, ${p.city}</div>
        <div class="card-tags">${tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
        <div class="card-footer">
