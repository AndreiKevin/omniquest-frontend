# Setup and Usage Guide

## Prerequisites
- Node.js 20+ and npm 10+
- Python 3.11+ (3.12 recommended)
- Docker and Docker Compose
- Windows PowerShell (or macOS/Linux shell)

## Frontend (Dev)
1) Open a terminal:
   - cd to the /frontend directory
   - npm install
   - npm run dev
2) Open the printed URL (e.g., http://localhost:5173). If 5173 is busy, Vite will choose 5174/5175.

## Backend (Dev, file-backed)
Windows PowerShell:
- cd to the /backend directory
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

## Backend Dev Setup
1) Configure .env
   - Development environment variables.
     - DATABASE_URL: postgresql+psycopg://postgres:postgres@127.0.0.1:5432/dev
       - Assuming you run with the dev DB docker compose file
     - Optional LLM config (OpenAI preferred; if missing, Azure AI Inference is used):
       - OPENAI_API_KEY
       - OPENAI_MODEL (default: gpt-4o-mini)
       - GITHUB_TOKEN (GitHub Models/Azure AI Inference)
       - AZURE_INFERENCE_ENDPOINT (default: https://models.github.ai/inference)
       - AZURE_INFERENCE_MODEL (default: mistral-ai/mistral-small-2503)
2) Start Dev Postgres:
   ```bash
   docker-compose -f docker-compose.dev-db.yml up --build
   ```
3) Initialize schema and load data **(once only)**:
   - python -m app.db_init
   - python -m app.ingest
4) Run API:
   - uvicorn app.main:app --reload


## Backend Prod Setup
1) Configure .env.docker
   - Production environment variables.
     - DATABASE_URL
     - Optional LLM config (OpenAI preferred; if missing, Azure AI Inference is used):
       - OPENAI_API_KEY
       - OPENAI_MODEL (default: gpt-4o-mini)
       - GITHUB_TOKEN (GitHub Models/Azure AI Inference)
       - AZURE_INFERENCE_ENDPOINT (default: https://models.github.ai/inference)
       - AZURE_INFERENCE_MODEL (default: mistral-ai/mistral-small-2503)
2) Start Dev Postgres:
   ```bash
   docker-compose -f docker-compose.dev-db.yml up --build
   ```
3) Initialize schema and load data **(once only)**:
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
Backend:
 - DATABASE_URL: Postgres connection string
 - OPENAI_API_KEY: If present, backend uses OpenAI for reasoning (preferred)
 - OPENAI_MODEL: Optional model name (default gpt-4o-mini)
 - GITHUB_TOKEN: If OPENAI_API_KEY is absent and this is present, backend uses Azure AI Inference (GitHub Models)
 - AZURE_INFERENCE_ENDPOINT: Optional, default https://models.github.ai/inference
 - AZURE_INFERENCE_MODEL: Optional, default mistral-ai/mistral-small-2503

Frontend:
 - VITE_API_URL: Base URL for the API (e.g., http://127.0.0.1:8000 in dev, http://localhost:8080 in docker)

Notes:
 - LLM selection order: OpenAI (if OPENAI_API_KEY) → Azure AI Inference (if GITHUB_TOKEN) → fallback text.
 - Embeddings use FastEmbed (384 dims) stored in pgvector; ensure the vector extension exists (db_init does this) and re-run ingest if you change models.

## Common Commands
- Deactivate Python venv: deactivate
- Stop Docker stack: docker compose down

## Troubleshooting
- PowerShell cannot run Activate.ps1: Run once in the same shell: Set-ExecutionPolicy -Scope Process RemoteSigned
- Port in use: Close the process or let Vite choose another port automatically.
- Node engine warnings: Use Node 20+ (nvm-windows/macOS) or build/run via Docker.


