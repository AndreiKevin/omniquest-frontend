## OmniQuest Grocery

### 1) Design and Implementation Overview

- Frontend
  - React + TypeScript, Vite, Tailwind v4, shadcn/ui.
  - React Query caches server results by params: query key is ['products', { pageSize, categories, sort }]. Switching sort/filters yields distinct cache entries; toggling back reuses cached pages until stale.
  - Product grid is responsive; images are object-contain within a fixed height to handle varying sizes. Cards fade in.
  - Filters: multi-category checklist dropdown; badges wrap and are removable. Sort is a single toggle: Off → Low→High → High→Low.
  - Chatbot: right-docked panel, markdown-rendered assistant messages, content-sized bubbles, and a pulsing loading bubble.

- Backend
  - FastAPI endpoints: /products (pagination, multi-category filters, price sort), /categories, /chatbot.
  - Data: file-backed (data.json) or Postgres (auto-switch via DATABASE_URL).
  - RAG: FastEmbed (384 dims) embeddings stored in pgvector; similarity uses cosine operator <=> with optional IVFFlat index.
  - Chat: prompt contains user query, recent messages, and retrieved products JSON. Provider selection: OpenAI (OPENAI_API_KEY) → Azure AI Inference (GITHUB_TOKEN) → fallback.

- Database and Indexing
  - Schema: products(id uuid, product_name, brand, category, price, quantity, product_image, embedding vector(384)).
  - Indexes (created in db_init.py):
    - idx_products_category_price_btree(category, price)
    - idx_products_price_btree(price)
    - idx_products_category_btree(category)
    - idx_products_embedding_cos USING ivfflat (embedding vector_cosine_ops)
  - Index usage in queries:
    - Filters use category IN (...), enabling the btree (category) and the composite (category,price) during sorted reads.
    - Sorting by price (with or without category predicate) benefits from the composite or single-column price index.
    - Similarity search embeds the query (FastEmbed) and orders by embedding <=> :vector, which uses the IVFFlat index when present.
    - You can verify with EXPLAIN/EXPLAIN ANALYZE after running python -m app.db_init.

- Infra & Scaling
  - Gunicorn worker processes for CPU core utilization.
  - NGINX reverse proxy load-balances two backend replicas (compose) and fronts the API.
  - Dev DB compose for a standalone pgvector Postgres.
  - High-concurrency settings:
    - docker-compose ulimits nofile raised to 65536 for services handling many sockets.
    - Gunicorn: workers increased and worker_connections tuned for asyncio worker.
    - SQLAlchemy: pool_size/max_overflow tuned to avoid descriptor exhaustion under heavy load.
    - Consider increasing OS ulimits and NGINX worker_connections for 10k+ concurrent users.

### 2) Setup and Run

Dev (venv + file-backed):
- Backend
  - cd backend
  - py -3 -m venv .venv
  - .\.venv\Scripts\Activate.ps1
  - pip install -r requirements.txt
  - uvicorn app.main:app --reload
- Frontend
  - cd frontend
  - npm install
  - npm run dev

Dev (with Postgres + pgvector):
- From repo root: docker compose up -d db (or: docker compose -f docker-compose.dev-db.yml up)
- In backend shell:
  - set DATABASE_URL (see HELP.md)
  - python -m app.db_init
  - python -m app.ingest
  - uvicorn app.main:app --reload

Docker (full stack):
- Ensure backend/.env.docker and frontend/.env.docker exist.
- docker compose up --build
- Frontend: http://localhost:5173
- API via NGINX: http://localhost:8080

LLM Env:
- OpenAI: OPENAI_API_KEY, optional OPENAI_MODEL (default gpt-4o-mini)
- Azure AI Inference (GitHub Models): GITHUB_TOKEN, optional AZURE_INFERENCE_ENDPOINT (default https://models.github.ai/inference), AZURE_INFERENCE_MODEL (default mistral-ai/mistral-small-2503)

Load Testing:
- cd backend
- locust -f locustfile.py --host http://127.0.0.1:8000
- Provided tasks exercise pagination, multi-category filtering, and sorting.

Notes:
- If changing embedding model/dimension, update Vector column size and rerun ingest; rebuild the IVFFlat index if used.
- Assistant messages render markdown (GFM) in the UI.
