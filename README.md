# Sanjivni — AI Emergency Coordination Platform

## Architecture
- `frontend/`: React + Vite PWA, deployable to Vercel
- `backend/`: Django REST Framework API with PostgreSQL/Redis support
- AI triage: Groq-compatible API integration using Llama 3.1
- Roles: Patient, Hospital Admin, Ambulance Driver

## Quick start

### Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

### Backend
```bash
cd backend
cp .env.example .env
python -m venv .venv
# activate the environment
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## Vercel
Import this GitHub repository into Vercel and set the Root Directory to `frontend`.
Set `VITE_API_URL` to your deployed backend API URL.

For production, deploy Django to a Python-capable host and use PostgreSQL + Redis.
