# KEEFAO Backend API

Kenya Education Empowerment Fund Alumni Organization (KEEFAO) Backend System

A secure, scalable Django REST API powering the KEEFAO website for member registration, event management, contributions, announcements, and gallery.

---

# Overview

KEEFAO is a Community Based Organization (CBO) in Kakamega, Kenya, founded in 2017 by KEEF alumni to support needy students through education funding.

This backend provides:

• Member registration and authentication
• Event creation and registration
• Public contributions (no login required)
• Announcements management
• Gallery management
• REST API for frontend integration

---

# Tech Stack

Backend
• Python 3.10+
• Django 4+
• Django REST Framework
• JWT Authentication

Database
• SQLite (development)
• PostgreSQL (production recommended)

Other
• CORS Headers
• Pillow (image handling)

---

# Project Structure

```
keefao-backend/
│
├── manage.py
├── README.md
├── .gitignore
├── requirements.txt
├── .env.example
│
├── keefao/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│
├── apps/
│   │
│   ├── accounts/
│   │   ├── models.py         # Member
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── events/
│   │   ├── models.py         #Event, EventRegistration
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── contributions/
│   │   ├── models.py         #Contribution
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── payments/
│   │   ├── models.py       # Payment
|   |   ├── services.py     # PaymentService 
│   │   ├── views.py        # Mpesa/Stripe views
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── mpesa.py
│   │   ├── stripe.py
│   │   └── admin.py
│   │
│   ├── core/
│   │   ├── models.py       # SiteSetting
│   │   ├── views.py        # SiteSettingsView
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   └── gallery/
│       ├── models.py         # GalleryImage
│       ├── views.py
│       ├── serializers.py
│       ├── urls.py
│       └── admin.py
│
├── media/
├── static/
│
└── scripts/
    └── wait-for-db.sh
```

---

# Features

Member Features

• Register as alumni member
• Automatic username generation
• Secure login authentication
• Event registration

Public Features

• View announcements
• View events
• View gallery
• Submit contribution (minimum KES 50)
• Donate without login

Admin Features

• Manage members
• Manage events
• Manage announcements
• Manage gallery
• View contributions

---

---
Benefits of core app
Global site settings are centralized and editable in admin.
Reusable view for frontend or API consumption.
Logging ready – tracks fetch success or errors.
Scalable – you can add more site-wide utilities, constants, or helpers.
Fully modular – sits cleanly alongside accounts, events, contributions, payments, and gallery.
---

# API Base URL

```
http://localhost:8000/api/
```

---

# API Endpoints

Authentication

POST `/api/register/`
Register new member

---

Events

GET `/api/events/`
List events

POST `/api/events/register/`
Register for event (requires login)

---

Contributions

POST `/api/contribute/`
Public contribution (no login required)

Minimum contribution: KES 50

---

Announcements

GET `/api/announcements/`
List announcements

---

Gallery

GET `/api/gallery/`
List gallery images

---

# Installation Guide

Step 1: Clone project

```
git clone https://github.com/yourusername/keefao.git

cd keefao
```

---

Step 2: Create virtual environment

```
python -m venv venv

source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

Step 3: Install dependencies

```
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install pillow
```

---

Step 4: Run migrations

```
python manage.py makemigrations

python manage.py migrate
```

---

Step 5: Create admin user

```
python manage.py createsuperuser
```

---

Step 6: Run server

```
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000
```

---

# Admin Panel

Access admin dashboard:

```
http://127.0.0.1:8000/admin
```

Admin can manage:

• Members
• Events
• Contributions
• Announcements
• Gallery

---

# Sample Member Registration JSON

```
POST /api/register/

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@email.com",
  "password": "securepassword",
  "sponsor_name": "Jane Doe",
  "kcse_year": 2018
}
```

---

# Contribution JSON Example

```
POST /api/contribute/

{
  "contributor_name": "Well Wisher",
  "email": "donor@email.com",
  "amount": 500,
  "message": "Supporting education"
}
```

---

# Production Deployment Recommendations

Use:

• PostgreSQL database
• Gunicorn
• Nginx
• HTTPS (Let's Encrypt)
• Cloud storage for media

Recommended hosts:

• Render
• Railway
• DigitalOcean
• AWS

---

# Security Features

• JWT authentication
• Password hashing
• Protected endpoints
• Minimum contribution validation

---

# Future Improvements

• M-Pesa integration
• Email notifications
• Member dashboard
• Payment tracking
• Reporting system

---

# License

MIT License

---

# Maintained By

KEEFAO Tech Team
Supporting education through technology.

---

# Support

For technical support contact:

[keefao@example.com](mailto:keefao@example.com)

 