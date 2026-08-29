# SETU — Strategic Disaster Response Command System

SETU (Strategic Emergency & Transport Unit) is a full-stack disaster response management and GIS intelligence platform. It provides real-time telemetry, risk corridor analysis, relief stock allocation, and dispatch recommendations for regional command centers, field officers, NGOs, and citizens.

```text
                                  USERS
                                    │
                                    ▼
                            ┌──────────────┐
                            │    Vercel    │
                            │ React Frontend│
                            └───────┬──────┘
                                    │ HTTPS API (VITE_API_URL)
                                    ▼
                            ┌──────────────┐
                            │    Render    │
                            │ Django API   │
                            └───────┬──────┘
                                    │ DATABASE_URL
                                    ▼
                            ┌──────────────┐
                            │   Supabase   │
                            │  PostgreSQL  │
                            └──────────────┘
```

---

## Tech Stack

* **Frontend:** React, Vite, TailwindCSS, Leaflet / React-Leaflet, Axios
* **Backend:** Django 5, Django REST Framework, SimpleJWT, Gunicorn, WhiteNoise
* **Database:** PostgreSQL (Supabase in production, SQLite for local dev)
* **Frontend Hosting:** Vercel
* **Backend Hosting:** Render
* **Database Hosting:** Supabase

---

## Repository Structure

```text
SETU/
├── frontend/                 # Vite React application
│   ├── src/                  # React components, pages, API service, & utilities
│   ├── public/               # Public static assets (logos, icons)
│   ├── dist/                 # Production build output
│   ├── package.json          # Frontend dependencies & scripts
│   ├── vite.config.js        # Vite configuration & dev proxy
│   ├── vercel.json           # Vercel SPA routing rules
│   └── .env.example          # Frontend environment variables template
│
├── backend/                  # Django REST Framework API
│   ├── config/               # Django settings, WSGI/ASGI, URLs
│   ├── accounts/             # Authentication & user profile management
│   ├── core/                 # Disaster management models & API views
│   ├── logistics/            # Relief stock & inventory models
│   ├── matching/             # Demand-supply matching engine
│   ├── dashboard/            # Command dashboard telemetry & statistics
│   ├── manage.py             # Django CLI manager
│   ├── requirements.txt      # Backend Python dependencies
│   └── .env.example          # Backend environment variables template
│
├── matching_engine/          # ML scoring & hazard risk prediction models
├── render.yaml               # Render Infrastructure-as-Code blueprint
├── vercel.json               # Root Vercel deployment configuration
├── .gitignore                # Production Git ignore rules
└── README.md                 # Project documentation
```

---

## Local Development Setup

### Prerequisites
* Python 3.10+
* Node.js v18+ and npm

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables file
cp .env.example .env

# Apply database migrations (uses local SQLite by default)
python manage.py migrate

# (Optional) Seed demo dataset
python manage.py seed_demo_data

# Start local backend server (runs at http://localhost:8000)
python manage.py runserver
```

### 2. Frontend Setup (React + Vite)

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment variables file
cp .env.example .env

# Start development server (runs at http://localhost:3000)
npm run dev
```

During local development, Vite proxies `/api` and `/media` requests directly to `http://localhost:8000`.

---

## Environment Variables Reference

### Backend (`backend/.env` / Render Dashboard)

| Variable | Description | Example / Recommended Value |
| :--- | :--- | :--- |
| `SECRET_KEY` | Django cryptographic signing key | `django-insecure-...` (dev) / Secure random string (prod) |
| `DEBUG` | Enable Django debug mode | `True` (dev) / `False` (prod) |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames | `localhost,127.0.0.1,.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://postgres:pass@db.ref.supabase.co:5432/postgres` |
| `USE_SQLITE` | Force local SQLite usage | `True` (for local dev without PostgreSQL) |
| `CORS_ALLOWED_ORIGINS` | Allowed origins for cross-site requests | `https://your-app.vercel.app` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF validation | `https://your-app.vercel.app,https://your-backend.onrender.com` |
| `JWT_ACCESS_TOKEN_LIFETIME_MIN` | JWT access token expiration in minutes | `60` |

### Frontend (`frontend/.env` / Vercel Dashboard)

| Variable | Description | Example / Recommended Value |
| :--- | :--- | :--- |
| `VITE_API_URL` | Base URL of Django API backend | `http://localhost:8000` (dev) / `https://setu-backend.onrender.com` (prod) |

---

## Production Deployment Guide

### Step 1: Push Code to GitHub
Ensure all code is committed and pushed to your remote repository:
```bash
git add .
git commit -m "Prepare full-stack application for production deployment"
git push origin main
```

### Step 2: Set Up Supabase PostgreSQL Database
1. Sign up / log in to [Supabase](https://supabase.com/).
2. Create a **New Project**. Note down your database password.
3. Once provisioned, go to **Project Settings** $\rightarrow$ **Database**.
4. Copy the **URI Connection String** under *Connection String* (e.g., `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`).

### Step 3: Deploy Django Backend on Render
1. Sign up / log in to [Render](https://render.com/).
2. Click **New +** $\rightarrow$ **Web Service**.
3. Connect your GitHub repository.
4. Set the following parameters:
   * **Name:** `setu-backend`
   * **Root Directory:** `backend`
   * **Environment:** `Python 3`
   * **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --no-input`
   * **Start Command:** `python manage.py migrate --no-input && gunicorn config.wsgi:application`
5. Under **Environment Variables**, add:
   * `PYTHON_VERSION`: `3.11.0`
   * `DEBUG`: `False`
   * `SECRET_KEY`: *(Generate a random 50+ char secret key)*
   * `ALLOWED_HOSTS`: `.onrender.com`
   * `DATABASE_URL`: *(Your Supabase connection URI)*
   * `CORS_ALLOWED_ORIGINS`: `https://<YOUR-VERCEL-FRONTEND>.vercel.app`
   * `CSRF_TRUSTED_ORIGINS`: `https://<YOUR-VERCEL-FRONTEND>.vercel.app,https://<YOUR-RENDER-BACKEND>.onrender.com`
6. Click **Create Web Service**. Render will build and launch your API. Note down your backend URL (e.g., `https://setu-backend.onrender.com`).

### Step 4: Deploy React Frontend on Vercel
1. Sign up / log in to [Vercel](https://vercel.com/).
2. Click **Add New...** $\rightarrow$ **Project**.
3. Import your GitHub repository.
4. Configure Project Settings:
   * **Framework Preset:** Vite
   * **Root Directory:** `frontend`
   * **Build Command:** `npm run build`
   * **Output Directory:** `dist`
5. Environment Variables:
   * `VITE_API_URL`: `https://<YOUR-RENDER-BACKEND>.onrender.com`
6. Click **Deploy**. Vercel will build and host your application. Note down your frontend URL (e.g., `https://setu-app.vercel.app`).

### Step 5: Final Cross-Origin & Security Alignment
1. In your **Render Dashboard**, update `CORS_ALLOWED_ORIGINS` to match your actual Vercel URL (e.g. `https://setu-app.vercel.app`).
2. Test authentication, API responses, and database connectivity on your deployed frontend.

---

## Production Security & Media Notes

> [!IMPORTANT]
> **Ephemeral Disk Storage on Render**: Render free-tier web instances have ephemeral storage. User-uploaded files saved to local `MEDIA_ROOT` will reset upon instance restarts. For persistent production file storage, integrate an external cloud storage provider such as Supabase Storage or AWS S3.

---

## License

MIT License. Developed for SETU Strategic Disaster Command System.
