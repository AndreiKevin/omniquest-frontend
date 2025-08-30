# Setup and Usage Guide

## Prerequisites
- Node.js 20+ and npm 10+
- Python 3.11+ (3.12 recommended)
- Docker and Docker Compose
- Windows PowerShell (or macOS/Linux shell)

## Frontend (Dev)
1) Open a terminal:
   - cd "E:\Computer Science\omniquest-frontend\frontend"
   - npm install
   - npm run dev
2) Open the printed URL (e.g., http://localhost:5173). If 5173 is busy, Vite will choose 5174/5175.

## Backend (Dev, file-backed)
Windows PowerShell:
- cd "E:\Computer Science\omniquest-frontend\backend"
- py -3 -m venv .venv
- .\.venv\Scripts\Activate.ps1
- pip install -r requirements.txt
- uvicorn app.main:app --reload

macOS/Linux:
- cd omniquest-frontend/backend
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- uvicorn app.main:app --reload

API runs at http://127.0.0.1:8000

## Backend (DB mode with Postgres + pgvector)
1) Start Postgres:
   - From repo root: docker compose up -d db
2) In a new shell for backend:
   - Windows PowerShell: $env:DATABASE_URL = "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/omniquest"
   - macOS/Linux: export DATABASE_URL="postgresql+psycopg://postgres:postgres@127.0.0.1:5432/omniquest"
3) Initialize schema and load data:
   - python -m app.db_init
   - python -m app.ingest
4) Run API:
   - uvicorn app.main:app --reload

## Full Stack with Docker
From repo root:
- docker compose up --build

Ports:
- Frontend: http://localhost:5173
- NGINX reverse proxy (to backends): http://localhost:8080

## Environment Variables
- DATABASE_URL: Postgres connection string (enables DB-backed API)
- VITE_API_URL (optional): Override frontend API URL at build/runtime

## Common Commands
- Deactivate Python venv: deactivate
- Stop Docker stack: docker compose down

## Troubleshooting
- PowerShell cannot run Activate.ps1: Run once in the same shell: Set-ExecutionPolicy -Scope Process RemoteSigned
- Port in use: Close the process or let Vite choose another port automatically.
- Node engine warnings: Use Node 20+ (nvm-windows/macOS) or build/run via Docker.


