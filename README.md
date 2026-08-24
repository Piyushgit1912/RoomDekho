# 🏠 RoomDekho – Smart Room & PG Finder Platform

A full-stack web application built with **Django REST Framework** + **HTML/CSS/JS** to find and list rooms, PGs, flats, and hostels across India — with zero brokerage.

---

## 📁 Project Structure

```
RoomDekho/
│
├── backend/                   ← Django backend
│   ├── manage.py
│   ├── seed_data.py           ← Load sample data
│   │
│   ├── roomdekho/             ← Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── users/                 ← Auth, profiles, favorites
│   ├── properties/            ← Listings & images
│   ├── bookings/              ← Inquiries
│   └── reviews/               ← Ratings & comments
│
├── frontend/                  ← HTML pages
│   ├── index.html             ← Home page
│   ├── property-list.html     ← Search & filter listings
│   ├── property-details.html  ← Full property view + inquiry
│   ├── add-property.html      ← 3-step listing form
│   ├── dashboard.html         ← User dashboard
│   ├── login.html
│   ├── register.html
│   └── about.html
│
├── static/
│   ├── css/main.css           ← Complete design system
│   └── js/api.js              ← API client & utilities
│
├── requirements.txt
└── .env.example
```

---

## 🚀 HOW TO RUN THE PROJECT

### Prerequisites
- Python 3.10 or higher
- pip (comes with Python)

---

### STEP 1 – Extract the ZIP

```
cd RoomDekho
```
### STEP 2 – Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should now see `(venv)` at the start of your terminal prompt.

### STEP 3 – Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Django, Django REST Framework, CORS headers, Pillow, and the MySQL client.

---

### STEP 4 – Set Up the MySQL Database

By default, this project is configured to use **MySQL**. 
Before running migrations, ensure you have a MySQL server running and create a database named `roomies_db`.

You can update the database credentials (username/password) in `backend/roomdekho/settings.py` under the `DATABASES` section to match your local MySQL configuration. The default expects username `root` and password `0809`.

Once your MySQL database is ready, run the migrations:

```bash
cd backend

python manage.py makemigrations users
python manage.py makemigrations properties
python manage.py makemigrations bookings
python manage.py makemigrations reviews
python manage.py migrate
```

---

### STEP 5 – Create Admin Account

```bash
python manage.py createsuperuser
```

Enter your desired username, email, and password when prompted.

---

### STEP 6 – (Optional) Load Sample Data

```bash
python manage.py shell < seed_data.py
```
*(If the above command doesn't work in Windows PowerShell, use `Get-Content seed_data.py | python manage.py shell`)*

This creates a sample owner account and 5 approved property listings so you can see the app working immediately.

Sample owner credentials:
- **Username:** `sample_owner`
- **Password:** `password123`

---

### STEP 7 – Start the Backend Server

```bash
python manage.py runserver
```

The API will be live at: **http://localhost:8000**
Django Admin panel: **http://localhost:8000/admin/**

---

### STEP 8 – Open the Frontend

Open a **new terminal tab/window** (keep the Django server running), then from the project root:

```bash
cd ..
python -m http.server 5500
```

Now open your browser and go to:
**http://localhost:5500/frontend/index.html**

> **Alternative:** You can also just double-click `frontend/index.html` directly in your file explorer to open it in a browser — but the live server method above is recommended for correct relative paths.

---

## 🔗 API Endpoints Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/register/` | No | Register new user |
| POST | `/api/login/` | No | Login, returns token |
| POST | `/api/logout/` | Yes | Logout |
| GET/PATCH | `/api/profile/` | Yes | View/update profile |
| GET | `/api/properties/` | No | List & search properties |
| GET | `/api/properties/{id}/` | No | Property detail |
| POST | `/api/add-property/` | Owner | Add new listing |
| PUT | `/api/update-property/{id}/` | Owner | Edit listing |
| DELETE | `/api/delete-property/{id}/` | Owner | Delete listing |
| GET | `/api/my-properties/` | Owner | Your listings |
| GET/POST | `/api/favorites/` | Yes | Saved properties |
| POST | `/api/inquiries/` | Yes | Send inquiry |
| GET | `/api/my-inquiries/` | Yes | View sent inquiries |
| GET/POST | `/api/properties/{id}/reviews/` | Mixed | Reviews |
| GET | `/api/admin/properties/` | Admin | All listings |
| POST | `/api/admin/properties/{id}/approve/` | Admin | Approve/reject |

### Search & Filter Parameters for `GET /api/properties/`

| Parameter | Example | Description |
|-----------|---------|-------------|
| `search` | `?search=Mumbai` | Search by city/location/title |
| `city` | `?city=Pune` | Filter by city |
| `room_type` | `?room_type=pg` | single/double/pg/hostel/flat_1bhk/flat_2bhk |
| `min_price` | `?min_price=5000` | Minimum rent |
| `max_price` | `?max_price=15000` | Maximum rent |
| `furnished_status` | `?furnished_status=furnished` | furnished/semi/unfurnished |
| `gender_preference` | `?gender_preference=female` | any/male/female |
| `wifi` | `?wifi=true` | WiFi available |
| `ac` | `?ac=true` | AC available |
| `parking` | `?parking=true` | Parking available |
| `food` | `?food=true` | Meals included |
| `ordering` | `?ordering=price` | price/-price/-created_at |

---

## 👥 User Roles

| Role | How to get | Capabilities |
|------|------------|--------------|
| **Tenant** | Register with "I'm a Tenant" | Search, save favorites, send inquiries, write reviews |
| **Owner** | Register with "I'm an Owner" | All tenant features + add/edit/delete listings |
| **Admin** | Set via Django admin panel | Approve/reject listings, manage all users |

To make a user an admin via Django Admin:
1. Go to `http://localhost:8000/admin/`
2. Open **Users → CustomUser**
3. Check **Staff status** and **Superuser status** for that user

---

## 🌐 Frontend Pages

| File | URL | Description |
|------|-----|-------------|
| `index.html` | `/` | Home: hero search, city cards, featured listings |
| `property-list.html` | `/property-list.html` | Search + filter sidebar + property cards |
| `property-details.html` | `/property-details.html?id=1` | Gallery, amenities, reviews, inquiry modal |
| `add-property.html` | `/add-property.html` | 3-step listing form with image upload |
| `dashboard.html` | `/dashboard.html` | My listings, favorites, inquiries, profile |
| `login.html` | `/login.html` | Email/password login |
| `register.html` | `/register.html` | Tenant or Owner registration |
| `about.html` | `/about.html` | About page |
| `superadmin.html` | `/superadmin.html` | Admin dashboard for overall platform management |

---

## 🔒 Security Features
- Token-based authentication (DRF TokenAuth)
- Passwords hashed with Django's PBKDF2
- CORS headers configured for cross-origin API access
- Owners can only edit/delete their own properties
- Admin approval required before listings go live

---

## 🛠️ Common Issues & Fixes

**"Module not found" error:**
Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.

**CORS error in browser:**
Make sure the Django server is running on port 8000 and `CORS_ALLOW_ALL_ORIGINS = True` is in settings.py.

**Images not loading:**
Make sure you're running the Django server — it serves media files in development.

**"No properties found" on home page:**
Run the seed data script: `python manage.py shell < seed_data.py`

---

## ⚙️ Switch to PostgreSQL (Optional)

1. Install: `pip install psycopg2-binary`
2. In `backend/roomdekho/settings.py`, replace the DATABASES block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'roomdekho_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🚢 Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Use a strong random `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Switch to PostgreSQL
- [ ] Use `gunicorn` as WSGI server
- [ ] Use `nginx` as reverse proxy
- [ ] Run `python manage.py collectstatic`
- [ ] Set up environment variables (do not hardcode secrets)

---

*Built with ❤️ for students and working professionals across India*


