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
