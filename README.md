# OmniQuest Grocery

## Design and Implementation Overview

- Frontend
  - React + TypeScript, Vite, Tailwind v4, shadcn/ui.
  - React Query caches server results by params: query key is ['products', { pageSize, categories, sort }]. Switching sort/filters yields distinct cache entries; toggling back reuses cached pages until stale.
  - Product grid is responsive; images are object-contain within a fixed height to handle varying sizes. Cards fade in.
  - Filters: multi-category checklist dropdown; filter badges wrap and are removable on click. Sort is a single toggle: Off → Low→High → High→Low.
  - Chatbot: right-docked panel, markdown-rendered assistant messages, content-sized bubbles, and a pulsing loading bubble. Recommended products are cards beneath assistant replies. User query used to semantically search the database for similar products then passed to the LLM to answer the user's question directly.

- Backend
  - FastAPI endpoints: /products (pagination, multi-category filters, price sort), /categories, /chatbot.
  - Data: file-backed (data.json) or Postgres (auto-switch via DATABASE_URL).
  - RAG: FastEmbed (384 dims) embeddings stored in pgvector; similarity uses cosine operator <=>.
  - Chat: prompt contains user query, recent messages, and retrieved products JSON. Chatbot has context to previous messages up to a max of 6 messages (arbitrary limit). Provider selection: OpenAI (OPENAI_API_KEY) → Azure AI Inference (GITHUB_TOKEN) → fallback.

- Database and Indexing
  - Schema: products(id uuid, product_name, brand, category, price, quantity, product_image, embedding vector(384)).
  - Indexes (created in db_init.py):
    - idx_products_category_price_btree(category, price)
    - idx_products_price_btree(price)
    - idx_products_category_btree(category)
  - Index usage in queries:
    - Filters use category IN (...), enabling the btree (category) and the composite (category,price) during sorted reads.
    - Sorting by price (with or without category predicate) benefits from the composite or single-column price index.
    - Similarity search embeds the query (FastEmbed) and orders by embedding <=> :vector.

- Infra & Scaling
  - Gunicorn worker processes for CPU core utilization (since Python is inherently single-threaded, Gunicorn is used to handle multiple requests concurrently).
  - NGINX reverse proxy load-balances two backend replicas (compose) and fronts the API. Even distribution of requests across the two backends is achieved using the least_conn load balancing setting.
  - Dev DB compose for a standalone pgvector Postgres.
  - High-concurrency settings:
    - docker-compose ulimits nofile raised to 65536 for services handling many sockets.
    - Gunicorn: workers increased and worker_connections tuned for asyncio worker.
    - SQLAlchemy: pool_size/max_overflow tuned to avoid descriptor exhaustion under heavy load.

- Limitations
  - Database connection gets exhausted quickly with ~17 failed requests/sec at ~277 requests/sec.

--------------------------------

## Usage Guide

### Prerequisites
- Node.js 20+ and npm 10+
- Python 3.11+ (3.12 recommended)
- Docker and Docker Compose

### Development Environment Setup

#### Frontend Development
1) Open a terminal:
   - cd to the /frontend directory
   - npm install
   - npm run dev
2) Open the printed URL (e.g., http://localhost:5173). If 5173 is busy, Vite will choose 5174/5175.

#### Backend Development

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


### Production Setup

1) Configure **backend/.env.docker** 
   - DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/omniquest
   - GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>

Get a free Github token from: https://github.com/marketplace/models/azureml-mistral/mistral-small-2503 -> Use this model -> Configure Authentication -> Create Personal Access Token

1) Configure **frontend/.env.docker** 
   - VITE_API_URL=http://localhost:8080

2) cd ..

3) Run Docker Compose:
   ```bash
   docker compose up --build
   ```

4) Frontend: http://localhost:5173

Load Testing:
- cd backend
- locust -f locustfile.py --host http://127.0.0.1:8000
- Provided tasks exercise pagination, multi-category filtering, and sorting.
