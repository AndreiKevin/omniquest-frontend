# Setup and Usage Guide

## Prerequisites
- Node.js 20+ and npm 10+
- Python 3.11+ (3.12 recommended)
- Docker and Docker Compose

## Development Environment Setup

### Frontend Development
1) Open a terminal:
   - cd to the /frontend directory
   - npm install
   - npm run dev
2) Open the printed URL (e.g., http://localhost:5173). If 5173 is busy, Vite will choose 5174/5175.

### Backend Development

1) Install dependencies:
   Windows PowerShell:
   - cd to the /backend directory
   - py -3 -m venv .venv
   - .\.venv\Scripts\Activate.ps1
   - pip install -r requirements.txt

   macOS/Linux:
   - cd to the /backend directory
   - python -m venv .venv && source .venv/bin/activate
   - pip install -r requirements.txt

   API runs at http://127.0.0.1:8000

2) Configure **backend/.env**
   - DATABASE_URL: postgresql+psycopg://postgres:postgres@127.0.0.1:5432/dev
   - GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>

Get a free Github token from: https://github.com/marketplace/models/azureml-mistral/mistral-small-2503 -> Use this model -> Configure Authentication -> Create Personal Access Token

1) Run Dev Postgres:
   ```bash
   docker compose -f docker-compose.dev-db.yml up --build
   ```

2) Initialize schema and load data **(once only)**:
   - cd backend
   - python -m app.db_init
   - python -m app.ingest

3) Run Backend:
   - uvicorn app.main:app --reload


--------------------------------


## Production Setup

1) Configure **backend/.env.docker** 
   - DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/omniquest:
   - GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>

Get a free Github token from: https://github.com/marketplace/models/azureml-mistral/mistral-small-2503 -> Use this model -> Configure Authentication -> Create Personal Access Token

1) Configure **frontend/.env.docker** 
   - VITE_API_URL=http://localhost:8080

2) Run Docker Compose:
   ```bash
   docker compose up --build
   ```

3) Frontend: http://localhost:5173