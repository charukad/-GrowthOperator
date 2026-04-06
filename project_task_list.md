# AI Social Growth OS (GrowthOperator) - Detailed Task List

This task list is broken down into 11 iterative vertical slices (Phase 0 to Phase 10). Each phase produces a working mini-system that includes frontend, backend, database, and workers.

## Phase 0 — Foundation Setup

_Goal: Prepare dev environment & setup core infrastructure. App runs locally with DB + Redis connected._

- [x] Setup monorepo structure (Turborepo or pnpm workspaces)
- [x] Create apps: web, api, worker
- [x] Setup Docker + docker-compose (Postgres, Redis, MinIO)
- [x] Enable `pgvector` extension in PostgreSQL
- [x] Setup FastAPI base project
- [x] Setup React + Vite + Tailwind CSS v4 for the frontend
- [x] Setup ESLint + Prettier
- [x] Setup environment variables management (`.env`, config loader)
- [x] Setup logging system (structlog / loguru)
- [x] Setup basic health check endpoints

## Phase 1 — Core Platform

_Goal: Basic system usable. User can login and create workspace._

- [x] Implement JWT authentication (access + refresh tokens)
- [x] Implement password hashing (bcrypt)
- [x] Create `users` table and `workspaces` table
- [x] Implement workspace RBAC (Role-Based Access Control)
- [x] Create base API router structure
- [x] Build minimal dashboard UI (Auth & Workspace selection)
- [x] Add global error handling
- [x] Add API request validation (Pydantic)
- [x] Create `brands` table (Brand Brain)

## Phase 2 — Trend + Idea Engine

_Goal: Generate usable ideas. User can generate trend-based ideas + hooks._

- [ ] Build scraping module (Playwright or requests-based)
- [ ] Create `trend_ingestion_worker`
- [ ] Normalize and store trends in DB with deduplication logic
- [ ] Implement embedding generation for trends
- [ ] Integrate LLM (OpenAI/Gemini/local)
- [ ] Build idea generation service
- [ ] Build hook generation service
- [ ] Add basic heuristic scoring for ideas
- [ ] Build idea UI (list + detail views)

... (rest of the file unchanged)
