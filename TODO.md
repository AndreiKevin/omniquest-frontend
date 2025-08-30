## OmniQuest Grocery App — Project TODO

Color scheme: blue, black, white. Frontend: TypeScript/React, React Query, Tailwind, shadcn/ui. Backend: FastAPI, Postgres (pgvector), NGINX, Docker, Locust.

### Milestone 1 — Bootstrap & Scaffolding
- [ ] Create `frontend/` with Vite (React + TS)
- [ ] Add Tailwind CSS, configure theme (blue/black/white)
- [ ] Initialize shadcn/ui and base components
- [ ] Install React Query and setup `QueryClientProvider`
- [ ] Create `backend/` FastAPI project skeleton
- [ ] Wire dev server scripts for both apps

### Milestone 2 — Backend Products API (Phase 1: file-backed)
- [ ] Define product schema (pydantic model)
- [ ] Implement `/products` endpoint with pagination, category filter, price sort
- [ ] Load data from `data.json` (temporary until DB)
- [ ] Validate query params and error handling
- [ ] Basic CORS setup for frontend

### Milestone 3 — Frontend Products Page
- [ ] Products grid: name, brand, category, price, image
- [ ] Opacity-in transition for cards
- [ ] Category filter dropdown (shadcn Select)
- [ ] Sort-by-price control (button/toggle)
- [ ] Active filter/sort badges under controls
- [ ] Badge delete (hover shows x, quick opacity transition)
- [ ] Responsive grid; handle different image sizes (height 100, variable width)

### Milestone 4 — Data Fetching & Pagination
- [ ] React Query hooks for products
- [ ] Paginated requests (never fetch full list)
- [ ] Infinite scroll on grid with intersection observer
- [ ] Cache pages; reset cache on filter/sort changes

### Milestone 5 — Chatbot UI (Frontend)
- [ ] Always-visible docked chat panel on right
- [ ] Message list (user/assistant bubbles like Messenger)
- [ ] Input + send button; disabled while sending
- [ ] Wire to backend `/chatbot` endpoint
- [ ] Render recommended products as cards beneath assistant replies

### Milestone 6 — Backend: DB + Search + RAG
- [ ] Dockerized Postgres with `pgvector`
- [ ] SQLAlchemy models and migrations for products
- [ ] Indexes on `category`, `price`
- [ ] Background job to ingest `data.json` into DB and vector store
- [ ] Embeddings generation (OpenAI or sentence-transformers)
- [ ] Vector similarity search (pgvector)
- [ ] `/chatbot` endpoint
  - [ ] embed query
  - [ ] retrieve top N similar products
  - [ ] construct prompt with user query + product snippets
  - [ ] call LLM to pick best products and explain
  - [ ] return LLM text + structured products

### Milestone 7 — Infra: NGINX, Gunicorn, Horizontal Scale
- [ ] Gunicorn config (multiple workers) for FastAPI app
- [ ] NGINX reverse proxy: SSL termination, caching, rate limits, health checks, retries
- [ ] Document process-level load balancing and settings
- [ ] docker-compose with two backend replicas and DB
- [ ] Scale docs: how to increase replicas and DB

### Milestone 8 — Load Testing (Locust)
- [ ] Locustfile: product search/filter/sort flows
- [ ] Scenarios targeting 16,384 concurrent users (explain assumptions)
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

