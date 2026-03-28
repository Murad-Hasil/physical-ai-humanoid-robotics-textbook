# Implementation Plan: Phase 4-5 Stability Layer

**Branch**: `001-performance-monitoring` | **Date**: 2026-03-18 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-performance-monitoring/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement backend stability features including ReindexService for manual knowledge base re-indexing, enhanced PerformanceMonitor for RAG step tracking, admin UI expansion with System Health tab, and secure API endpoints with rate limiting. The implementation builds on existing infrastructure (PostgreSQL, Qdrant, FastAPI) and integrates with the PerformanceMonitor service from Phase 2.

## Technical Context

**Language/Version**: Python 3.12, TypeScript 5.6, React 19
**Primary Dependencies**: FastAPI 0.109+, SQLAlchemy 2.0+, Pytest, Docusaurus 3.9+
**Storage**: PostgreSQL (Neon), Qdrant Cloud (vector database), local filesystem for uploads
**Testing**: pytest, pytest-asyncio, pytest-cov
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: 10 files/second re-indexing rate, <3s dashboard load time, <200ms p95 API latency
**Constraints**: Admin-only access for re-indexing, rate-limited operations, zero-downtime during health checks
**Scale/Scope**: Support 10k+ documents in Qdrant, 100+ concurrent users, real-time health monitoring

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Library-First Principle
**Status**: ✅ PASS
- ReindexService will be a standalone, testable service module
- PerformanceMonitor extensions are self-contained
- All services have clear single responsibilities

### Gate 2: CLI Interface (if applicable)
**Status**: N/A
- This is a web API feature, not a CLI tool
- Text I/O protocol not applicable

### Gate 3: Test-First (NON-NEGOTIABLE)
**Status**: ✅ COMMITTED
- TDD mandatory: Tests written → Implementation → Refactor
- Red-Green-Refactor cycle will be enforced
- Unit tests for services, integration tests for API endpoints

### Gate 4: Integration Testing
**Status**: ✅ COMMITTED
- Contract tests for new API endpoints (`POST /api/admin/reindex`, `GET /api/admin/stats`)
- Integration tests for ReindexService + IngestionService pipeline
- Service communication tests for PerformanceMonitor + RAG pipeline

### Gate 5: Observability & Simplicity (YAGNI)
**Status**: ✅ PASS
- Structured logging for all re-indexing operations
- Performance metrics logged with timestamps
- Start simple: in-memory progress tracking, no complex state machines
- Rate limiting prevents overload without complex queuing

## Project Structure

### Documentation (this feature)

```text
specs/001-performance-monitoring/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── services/
│   ├── reindex_service.py    # NEW: ReindexService
│   ├── performance_monitor.py # EXISTING: Enhanced with RAG step tracking
│   └── ...
├── api/
│   ├── admin.py              # EXISTING: New endpoints added
│   └── ...
├── models/
│   ├── reindex_job.py        # EXISTING
│   └── ...
└── tests/
    ├── unit/
    │   ├── test_reindex_service.py
    │   └── test_performance_monitor.py
    └── integration/
        ├── test_admin_endpoints.py
        └── test_reindex_flow.py
```

**Structure Decision**: Using existing backend structure with services/ pattern. ReindexService follows the same architectural pattern as IngestionService and HardwareContextService.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Background job tracking | Re-indexing is long-running | Polling simpler than WebSockets for MVP |
| Rate limiting | Prevents server overload | Required for security, not optional |

## Phase 0: Research & Discovery

### Unknowns to Resolve

1. **Re-indexing Progress Tracking**: How to track and expose progress to frontend?
   - Options: Database state (ReindexJob model), in-memory cache, Redis
   - Decision: Use ReindexJob model in PostgreSQL for persistence across restarts

2. **RAG Step Timing**: How to measure individual RAG pipeline steps?
   - Options: Middleware decorators, service-level timing, context managers
   - Decision: Service-level timing in RAG pipeline with structured logging

3. **Health Check Frequency**: How often to poll service health?
   - Options: Real-time on-demand, periodic background checks, hybrid
   - Decision: On-demand health checks with client-side caching (30s TTL)

4. **Rate Limiting Strategy**: What limits for re-indexing endpoint?
   - Options: Per-user, global, IP-based
   - Decision: Per-user rate limiting (existing upload_limiter pattern)

### Research Dispatch

**Task 1**: Research best practices for long-running job tracking in FastAPI
- Focus: Background tasks, job queues, progress tracking patterns
- Output: research.md section on job tracking

**Task 2**: Research RAG pipeline instrumentation patterns
- Focus: Timing individual steps (embedding, search, context assembly, LLM)
- Output: research.md section on RAG timing

**Task 3**: Research health check patterns for microservices
- Focus: Database connectivity, external API health, vector DB health
- Output: research.md section on health checks

**Task 4**: Research rate limiting patterns for heavy operations
- Focus: Token bucket, sliding window, concurrent request limits
- Output: research.md section on rate limiting

## Phase 1: Design & Contracts

### Data Model (data-model.md)

**Entities**:

1. **ReindexJob** (existing, verify completeness)
   - Fields: id, status, total_files, processed_files, failed_files, current_file, timestamps
   - Status enum: queued, running, completed, cancelled, failed
   - Relationships: created_by_user (User)

2. **PerformanceMetric** (new, if persisting metrics)
   - Fields: id, timestamp, endpoint, method, latency_ms, step_type, user_id
   - Step types: embedding, search, context_assembly, llm_call

### API Contracts (contracts/)

**New Endpoints**:

1. `POST /api/admin/reindex` - Trigger manual re-indexing
   - Request: {} (empty body)
   - Response: `{ job_id, status, total_files, message }`
   - Errors: 429 (rate limited), 403 (not admin), 500 (internal error)

2. `GET /api/admin/reindex/status` - Get re-indexing job status
   - Request: query params (job_id optional, returns latest if omitted)
   - Response: `{ job_id, status, progress, current_file, started_at, completed_at }`
   - Errors: 404 (job not found)

3. `GET /api/admin/stats` - Get performance and health stats
   - Request: query params (time_range optional)
   - Response: `{ rag_latency, llm_latency, health_status, usage_analytics }`
   - Errors: 403 (not admin)

4. `GET /api/admin/health` - Get system health status
   - Request: {}
   - Response: `{ postgresql, qdrant, grok_api }` with status and response_time
   - Errors: none (always returns health status)

### Quickstart (quickstart.md)

**For Developers**:
1. Run migrations: `alembic upgrade head`
2. Start backend: `uvicorn main:app --reload`
3. Test endpoints: `curl -X POST http://localhost:8000/api/admin/reindex` (with auth token)

**For Testing**:
1. Run tests: `pytest tests/unit/test_reindex_service.py -v`
2. Integration tests: `pytest tests/integration/test_reindex_flow.py -v`

## Phase 2: Implementation Tasks

*Note: Tasks will be created by /sp.tasks command*

### Backend Tasks (anticipated)

1. Create ReindexService with progress tracking
2. Enhance PerformanceMonitor with RAG step timing
3. Implement POST /api/admin/reindex endpoint
4. Implement GET /api/admin/stats endpoint
5. Implement GET /api/admin/health endpoint
6. Add rate limiting to re-indexing endpoint
7. Write unit tests for ReindexService
8. Write integration tests for admin endpoints

### Frontend Tasks (anticipated)

1. Create System Health tab component
2. Create Sync Knowledge Base section with progress bar
3. Implement polling for re-indexing progress
4. Add Last Synced timestamp display
5. Style components with robotic theme

## Success Metrics

- **SC-001**: Re-indexing completes at 10+ files/second
- **SC-002**: Dashboard loads within 3 seconds
- **SC-003**: Health checks complete within 500ms per service
- **SC-004**: Rate limiting prevents >10 re-index operations per minute per user
- **SC-005**: All new endpoints have 90%+ test coverage

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Re-indexing blocks other operations | High | Run as background task, non-blocking |
| Qdrant timeout during bulk upsert | Medium | Batch upserts with retries |
| Rate limiting too aggressive | Medium | Monitor and adjust limits based on usage |
| Health checks add latency | Low | Cache results with TTL |

---

**Next Step**: Run `/sp.tasks` to break this plan into actionable implementation tasks.
