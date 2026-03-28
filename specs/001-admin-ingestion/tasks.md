# Tasks: Admin Ingestion Dashboard

**Input**: Design documents from `/specs/001-admin-ingestion/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD approach per constitution (Test-First NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `docusaurus-textbook/src/`
- Paths shown match the actual project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 [P] Install backend dependencies: python-multipart in backend/requirements.txt
- [x] T002 [P] Install frontend dependency: react-dropzone in docusaurus-textbook/package.json
- [ ] T003 [P] Verify existing authentication system (Better-Auth) is functional
- [ ] T004 [P] Verify Qdrant Cloud connection in backend/config.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Add `is_admin` column to User model in backend/models/user.py
- [x] T006 Create Alembic migration for is_admin column in backend/alembic/versions/
- [x] T007 [P] Create IngestionLog model in backend/models/ingestion_log.py
- [x] T008 [P] Create ReindexJob model in backend/models/reindex_job.py
- [x] T009 Create Alembic migration for ingestion_logs and reindex_jobs tables in backend/alembic/versions/
- [x] T010 [P] Create admin authorization dependency in backend/auth/dependencies.py (get_current_admin_user)
- [x] T011 [P] Create PerformanceMonitor singleton class in backend/services/performance_monitor.py
- [x] T012 Run Alembic migrations: `alembic upgrade head` in backend/
- [x] T013 [P] Update User model relationship to include ingestion_logs in backend/models/user.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Admin File Upload (Priority: P1) 🎯 MVP

**Goal**: Enable administrators to upload multiple PDF/Markdown files through a drag-and-drop interface with progress tracking

**Independent Test**: Admin can log in, navigate to upload page, select multiple files, and verify successful upload and indexing

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Contract test for POST /api/admin/ingest/upload in backend/tests/contract/test_admin_api.py
- [ ] T015 [P] [US1] Contract test for POST /api/admin/ingest/upload-batch in backend/tests/contract/test_admin_api.py
- [ ] T016 [US1] Integration test for file upload → Qdrant indexing in backend/tests/integration/test_ingestion_pipeline.py
- [ ] T017 [US1] Test file validation (size, type, magic bytes) in backend/tests/unit/test_ingestion_service.py

### Implementation for User Story 1

- [x] T018 [P] [US1] Create IngestionService class in backend/services/ingestion_service.py
- [x] T019 [P] [US1] Implement file validation logic in backend/services/ingestion_service.py
- [x] T020 [US1] Implement PDF content extraction in backend/services/ingestion_service.py
- [x] T021 [US1] Implement Markdown content extraction in backend/services/ingestion_service.py
- [x] T022 [US1] Implement Qdrant indexing with metadata in backend/services/ingestion_service.py
- [x] T023 [P] [US1] Create admin API router in backend/api/admin.py
- [x] T024 [US1] Implement POST /api/admin/ingest/upload endpoint in backend/api/admin.py
- [x] T025 [US1] Implement POST /api/admin/ingest/upload-batch endpoint in backend/api/admin.py
- [x] T026 [US1] Add rate limiting (10 uploads/minute) in backend/api/admin.py
- [x] T027 [US1] Register admin router in backend/main.py
- [x] T028 [P] [US1] Create FileUploader component in docusaurus-textbook/src/components/Admin/FileUploader.jsx
- [x] T029 [US1] Implement drag-and-drop with react-dropzone in docusaurus-textbook/src/components/Admin/FileUploader.jsx
- [x] T030 [US1] Implement XMLHttpRequest for upload progress tracking in docusaurus-textbook/src/components/Admin/FileUploader.jsx
- [x] T031 [US1] Add success/error toast notifications in docusaurus-textbook/src/components/Admin/FileUploader.jsx
- [x] T032 [US1] Create admin ingest page in docusaurus-textbook/src/pages/admin/ingest.tsx
- [x] T033 [US1] Add AdminGuard protection to ingest page in docusaurus-textbook/src/pages/admin/ingest.tsx
- [x] T034 [US1] Apply Neon-Blue/Glassmorphism theme to upload component in docusaurus-textbook/src/components/Admin/FileUploader.jsx
- [x] T035 [US1] Add logging for upload operations in backend/api/admin.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Indexed Files (Priority: P2)

**Goal**: Display a list of all indexed files with metadata (name, status, chunk count, timestamps)

**Independent Test**: Admin can navigate to ingestion page and see a table of indexed files with complete metadata

### Tests for User Story 2 ⚠️

- [ ] T036 [P] [US2] Contract test for GET /api/admin/ingest/files in backend/tests/contract/test_admin_api.py
- [ ] T037 [US2] Integration test for list files with pagination in backend/tests/integration/test_ingestion_pipeline.py
- [ ] T038 [US2] Test empty state (no files indexed) in backend/tests/unit/test_ingestion_service.py

### Implementation for User Story 2

- [ ] T039 [P] [US2] Implement get_indexed_files method in backend/services/ingestion_service.py
- [ ] T040 [US2] Implement Qdrant query for file metadata in backend/services/ingestion_service.py
- [ ] T041 [US2] Implement pagination logic (limit, offset, sort) in backend/services/ingestion_service.py
- [ ] T042 [US2] Implement GET /api/admin/ingest/files endpoint in backend/api/admin.py
- [ ] T043 [P] [US2] Create IndexedFilesTable component in docusaurus-textbook/src/components/IndexedFilesTable.jsx
- [ ] T044 [US2] Implement table with columns: file name, type, size, chunk count, status, uploaded_at in docusaurus-textbook/src/components/IndexedFilesTable.jsx
- [ ] T045 [US2] Add pagination controls (prev/next, page numbers) in docusaurus-textbook/src/components/IndexedFilesTable.jsx
- [ ] T046 [US2] Implement empty state message with guidance in docusaurus-textbook/src/components/IndexedFilesTable.jsx
- [ ] T047 [US2] Add auto-refresh every 30 seconds in docusaurus-textbook/src/components/IndexedFilesTable.jsx
- [ ] T048 [US2] Apply Neon-Blue/Glassmorphism theme to table in docusaurus-textbook/src/components/IndexedFilesTable.jsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Re-index Knowledge Base (Priority: P3)

**Goal**: Allow administrators to trigger background re-indexing of all files with progress tracking

**Independent Test**: Admin can click re-index button and see real-time progress updates until completion

### Tests for User Story 3 ⚠️

- [ ] T049 [P] [US3] Contract test for POST /api/admin/ingest/reindex in backend/tests/contract/test_admin_api.py
- [ ] T050 [P] [US3] Contract test for GET /api/admin/ingest/reindex/status in backend/tests/contract/test_admin_api.py
- [ ] T051 [US3] Integration test for reindex job lifecycle in backend/tests/integration/test_ingestion_pipeline.py
- [ ] T052 [US3] Test concurrent reindex prevention (409 conflict) in backend/tests/unit/test_ingestion_service.py

### Implementation for User Story 3

- [ ] T053 [P] [US3] Implement reindex_all background task in backend/services/ingestion_service.py
- [ ] T054 [US3] Implement get_reindex_progress method in backend/services/ingestion_service.py
- [ ] T055 [US3] Implement single-job enforcement logic in backend/services/ingestion_service.py
- [ ] T056 [P] [US3] Implement POST /api/admin/ingest/reindex endpoint in backend/api/admin.py
- [ ] T057 [US3] Implement GET /api/admin/ingest/reindex/status endpoint in backend/api/admin.py
- [ ] T058 [P] [US3] Add ReindexButton component in docusaurus-textbook/src/components/ReindexButton.jsx
- [ ] T059 [US3] Implement polling for reindex status (every 5 seconds) in docusaurus-textbook/src/components/ReindexButton.jsx
- [ ] T060 [US3] Add progress bar and status display in docusaurus-textbook/src/components/ReindexButton.jsx
- [ ] T061 [US3] Add completion notification/toast in docusaurus-textbook/src/components/ReindexButton.jsx
- [ ] T062 [US3] Integrate ReindexButton into ingest page in docusaurus-textbook/src/pages/admin/ingest.tsx

**Checkpoint**: At this point, User Stories 1, 2, and 3 should all work independently

---

## Phase 6: User Story 4 - Monitor System Performance (Priority: P4)

**Goal**: Display chat latency metrics and Grok API health status in real-time

**Independent Test**: Admin can view performance section and see current latency metrics and API status

### Tests for User Story 4 ⚠️

- [ ] T063 [P] [US4] Contract test for GET /api/admin/metrics in backend/tests/contract/test_admin_api.py
- [ ] T064 [P] [US4] Contract test for GET /api/admin/grok/status in backend/tests/contract/test_admin_api.py
- [ ] T065 [US4] Test metrics calculation (avg, p95, p99) in backend/tests/unit/test_performance_monitor.py
- [ ] T066 [US4] Test Grok API health check in backend/tests/unit/test_grok_client.py

### Implementation for User Story 4

- [ ] T067 [P] [US4] Add middleware to record API latencies in backend/middleware/metrics_middleware.py
- [ ] T068 [US4] Register metrics middleware in backend/main.py
- [ ] T069 [US4] Implement get_metrics method in backend/services/performance_monitor.py
- [ ] T070 [US4] Implement GET /api/admin/metrics endpoint in backend/api/admin.py
- [ ] T071 [P] [US4] Implement Grok API health check in backend/llm/grok_client.py
- [ ] T072 [US4] Implement GET /api/admin/grok/status endpoint in backend/api/admin.py
- [ ] T073 [P] [US4] Create PerformanceMetrics component in docusaurus-textbook/src/components/PerformanceMetrics.jsx
- [ ] T074 [US4] Implement latency display (avg, p95, p99) in docusaurus-textbook/src/components/PerformanceMetrics.jsx
- [ ] T075 [US4] Implement Grok status indicator (healthy/unhealthy) in docusaurus-textbook/src/components/PerformanceMetrics.jsx
- [ ] T076 [US4] Add auto-refresh every 60 seconds in docusaurus-textbook/src/components/PerformanceMetrics.jsx
- [ ] T077 [US4] Integrate PerformanceMetrics into ingest page in docusaurus-textbook/src/pages/admin/ingest.tsx
- [ ] T078 [US4] Apply Neon-Blue/Glassmorphism theme to metrics display in docusaurus-textbook/src/components/PerformanceMetrics.jsx

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Access Control Enforcement (Priority: P5)

**Goal**: Ensure only admin users can access ingestion dashboard and related endpoints

**Independent Test**: Non-admin users are denied access (403) while admin users are granted access (200)

### Tests for User Story 5 ⚠️

- [ ] T079 [P] [US5] Test get_current_admin_user dependency with admin user in backend/tests/unit/test_auth.py
- [ ] T080 [US5] Test get_current_admin_user dependency with non-admin user (403) in backend/tests/unit/test_auth.py
- [ ] T081 [US5] Integration test for admin-only endpoint access in backend/tests/integration/test_admin_auth.py
- [ ] T082 [US5] Frontend test for AdminGuard redirect in docusaurus-textbook/src/components/__tests__/AdminGuard.test.jsx

### Implementation for User Story 5

- [ ] T083 [P] [US5] Update useAuth hook to include is_admin field in docusaurus-textbook/src/hooks/useAuth.tsx
- [ ] T084 [P] [US5] Create AdminGuard component in docusaurus-textbook/src/components/AdminGuard.jsx
- [ ] T085 [US5] Implement redirect logic for non-admin users in docusaurus-textbook/src/components/AdminGuard.jsx
- [ ] T086 [US5] Apply AdminGuard to ingest page in docusaurus-textbook/src/pages/admin/ingest.tsx
- [ ] T087 [P] [US5] Create AdminNav component in docusaurus-textbook/src/components/AdminNav.jsx
- [ ] T088 [US5] Add conditional "Admin Panel" link to navbar (only if user.is_admin) in docusaurus-textbook/src/components/AdminNav.jsx
- [ ] T089 [US5] Integrate AdminNav into theme/Navbar in docusaurus-textbook/src/theme/Navbar/index.js
- [ ] T090 [US5] Add security event logging for unauthorized access attempts in backend/auth/dependencies.py
- [ ] T091 [US5] Verify all admin endpoints use get_current_admin_user dependency in backend/api/admin.py

**Checkpoint**: All user stories complete with full access control enforcement

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T092 [P] Add Swagger/OpenAPI documentation annotations in backend/api/admin.py
- [ ] T093 [P] Update API documentation in docs/ directory
- [ ] T094 Code cleanup and refactoring across all services
- [ ] T095 Performance optimization: Add database connection pooling verification
- [ ] T096 [P] Add comprehensive unit tests for edge cases in backend/tests/unit/
- [ ] T097 Security hardening: Verify all file uploads are sanitized
- [ ] T098 Run quickstart.md validation steps
- [ ] T099 [P] Test complete user journey: upload → view → reindex → monitor
- [ ] T100 [P] Test access control: verify non-admin users cannot access any admin endpoints

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent, may use US1 components
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on IngestionLog model (US1)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Cross-cutting, applies to all stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD per constitution)
- Models before services
- Services before endpoints
- Backend before frontend (for integration)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: All tasks T001-T004 can run in parallel
- **Phase 2**: T005, T007, T008, T010, T011, T013 can run in parallel
- **Phase 3**: T014-T017 (tests) can run in parallel; T018, T023, T028 can start in parallel after tests
- **Phase 4**: T036-T038 (tests) can run in parallel; T039, T043 can start in parallel
- **Phase 5**: T049-T052 (tests) can run in parallel; T053, T056, T058 can start in parallel
- **Phase 6**: T063-T066 (tests) can run in parallel; T067, T071, T073 can start in parallel
- **Phase 7**: T079-T082 (tests) can run in parallel; T083, T084, T087 can start in parallel
- **Phase 8**: T092, T093, T096, T098, T099, T100 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for POST /api/admin/ingest/upload in backend/tests/contract/test_admin_api.py"
Task: "Contract test for POST /api/admin/ingest/upload-batch in backend/tests/contract/test_admin_api.py"
Task: "Integration test for file upload → Qdrant indexing in backend/tests/integration/test_ingestion_pipeline.py"
Task: "Test file validation in backend/tests/unit/test_ingestion_service.py"

# Launch all models for User Story 1 together:
(Already in Foundational phase - IngestionLog model)

# Launch backend services in parallel:
Task: "Create IngestionService class in backend/services/ingestion_service.py"
Task: "Create admin API router in backend/api/admin.py"

# Launch frontend components in parallel (after backend endpoints ready):
Task: "Create FileUploader component in docusaurus-textbook/src/components/FileUploader.jsx"
Task: "Create admin ingest page in docusaurus-textbook/src/pages/admin/ingest.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T013) - CRITICAL
3. Complete Phase 3: User Story 1 (T014-T035)
4. **STOP and VALIDATE**: Test file upload → indexing → appearance in list
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (File Upload) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (View Files) → Test independently → Deploy/Demo
4. Add User Story 3 (Re-index) → Test independently → Deploy/Demo
5. Add User Story 4 (Performance) → Test independently → Deploy/Demo
6. Add User Story 5 (Access Control) → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (File Upload)
   - Developer B: User Story 2 (View Files)
   - Developer C: User Story 4 (Performance Monitoring)
3. After US1/2/4 complete:
   - Developer A: User Story 3 (Re-index)
   - Developer B: User Story 5 (Access Control)
4. All stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD per constitution)
- Commit after each task or logical group of 2-3 tasks
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **Total Tasks**: 100 tasks across 8 phases
- **MVP Scope**: Phases 1-3 (35 tasks) for User Story 1 only
