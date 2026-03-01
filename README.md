
---

# KEEFAO Backend API

**Kenya Education Empowerment Fund Alumni Organization (KEEFAO) Backend System**

A secure, scalable Django REST API powering the KEEFAO website for member registration, event management, automated contributions, announcements, and gallery.

---

# 🚀 Key Features

### 💳 Integrated Payment Systems

* **M-Pesa Express (STK Push):** Real-time mobile payment integration via Safaricom Daraja API.
* **Stripe Global Payments:** Support for international credit/debit card donations.
* **Automated Accounting:** Django Signals automatically convert successful `Payments` into `Contribution` records and update Member balances.

### 👤 Member & Public Features

* **Member Portal:** Registration, JWT-based authentication, and automated username generation.
* **Event Management:** Event creation and secure registration for logged-in alumni.
* **Public Contributions:** Anonymous or named donations (min. KES 50) with no login required.
* **Dynamic Content:** API endpoints for Announcements and Gallery management.

### 🛠️ Advanced Admin Dashboard

* **Financial Insights:** Custom admin templates displaying total verified contributions and entry counts.
* **Visual Auditing:** Color-coded transaction statuses (Pending, Verified, Failed).
* **Batch Operations:** One-click verification for manual contribution audits.

---

# 🏗️ Project Structure

```text
keefao-backend/
├── keefao/              # Project configuration (settings, urls, wsgi)
├── apps/
│   ├── accounts/        # Custom Member model & Auth logic
│   ├── contributions/   # Contribution records & aggregate logic
│   ├── payments/        # M-Pesa & Stripe services, Webhooks, and Signals
│   ├── events/          # Event management & Registrations
│   ├── core/            # Global SiteSettings & Utilities
│   └── gallery/         # Image management
├── templates/
│   └── admin/           # Custom Admin dashboard overrides
├── static/ & media/     # Assets and user-uploaded content
└── manage.py

```

---

# 🛠️ Tech Stack

* **Backend:** Python 3.12+, Django 5.x, Django REST Framework (DRF)
* **Auth:** SimpleJWT (JSON Web Tokens)
* **Payments:** Safaricom Daraja API, Stripe API
* **Database:** SQLite (Dev), PostgreSQL (Recommended for Prod)
* **Task Handling:** Django Signals (Real-time processing)

---

# 🚀 Installation & Setup

### 1. Environment Setup

```bash
git clone https://github.com/yourusername/keefao.git
cd keefao
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

```

### 2. Configuration (`.env`)

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your_secret_key
MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_SHORTCODE=174379
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

```

### 3. Database Initialization

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

```

```
# Core Framework
Django>=4.2,<5.1
djangorestframework
djangorestframework-simplejwt
django-cors-headers

# Database & Environment
psycopg2-binary        # PostgreSQL driver for production
python-dotenv          # Loads variables from .env
requests               # Required for M-Pesa Daraja API calls

# Payments & Media
stripe                 # Stripe Python SDK
Pillow                 # Image handling for Gallery/Profile photos

# Production Deployment
gunicorn               # WSGI HTTP Server for UNIX
whitenoise             # Serving static files efficiently in production
```
---

# 🔌 API Endpoints (Highlights)

| Endpoint | Method | Description | Auth |
| --- | --- | --- | --- |
| `/api/register/` | POST | Alumni self-registration | Public |
| `/api/payments/mpesa/` | POST | Trigger M-Pesa STK Push | Public/Member |
| `/api/payments/stripe/` | POST | Create Stripe Checkout Session | Public/Member |
| `/api/contributions/` | GET | List verified contributions | Public |
| `/api/events/register/` | POST | Register for an upcoming event | **Member** |

---

# 📊 Admin Insights

Access the dashboard at `/admin`.
The **Contributions** module features a custom header:

* **Total Verified Amount:** Real-time sum of all successful KEEF funding.
* **Status Indicators:** Orange (Pending), Green (Verified), Red (Failed).

---

# 🔒 Security

* **Idempotency:** Signals check `payment_reference` to prevent double-counting contributions.
* **Validation:** Minimum contribution limits and secure webhook signature verification for Stripe.
* **Environment Safety:** Sensitive credentials managed via environment variables.

---

# 📄 License & Support

Distributed under the **MIT License**.
Maintained by the **KEEFAO Tech Team**.
Contact: [keefao@example.com](mailto:keefao@example.com)

---

