## OmniQuest Grocery App — Project TODO

Color scheme: blue, black, white. Frontend: TypeScript/React, React Query, Tailwind, shadcn/ui. Backend: FastAPI, Postgres (pgvector), NGINX, Docker, Locust.

### Milestone 1 — Bootstrap & Scaffolding
- [x] Create `frontend/` with Vite (React + TS)
- [x] Add Tailwind CSS, configure theme (blue/black/white)
- [x] Initialize shadcn/ui and base components
- [x] Install React Query and setup `QueryClientProvider`
- [x] Create `backend/` FastAPI project skeleton
- [x] Wire dev server scripts for both apps

### Milestone 2 — Backend Products API (Phase 1: file-backed)
- [x] Define product schema (pydantic model)
- [x] Implement `/products` endpoint with pagination, category filter, price sort
- [x] Add `/categories` endpoint
- [x] Load data from `data.json` (temporary until DB)
- [ ] Validate query params and error handling (improve messages/ranges)
- [x] Basic CORS setup for frontend

### Milestone 3 — Frontend Products Page
- [x] Products grid: name, brand, category, price, image
- [x] Opacity-in transition for cards
- [x] Category filter dropdown (multi-select checklist)
- [x] Sort-by-price single toggle (off ↔ low→high ↔ high→low)
- [x] Active filter/sort badges under controls (wrap, hover→X)
- [x] Responsive grid; handle different image sizes (height 100, variable width)

### Milestone 4 — Data Fetching & Pagination
- [x] React Query hooks for products
- [x] Paginated requests (never fetch full list)
- [x] Infinite scroll on grid with intersection observer
- [x] Cache pages; reset cache on filter/sort changes via query keys

### Milestone 5 — Chatbot UI (Frontend)
- [x] Always-visible docked chat panel on right
- [x] Message list (bubbles with markdown support; user right-aligned)
- [x] Loading pulse bubble while awaiting response
- [x] Wire to backend `/chatbot` endpoint
- [x] Render recommended products as cards beneath assistant replies

### Milestone 6 — Backend: DB + Search + RAG
- [x] Dockerized Postgres with `pgvector` (compose/dev-db)
- [x] SQLAlchemy models for products (+ pgvector column)
- [x] Indexes: base category/price (add vector index as needed)
- [x] Ingest `data.json` into DB with FastEmbed (384 dims)
- [x] Vector similarity search with pgvector (<=> cosine)
- [x] `/chatbot` endpoint
  - [x] embed query (FastEmbed)
  - [x] retrieve top N similar products
  - [x] construct prompt incl. products JSON + recent messages
  - [x] call LLM (OpenAI preferred, Azure fallback)
  - [x] return LLM text + structured products

### Milestone 7 — Infra: NGINX, Gunicorn, Horizontal Scale
- [x] Gunicorn config (multiple workers) for FastAPI app
- [x] NGINX reverse proxy: upstream to two backends
- [x] docker-compose with two backend replicas and DB
- [ ] Document LB settings, SSL termination, rate limiting
- [ ] Scale docs: how to increase replicas and DB

### Milestone 8 — Load Testing (Locust)
- [x] Locustfile: product page, pagination, filters, sort scenarios
- [ ] Scenarios targeting 16,384 concurrent users (document assumptions)
- [ ] Measure latency and error rates under load
- [ ] Report and tuning guidance

### Milestone 9 — DX, QA, and Docs
- [ ] README with setup/run instructions (dev and docker-compose)
- [ ] Architecture diagrams (frontend, backend, proxy, DB, vector flow)
- [ ] .env templates for secrets/keys
- [ ] Basic CI hints (format/lint/test)

---

### Implementation Notes
- Image sizes vary (e.g., 208×100, 233×100, all ≥ ?×100). Constrain height to 100px, object-contain.
- Always fetch only visible page; reset when filters/sort change.
- Use badges to show active filters/sort with quick opacity hover→X transition.
- Chatbot recommendations must be grounded in availability and user description via RAG.

### Stretch
- Skeleton loaders for grid and chat
- Error boundaries and retry UI
- Persisted React Query cache between navigations

