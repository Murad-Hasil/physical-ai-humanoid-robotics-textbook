# Tasks: Phase 4-5 Stability Layer

**Input**: Design documents from `/specs/001-performance-monitoring/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification or if user requests TDD approach.

**Organization**: Tasks are organized by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/services/`, `backend/api/`, `backend/models/`, `backend/tests/`
- **Frontend**: Docusaurus textbook frontend (admin dashboard components)
- Paths shown below use existing backend structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment verification

- [x] T001 Verify backend dependencies installed: `pip install -r backend/requirements.txt`
- [x] T002 Verify database connection (PostgreSQL or SQLite) in `backend/.env`
- [x] T003 Verify Qdrant connection configured in `backend/.env`
- [x] T004 [P] Verify Grok API key configured in `backend/.env`
- [x] T005 [P] Run existing test suite: `cd backend && pytest tests/ -v`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Verify ReindexJob model exists in `backend/models/reindex_job.py` with all required fields
- [x] T007 Create Alembic migration for reindex_jobs table if not exists: `alembic revision --autogenerate -m "Create reindex_jobs table"`
- [x] T008 Run migrations: `alembic upgrade head`
- [x] T009 [P] Create rate limiter for re-indexing in `backend/middleware/rate_limiter.py` (reuse upload_limiter pattern)
- [x] T010 [P] Add reindex_limiter instance: `RateLimiter(max_requests=10, window_seconds=60)` in `backend/middleware/rate_limiter.py`
- [x] T011 Verify PerformanceMonitor singleton in `backend/services/performance_monitor.py` has `record_step_latency()` method
- [x] T012 [P] Add RAGStepType enum to `backend/services/performance_monitor.py` (embedding, search, context_assembly, llm_call)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Performance Metrics Dashboard (Priority: P1) 🎯 MVP

**Goal**: Implement backend infrastructure to track and expose RAG latency and LLM latency metrics

**Independent Test**: Admin can call `GET /api/admin/stats` and receive latency metrics with avg, p95, p99 values

### Implementation for User Story 1

- [x] T013 [P] [US1] Add `record_step_latency(step_name: str, latency_ms: float)` method to `backend/services/performance_monitor.py`
- [x] T014 [P] [US1] Add `get_metrics_by_step(step_name: str)` method to `backend/services/performance_monitor.py`
- [x] T015 [US1] Enhance RAG pipeline to time embedding step in `backend/services/rag_pipeline.py` using context manager
- [x] T016 [US1] Enhance RAG pipeline to time search step in `backend/services/rag_pipeline.py` using context manager
- [x] T017 [US1] Enhance RAG pipeline to time context assembly step in `backend/services/rag_pipeline.py` using context manager
- [x] T018 [US1] Enhance Grok client to time LLM call in `backend/llm/grok_client.py` and report to PerformanceMonitor
- [x] T019 [US1] Implement `GET /api/admin/stats` endpoint in `backend/api/admin.py` returning rag_latency and llm_latency
- [x] T020 [US1] Add time_range query parameter support to `/api/admin/stats` endpoint
- [x] T021 [US1] Add error handling for PerformanceMonitor unavailability in `/api/admin/stats` endpoint
- [x] T022 [US1] Add structured logging for stats endpoint access in `backend/api/admin.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently via `/api/admin/stats` endpoint

---

## Phase 4: User Story 2 - Monitor System Health Status (Priority: P2)

**Goal**: Implement health check system for PostgreSQL, Qdrant, and Grok API connectivity

**Independent Test**: Admin can call `GET /api/admin/health` and receive status (healthy/unhealthy) for all three services

### Implementation for User Story 2

- [x] T023 [P] [US2] Create HealthStatus dataclass in `backend/services/health_service.py` (status, response_time_ms, error, last_checked)
- [x] T024 [P] [US2] Implement `check_postgresql_health()` function in `backend/services/health_service.py`
- [x] T025 [P] [US2] Implement `check_qdrant_health()` function in `backend/services/health_service.py`
- [x] T026 [P] [US2] Implement `check_grok_api_health()` function in `backend/services/health_service.py`
- [x] T027 [US2] Implement `GET /api/admin/health` endpoint in `backend/api/admin.py` calling all health check functions
- [x] T028 [US2] Add overall_status calculation logic (healthy/degraded/unhealthy) in `/api/admin/health` endpoint
- [x] T029 [US2] Add collection info to Qdrant health response (document_count, collection_name)
- [x] T030 [US2] Add structured logging for health check failures in `backend/services/health_service.py`
- [x] T031 [US2] Add error handling for each service health check (timeout handling)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Re-indexing with Progress Tracking (Priority: P3)

**Goal**: Implement manual re-indexing service with progress tracking and rate limiting

**Independent Test**: Admin can call `POST /api/admin/reindex` and monitor progress via `GET /api/admin/reindex/status`

### Implementation for User Story 3

- [x] T032 [P] [US3] Create ReindexService class in `backend/services/reindex_service.py`
- [x] T033 [P] [US3] Implement `count_files()` method in `backend/services/reindex_service.py` to count IngestionLog entries
- [x] T034 [US3] Implement `start_reindex(user: User)` method in `backend/services/reindex_service.py` creating ReindexJob
- [x] T035 [US3] Implement `_run_reindex(job_id: UUID)` background task in `backend/services/reindex_service.py`
- [x] T036 [US3] Implement progress update logic in `_run_reindex()` calling `update_job_progress()`
- [x] T037 [US3] Implement file re-indexing loop: get IngestionLog, re-run IngestionService pipeline
- [x] T038 [US3] Implement job completion logic (set status, completed_at) in `backend/services/reindex_service.py`
- [x] T039 [US3] Implement error handling and failed_files counter in `_run_reindex()`
- [x] T040 [US3] Implement `GET /api/admin/reindex/status` endpoint in `backend/api/admin.py`
- [x] T041 [US3] Add job_id query parameter support (return latest if omitted) in `/api/admin/reindex/status`
- [x] T042 [US3] Add progress calculation (percent_complete) in `/api/admin/reindex/status` response
- [x] T043 [US3] Add timing information (elapsed_seconds, estimated_remaining_seconds) in status response
- [x] T044 [US3] Add rate limiting to `POST /api/admin/reindex` endpoint using reindex_limiter
- [x] T045 [US3] Add concurrent job check (prevent multiple running jobs) in `POST /api/admin/reindex`
- [x] T046 [US3] Add structured logging for re-indexing operations (start, progress, completion, errors)
- [x] T047 [US3] Add 429 response with Retry-After header for rate-limited requests

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Admin UI Integration (Frontend - Docusaurus)

**Goal**: Create System Status tab in Admin Dashboard with health indicators and re-indexing controls

**Independent Test**: Admin can navigate to System Status page and see health badges, latency stats, and trigger re-indexing

### Implementation for Admin UI

- [x] T048 [P] [UI] Create SystemStatus page component in `docusaurus-textbook/src/pages/admin/status.tsx`
- [x] T049 [P] [UI] Create HealthCard component in `docusaurus-textbook/src/components/Admin/HealthCard.tsx` (displays service status)
- [x] T050 [UI] Implement latency display cards in status.tsx
- [x] T051 [UI] Implement API fetch for `/api/admin/health` in status.tsx
- [x] T052 [UI] Implement API fetch for `/api/admin/stats` in status.tsx
- [x] T053 [UI] Implement API fetch for `POST /api/admin/ingest/reindex` in status.tsx
- [x] T054 [UI] Implement API fetch for `GET /api/admin/reindex/status` in status.tsx
- [x] T055 [UI] Add System Status link to Admin Dashboard navigation (manual step)
- [x] T056 [UI] Implement polling logic for health status (30s interval) in SystemStatus component
- [x] T057 [UI] Implement polling logic for re-indexing progress (5s interval) during active jobs
- [x] T058 [UI] Create SyncKnowledgeBase section with "Re-index Now" button
- [x] T059 [UI] Implement progress bar for re-indexing progress display
- [x] T060 [UI] Add "Last Synced" timestamp display
- [x] T061 [UI] Style all components with neon color theme (green=healthy, orange=degraded, red=unhealthy)
- [x] T062 [UI] Add error state handling (display error messages when API calls fail)
- [x] T063 [UI] Add loading states for all async operations
- [x] T064 [UI] Implement health status color coding (green=healthy, red=unhealthy, yellow=degraded)

**Checkpoint**: Full admin UI with system health, latency stats, and re-indexing controls complete

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories

- [x] T065 [P] Update quickstart.md with new endpoint examples and testing commands
- [x] T066 [P] Add API documentation to `/docs` (Swagger/OpenAPI annotations)
- [x] T067 Code cleanup: remove unused imports, fix linting issues
- [x] T068 Add comprehensive error messages for all error scenarios
- [x] T069 [P] Add unit tests for ReindexService in `backend/tests/unit/test_reindex_service.py`
- [x] T070 [P] Add unit tests for HealthService in `backend/tests/unit/test_health_service.py`
- [x] T071 [P] Add integration tests for admin endpoints in `backend/tests/integration/test_admin_endpoints.py`
- [x] T072 [P] Add integration tests for re-indexing flow in `backend/tests/integration/test_reindex_flow.py`
- [x] T073 Run full test suite: `pytest tests/ -v --cov=services --cov=api`
- [x] T074 Security review: verify all admin endpoints require admin authentication
- [x] T075 Performance test: verify re-indexing achieves 10+ files/second rate
- [x] T076 Validate all success criteria from spec.md are met
- [x] T077 Update INFRASTRUCTURE_STATUS.md with new features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Admin UI (Phase 6)**: Depends on all backend endpoints being functional
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T004, T005)
- All Foundational tasks marked [P] can run in parallel (T009, T010, T012)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- All UI components marked [P] can run in parallel (T048, T049, T050)
- All test tasks marked [P] can run in parallel (T069, T070, T071, T072)

---

## Parallel Example: User Story 1

```bash
# Launch all US1 service enhancements together:
Task: "Add record_step_latency() method to performance_monitor.py"
Task: "Add get_metrics_by_step() method to performance_monitor.py"

# Then implement RAG pipeline timing:
Task: "Enhance RAG pipeline to time embedding step"
Task: "Enhance RAG pipeline to time search step"
Task: "Enhance RAG pipeline to time context assembly step"

# Then implement endpoint:
Task: "Implement GET /api/admin/stats endpoint"
```

---

## Parallel Example: User Story 2

```bash
# Launch all health check functions in parallel:
Task: "Implement check_postgresql_health() in health_service.py"
Task: "Implement check_qdrant_health() in health_service.py"
Task: "Implement check_grok_api_health() in health_service.py"

# Then implement endpoint:
Task: "Implement GET /api/admin/health endpoint"
```

---

## Parallel Example: User Story 3

```bash
# Launch ReindexService creation in parallel with methods:
Task: "Create ReindexService class"
Task: "Implement count_files() method"

# Then implement background task:
Task: "Implement _run_reindex() background task"
Task: "Implement progress update logic"
Task: "Implement file re-indexing loop"

# Then implement endpoints:
Task: "Implement GET /api/admin/reindex/status endpoint"
Task: "Implement POST /api/admin/reindex endpoint with rate limiting"
```

---

## Parallel Example: Admin UI

```bash
# Launch all UI components in parallel (different files):
Task: "Create SystemStatus page component"
Task: "Create HealthBadge component"
Task: "Create LatencyChart component"

# Launch all API service calls in parallel:
Task: "Implement API call for /api/admin/health"
Task: "Implement API call for /api/admin/stats"
Task: "Implement API call for POST /api/admin/reindex"
Task: "Implement API call for GET /api/admin/reindex/status"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test `/api/admin/stats` endpoint
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently via `/api/admin/stats` → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently via `/api/admin/health` → Deploy/Demo
4. Add User Story 3 → Test independently via `/api/admin/reindex` → Deploy/Demo
5. Add Admin UI → Test full dashboard → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Performance metrics)
   - Developer B: User Story 2 (Health checks)
   - Developer C: User Story 3 (Re-indexing)
3. Stories complete and integrate independently
4. Frontend developer starts Admin UI after backend endpoints are functional

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **Definition of Done**: Admin can trigger re-index and see progress, dashboard shows live latency stats, all connections verified with green "Online" indicators

---

## Task Summary

**Total Tasks**: 77

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 7 tasks
- Phase 3 (US1 - Performance Metrics): 10 tasks
- Phase 4 (US2 - Health Checks): 9 tasks
- Phase 5 (US3 - Re-indexing): 16 tasks
- Phase 6 (Admin UI): 17 tasks
- Phase 7 (Polish): 13 tasks

**Parallel Opportunities**:
- Setup: 2 tasks can run in parallel
- Foundational: 3 tasks can run in parallel
- US1: 2 tasks can run in parallel initially
- US2: 3 tasks can run in parallel initially
- US3: 2 tasks can run in parallel initially
- Admin UI: 4 tasks can run in parallel initially
- Polish: 4 test tasks can run in parallel

**Suggested MVP Scope**: Phases 1-3 (User Story 1 only) - 22 tasks
**Full Feature Scope**: All 7 phases - 77 tasks
