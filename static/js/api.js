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
