# sotota-machineries-website

**M/S. Sotota Machineries Store**  
Station Road, Jamalpur, Mymensingh Division, Bangladesh  
Facebook: https://www.facebook.com/SototaMachineriesStore

---

## 📁 Complete Project Structure

```
sotota-machineries-website/
│
├── 📄 app.py                   ← Flask application (all routes)
├── 📄 models.py                ← SQLAlchemy database models
├── 📄 schema.sql               ← Raw SQL schema + seed data (run once)
├── 📄 requirements.txt         ← Python dependencies
├── 📄 .env.example             ← Environment variables template
├── 📄 .env                     ← YOUR config (never commit this)
├── 📄 README.md                ← This file
│
├── 📁 templates/               ← Jinja2 HTML templates (Flask renders these)
│   ├── base.html               ← Shared header, navbar, footer
│   ├── index.html              ← Homepage
│   ├── machines.html           ← Machines & Engines page
│   ├── generators.html         ← Generators & Shallow Machines
│   ├── motors.html             ← Motors & Water Pumps
│   ├── oils.html               ← Oils & Lubricants
│   ├── home_kitchen.html       ← Home & Kitchen Accessories
│   ├── fittings.html           ← Fittings
│   ├── about.html              ← About Us
│   ├── contact.html            ← Contact & Support
│   ├── 404.html                ← Error page
│   └── 📁 admin/               ← Admin panel templates
│       ├── login.html
│       ├── dashboard.html
│       ├── products.html
│       ├── product_form.html   ← Add / Edit product form
│       └── reviews.html
│
├── 📁 static/                  ← CSS, JS, images served directly
│   ├── 📁 css/
│   │   └── style.css           ← Main stylesheet
│   ├── 📁 js/
│   │   └── main.js             ← Shared JavaScript
│   └── 📁 uploads/             ← Product images uploaded via admin
│       └── (auto-created)
│
└── 📁 frontend/                ← Standalone HTML files (no server needed)
    ├── index.html
    ├── machines.html
    ├── generators.html
    ├── motors.html
    ├── oils.html
    ├── home-kitchen.html
    ├── fittings.html
    ├── about.html
    ├── contact.html
    └── admin.html
```

---

## ⚙️ Setup (Step by Step)

### 1 — Install Python & PostgreSQL
- Python 3.10 or higher
- PostgreSQL 14 or higher

### 2 — Install Python packages
```bash
cd sotota-machineries-website
pip install -r requirements.txt
```

### 3 — Create the database
```sql
-- In psql terminal:
CREATE DATABASE sotota_machineries;
```

### 4 — Configure environment
```bash
cp .env.example .env
# Open .env and fill in your real values:
#   DB_PASSWORD, SECRET_KEY, WHATSAPP_NUMBER, PHONE_NUMBER, ADMIN_PASSWORD
```

### 5 — Load the schema and seed data
```bash
psql -U postgres -d sotota_machineries -f schema.sql
```

### 6 — Run the Flask server
```bash
python app.py
```

Visit: **http://localhost:5000**  
Admin panel: **http://localhost:5000/admin**

---

## 🔗 All URL Routes

| URL | Page |
|-----|------|
| `/` | Homepage |
| `/machines` | Machines & Diesel Engines |
| `/generators` | Generators & Shallow Machines |
| `/motors` | Motors & Water Pumps |
| `/oils` | Oils & Lubricants |
| `/home-kitchen` | Home & Kitchen |
| `/fittings` | Fittings |
| `/about` | About Us |
| `/contact` | Contact & Support |
| `/submit-review` | POST — Submit customer review |
| `/admin` | Admin Dashboard |
| `/admin/login` | Admin Login |
| `/admin/products` | Manage all products |
| `/admin/products/add` | Add new product |
| `/admin/products/edit/<id>` | Edit product |
| `/admin/products/delete/<id>` | Delete product |
| `/admin/reviews` | Approve / delete reviews |
| `/api/products?category=machines&badge=Hot` | JSON API |
| `/api/categories` | JSON API — all categories |

---

## 🌐 Deploying Online

### Option A — PythonAnywhere (easiest, free tier)
1. Sign up at pythonanywhere.com
2. Upload all files
3. Create a PostgreSQL database (or use MySQL)
4. Set environment variables in the dashboard
5. Point WSGI file to `app.py`

### Option B — VPS (cPanel with Python)
1. Upload files to your hosting
2. Set up Python virtual environment
3. Configure `.env` with your database credentials
4. Run with gunicorn: `gunicorn app:app`

### Option C — cPanel Shared Hosting (HTML only)
Upload just the `frontend/` folder files into `public_html/` — no Python needed, works immediately.

---

## ⚠️ Important Before Going Live

1. Change `ADMIN_PASSWORD` in `.env` from `sotota2024` to your own secret password
2. Replace `8801XXXXXXXXX` with your real WhatsApp/phone number in `.env`
3. Set `FLASK_DEBUG=False` in `.env`
4. Generate a strong `SECRET_KEY` (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`)
