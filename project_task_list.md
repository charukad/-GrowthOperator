# AI Social Growth OS (GrowthOperator) - Detailed Task List

This task list is broken down into 11 iterative vertical slices (Phase 0 to Phase 10). Each phase produces a working mini-system that includes frontend, backend, database, and workers.

## Phase 0 — Foundation Setup
*Goal: Prepare dev environment & setup core infrastructure. App runs locally with DB + Redis connected.*

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
*Goal: Basic system usable. User can login and create workspace.*

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
*Goal: Generate usable ideas. User can generate trend-based ideas + hooks.*

- [x] Build scraping module (Playwright or requests-based)
- [x] Create `trend_ingestion_worker`
- [x] Normalize and store trends in DB with deduplication logic
- [x] Implement embedding generation for trends
- [x] Integrate LLM (OpenAI/Gemini/local)
- [x] Build idea generation service
- [x] Build hook generation service
- [x] Add basic heuristic scoring for ideas
- [x] Build idea UI (list + detail views)

## Phase 3 — Content Engine
*Goal: Turn ideas into content. Idea → full script + caption.*

- [x] Build caption generation service
- [x] Build script generation service
- [x] Implement scene breakdown logic
- [ ] Add blueprint generator
- [ ] Implement hook scoring model (rule-based initially)
- [ ] Add content editing UI (rich text editor)
- [x] Add brand tone enforcement (simple rules)

## Phase 4 — Publishing System
*Goal: Post content. User can schedule and publish posts.*

- [ ] Implement social account connection (start with 1 platform, e.g., Facebook)
- [ ] Create `publish_jobs` table
- [ ] Build publish API endpoints
- [ ] Implement scheduling logic
- [ ] Create `publishing_worker`
- [ ] Handle platform-specific formatting
- [ ] Add retry and failure handling mechanism
- [ ] Add preview before publish feature

## Phase 5 — Analytics + Feedback
*Goal: Learn from results. User sees post performance.*

- [ ] Create metrics tables in the database
- [ ] Build `analytics_ingestion_worker`
- [ ] Fetch metrics from platform APIs
- [ ] Store analytics snapshots
- [ ] Create analytics API endpoints
- [ ] Build charts and dashboards UI
- [ ] Add basic performance scoring

## Phase 6 — Advanced Intelligence
*Goal: Smart system behavior. System improves idea quality using memory.*

- [ ] Build competitor scraping service
- [ ] Store competitor posts in DB
- [ ] Implement audience analysis heuristics
- [ ] Setup `pgvector` memory storage
- [ ] Implement similarity search for memory
- [ ] Add memory retrieval to the idea generation prompt context

## Phase 7 — Monetization Engine
*Goal: Generate revenue. Content linked to revenue strategy.*

- [ ] Create monetization tables
- [ ] Build affiliate offer system
- [ ] Add CTA (Call to Action) generation
- [ ] Map ideas to monetization strategies
- [ ] Add monetization scoring logic
- [ ] Add funnel suggestions

## Phase 8 — Engagement System
*Goal: Increase interaction. Engagement insights + reply suggestions.*

- [ ] Build `comment_ingestion_worker`
- [ ] Classify comments (basic NLP/LLM)
- [ ] Generate reply suggestions
- [ ] Add DM (Direct Message) ingestion
- [ ] Add lead detection scoring based on engagement

## Phase 9 — Agent System (Office)
*Goal: Full orchestration. Full agent-driven workflow system.*

- [ ] Create base agent interface class
- [ ] Implement Orchestrator Agent
- [ ] Define agent registry and implement specialized agents:
  - [ ] Trend Agent
  - [ ] Idea Agent
  - [ ] Hook Agent
  - [ ] Script Agent
  - [ ] Monetization Agent
  - [ ] Publishing Agent
  - [ ] Analytics Agent
  - [ ] Memory Agent
- [ ] Build workflow engine and task routing logic
- [ ] Add confidence scoring for agent outputs
- [ ] Build office visualization UI (agents + states)

## Phase 10 — Optimization & Production
*Goal: Production readiness.*

- [ ] Add caching (Redis)
- [ ] Optimize DB queries (add indexes)
- [ ] Add rate limiting
- [ ] Add audit logs
- [ ] Add feature flags
- [ ] Add monitoring (Prometheus + Grafana)
- [ ] Add structured logging
- [ ] Add error tracking (e.g., Sentry)
- [ ] Add CI/CD pipeline
- [ ] Deploy using Docker/Kubernetes
