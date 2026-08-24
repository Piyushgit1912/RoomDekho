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
