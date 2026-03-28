# Tasks: Hardware-Aware Authentication and Personalization

**Input**: Design documents from `/specs/001-hardware-aware-auth/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks for validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/auth/`, `backend/models/`, `backend/services/`, `backend/api/`, `backend/tests/`
- **Frontend**: `docusaurus-textbook/src/components/`, `docusaurus-textbook/src/hooks/`, `docusaurus-textbook/src/pages/`
- Paths shown below follow the web app structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Create backend directory structure: backend/auth/, backend/models/, backend/services/, backend/api/, backend/utils/
- [x] T002 [P] Install Python dependencies: PyJWT, sqlalchemy, alembic, bcrypt, python-jose, passlib in backend/requirements.txt
- [x] T003 [P] Install frontend dependencies: better-auth in docusaurus-textbook/package.json
- [x] T004 Configure environment variables in backend/.env: DATABASE_URL, BETTER_AUTH_SECRET, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, JWT_SECRET
- [x] T005 [P] Initialize Alembic migrations in backend/alembic/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Create Better-Auth configuration in backend/auth/better_auth_config.py with email/password and GitHub OAuth providers
- [x] T007 [P] Create database engine and session factory in backend/db/session.py using SQLAlchemy with SQLite/PostgreSQL
- [x] T008 [P] Create base model class in backend/models/base.py with common fields (id, created_at, updated_at)
- [x] T009 [P] Implement session validator in backend/auth/session_validator.py for JWT/session token validation
- [x] T010 [P] Create FastAPI authentication middleware in backend/auth/middleware.py for dependency injection
- [x] T011 [P] Create PDF hardware constants utility in backend/utils/pdf_hardware_constants.py with Page 5 and Page 8 references
- [x] T012 Configure logging infrastructure in backend/utils/logger.py with security event logging
- [x] T013 [P] Create initial Alembic migration script in backend/alembic/versions/001_initial_schema.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Student Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Students can register with email/password or GitHub OAuth, sign in securely, and manage their session

**Independent Test**: Can be fully tested by registering a new student account, signing in, and verifying access to protected resources

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Contract test for registration endpoint in backend/tests/unit/test_auth.py::test_register_student
- [ ] T015 [P] [US1] Contract test for login endpoint in backend/tests/unit/test_auth.py::test_login_student
- [ ] T016 [P] [US1] Integration test for GitHub OAuth flow in backend/tests/integration/test_github_oauth.py
- [ ] T017 [P] [US1] Test session validation middleware in backend/tests/unit/test_session_validator.py

### Implementation for User Story 1

- [ ] T018 [P] [US1] Create User model extending Better-Auth in backend/models/user.py with email, password_hash, github_id, email_verified fields
- [ ] T019 [P] [US1] Create StudentProfile model in backend/models/student_profile.py with user_id FK, display_name, bio, timezone fields
- [ ] T020 [US1] Implement authentication service in backend/auth/auth_service.py with register, login, logout functions
- [ ] T021 [US1] Implement GitHub OAuth callback handler in backend/auth/github_oauth.py
- [ ] T022 [US1] Create auth API endpoints in backend/api/auth.py: POST /api/auth/register, POST /api/auth/login, POST /api/auth/logout, GET /api/auth/github, GET /api/auth/github/callback
- [ ] T023 [US1] Create GET /api/auth/me endpoint in backend/api/auth.py for retrieving current user
- [ ] T024 [US1] Add input validation for registration (email format, password length >= 8) in backend/api/auth.py
- [ ] T025 [US1] Add error handling for invalid credentials, duplicate email, OAuth failures in backend/api/auth.py
- [ ] T026 [US1] Add logging for authentication events (login attempts, failures, logout) in backend/auth/auth_service.py
- [ ] T027 [US1] Create useAuth hook in docusaurus-textbook/src/hooks/useAuth.js with user, loading, login, logout, register functions
- [ ] T028 [US1] Create LoginButton component in docusaurus-textbook/src/components/LoginButton.jsx with email/password and GitHub OAuth options
- [ ] T029 [US1] Create AuthProvider wrapper in docusaurus-textbook/src/theme/Root.js for global auth state management
- [ ] T030 [US1] Update Docusaurus navbar config in docusaurus-textbook/docusaurus.config.js to include LoginButton component

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - students can register, login, and see auth state in UI

---

## Phase 4: User Story 2 - Configure Hardware Profile from PDF (Priority: P2)

**Goal**: Students can save their hardware setup (Sim Rig or Edge Kit) with PDF-specified options to receive tailored guidance

**Independent Test**: Can be fully tested by a logged-in student creating, viewing, and updating their hardware profile with PDF-specified hardware options

### Tests for User Story 2 ⚠️

- [ ] T031 [P] [US2] Contract test for hardware config endpoints in backend/tests/unit/test_hardware.py::test_create_hardware_config
- [ ] T032 [P] [US2] Validation test for PDF hardware enums in backend/tests/unit/test_hardware.py::test_hardware_type_validation
- [ ] T033 [P] [US2] Integration test for hardware profile CRUD in backend/tests/integration/test_hardware_profile.py

### Implementation for User Story 2

- [ ] T034 [P] [US2] Create HardwareConfig model in backend/models/hardware_config.py with hardware_type, gpu_model, gpu_vram_gb, ubuntu_version, edge_kit_type, jetpack_version, robot_model, sensor_model, additional_specs fields
- [ ] T035 [P] [US2] Add CHECK constraints to HardwareConfig in backend/models/hardware_config.py for hardware_type enum, edge_kit_type enum, robot_model enum
- [ ] T036 [US2] Create hardware profile API endpoints in backend/api/hardware.py: GET /api/student/hardware-config, PUT /api/student/hardware-config
- [ ] T037 [US2] Add validation for PDF-specified hardware values in backend/api/hardware.py (sim_rig requires gpu_vram_gb >= 12, edge_kit requires edge_kit_type)
- [ ] T038 [US2] Implement hardware config service in backend/services/hardware_config_service.py with get_config, update_config functions
- [ ] T039 [US2] Add error handling for invalid hardware types, missing required fields in backend/api/hardware.py
- [ ] T040 [US2] Create HardwareProfileForm component in docusaurus-textbook/src/components/HardwareProfileForm.jsx with Sim Rig/Edge Kit toggle and PDF-specified dropdowns
- [ ] T041 [US2] Create useHardwareProfile hook in docusaurus-textbook/src/hooks/useHardwareProfile.js for form state management
- [ ] T042 [US2] Add tooltips explaining hardware differences (Sim Rig vs Edge Kit) in docusaurus-textbook/src/components/HardwareProfileForm.jsx
- [ ] T043 [US2] Create user profile page in docusaurus-textbook/src/pages/profile.jsx to display and edit hardware profile
- [ ] T044 [US2] Add logging for hardware profile updates in backend/services/hardware_config_service.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - students can register/login AND save their hardware profile

---

## Phase 5: User Story 3 - Receive Hardware-Aware Chatbot Responses (Priority: P3)

**Goal**: Chatbot automatically adjusts technical advice based on student's hardware setup (Sim Rig vs Edge Kit) with PDF Page 5 and Page 8 prioritization

**Independent Test**: Can be fully tested by asking the chatbot a technical question and verifying the response includes hardware-specific instructions matching the student's saved profile

### Tests for User Story 3 ⚠️

- [ ] T045 [P] [US3] Contract test for chat endpoint with personalization in backend/tests/integration/test_chat_personalization.py::test_chat_with_hardware_context
- [ ] T046 [P] [US3] Test Edge Kit inference advice in backend/tests/integration/test_chat_personalization.py::test_edge_kit_inference_response
- [ ] T047 [P] [US3] Test Sim Rig workstation advice in backend/tests/integration/test_chat_personalization.py::test_sim_rig_workstation_response
- [ ] T048 [P] [US3] Test context injection service in backend/tests/unit/test_hardware_context_service.py

### Implementation for User Story 3

- [ ] T049 [P] [US3] Create HardwareContextService in backend/services/hardware_context_service.py with get_user_context, inject_context functions
- [ ] T050 [P] [US3] Implement PDF Page 5 logic in backend/services/hardware_context_service.py for Hardware Reality constraints
- [ ] T051 [P] [US3] Implement PDF Page 8 logic in backend/services/hardware_context_service.py for Inference/Sim-to-Real prioritization
- [ ] T052 [US3] Update RAG pipeline in backend/services/rag_pipeline.py to accept hardware_context parameter and call HardwareContextService
- [ ] T053 [US3] Modify Grok API prompt injection in backend/llm/grok_client.py to include hardware context with XML delimiters
- [ ] T054 [US3] Update POST /api/chat endpoint in backend/api/chat.py to retrieve user hardware profile and pass to RAG pipeline
- [ ] T055 [US3] Add hardware_context_used, hardware_type_applied, pdf_pages_referenced fields to chat response in backend/api/chat.py
- [ ] T056 [US3] Implement graceful degradation for missing hardware profile in backend/services/hardware_context_service.py (generic responses or prompt to setup profile)
- [ ] T057 [US3] Add hardware_profile_snapshot to ChatMessage model in backend/models/chat_message.py
- [ ] T058 [US3] Add pdf_page_references field to ChatMessage model in backend/models/chat_message.py
- [ ] T059 [US3] Add logging for hardware context injections in backend/services/hardware_context_service.py
- [ ] T060 [US3] Test hardware-aware chat with Edge Kit profile (Jetson Orin Nano) to verify inference-optimized advice
- [ ] T061 [US3] Test hardware-aware chat with Sim Rig profile (RTX 4070 Ti) to verify workstation-optimized advice

**Checkpoint**: All user stories should now be independently functional - chatbot provides hardware-aware responses based on PDF specifications

---

## Phase 6: User Story 4 - Track Weekly Curriculum Progress (Priority: P4)

**Goal**: System tracks student progress through 13-week curriculum with completion timestamps and scores

**Independent Test**: Can be fully tested by a student completing a week and verifying their progress is recorded and visible in their profile

### Tests for User Story 4 ⚠️

- [ ] T062 [P] [US4] Contract test for curriculum progress endpoints in backend/tests/unit/test_curriculum.py::test_record_progress
- [ ] T063 [P] [US4] Validation test for week number constraints (1-13) in backend/tests/unit/test_curriculum.py::test_week_number_validation
- [ ] T064 [P] [US4] Integration test for progress tracking in backend/tests/integration/test_curriculum_progress.py

### Implementation for User Story 4

- [ ] T065 [P] [US4] Create CurriculumProgress model in backend/models/curriculum_progress.py with student_profile_id FK, week_number, module_id, completed_at, score_percentage, notes fields
- [ ] T066 [P] [US4] Add CHECK constraints to CurriculumProgress in backend/models/curriculum_progress.py for week_number (1-13) and score_percentage (0-100)
- [ ] T067 [P] [US4] Add unique constraint for (student_profile_id, week_number, module_id) in backend/models/curriculum_progress.py
- [ ] T068 [US4] Create curriculum progress API endpoints in backend/api/curriculum.py: GET /api/student/curriculum-progress, POST /api/student/curriculum-progress
- [ ] T069 [US4] Implement curriculum progress service in backend/services/curriculum_service.py with record_progress, get_progress, get_summary functions
- [ ] T070 [US4] Add validation for week_number (1-13), module_id pattern in backend/api/curriculum.py
- [ ] T071 [US4] Add error handling for duplicate progress records, invalid week numbers in backend/api/curriculum.py
- [ ] T072 [US4] Create CurriculumProgress component in docusaurus-textbook/src/components/CurriculumProgress.jsx to display completed weeks and remaining weeks
- [ ] T073 [US4] Create progress page in docusaurus-textbook/src/pages/progress.jsx showing 13-week curriculum timeline
- [ ] T074 [US4] Add progress summary calculation (total_weeks_completed) in backend/services/curriculum_service.py
- [ ] T075 [US4] Update StudentProfile model to cache total_weeks_completed in backend/models/student_profile.py
- [ ] T076 [US4] Add logging for curriculum progress updates in backend/services/curriculum_service.py

**Checkpoint**: User Stories 1-4 all functional - students can register, save hardware profile, get hardware-aware chat responses, and track curriculum progress

---

## Phase 7: User Story 5 - Access Protected API Endpoints Securely (Priority: P5)

**Goal**: All API endpoints (chat, ingest, profile) require valid authentication tokens with proper error responses

**Independent Test**: Can be fully tested by attempting to access protected endpoints without authentication (should fail with 401) and with valid authentication (should succeed)

### Tests for User Story 5 ⚠️

- [ ] T077 [P] [US5] Test 401 Unauthorized for unauthenticated chat request in backend/tests/integration/test_protected_endpoints.py::test_chat_requires_auth
- [ ] T078 [P] [US5] Test 401 Unauthorized for unauthenticated profile request in backend/tests/integration/test_protected_endpoints.py::test_profile_requires_auth
- [ ] T079 [P] [US5] Test 401 Unauthorized for unauthenticated ingest request in backend/tests/integration/test_protected_endpoints.py::test_ingest_requires_auth
- [ ] T080 [P] [US5] Test successful authenticated request in backend/tests/integration/test_protected_endpoints.py::test_authenticated_request

### Implementation for User Story 5

- [ ] T081 [P] [US5] Update POST /api/chat endpoint in backend/api/chat.py to require authentication via Depends(get_current_user)
- [ ] T082 [P] [US5] Update POST /api/ingest endpoint in backend/api/ingest.py to require authentication via Depends(get_current_user)
- [ ] T083 [US5] Add 401 Unauthorized error responses to all protected endpoints in backend/api/*.py
- [ ] T084 [US5] Implement session expiration handling with clear error messages in backend/auth/middleware.py
- [ ] T085 [US5] Add rate limiting to authentication endpoints (10 req/min per IP) in backend/auth/middleware.py
- [ ] T086 [US5] Add rate limiting to chat endpoint (30 req/min per user) in backend/auth/middleware.py
- [ ] T087 [US5] Implement CSRF protection for state-changing operations in backend/auth/middleware.py
- [ ] T088 [US5] Add security event logging for authentication failures, rate limit violations in backend/utils/logger.py
- [ ] T089 [US5] Test all protected endpoints return 401 without valid session cookie
- [ ] T090 [US5] Test all protected endpoints succeed with valid session cookie
- [ ] T091 [US5] Test session expiration prompts user to log in again in frontend

**Checkpoint**: All 5 user stories complete and independently functional - full authentication security implemented across all endpoints

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories and final validation

- [ ] T092 [P] Create database migration script in backend/alembic/versions/002_add_chat_tables.py for ChatSession and ChatMessage models
- [ ] T093 [P] Create chat history API endpoints in backend/api/chat_history.py: GET /api/student/chat-history, GET /api/student/chat-history/{session_id}
- [ ] T094 [P] Create ChatHistory component in docusaurus-textbook/src/components/ChatHistory.jsx for viewing past conversations
- [ ] T095 Update quickstart.md with complete setup instructions and testing procedures
- [ ] T096 [P] Run full test suite: pytest backend/tests/ -v
- [ ] T097 [P] Validate API contracts against OpenAPI spec in specs/001-hardware-aware-auth/contracts/api-contracts.yaml
- [ ] T098 Documentation updates: Add API documentation in backend/docs/ for all endpoints
- [ ] T099 Security hardening: Review all endpoints for proper authentication, authorization, input validation
- [ ] T100 Performance optimization: Add database indexes on frequently queried fields (email, user_id, session_id)
- [ ] T101 [P] Test complete user journey: register → login → setup hardware profile → chat with personalization → track progress
- [ ] T102 Validate PDF Page 5 and Page 8 references are correctly applied in hardware-aware responses

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 for hardware profile but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Cross-cutting concern, applies to all stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T002, T003, T005 can run in parallel
- **Foundational Phase**: T006, T007, T008, T009, T010, T011, T013 can run in parallel
- **User Story 1 Tests**: T014, T015, T016, T017 can run in parallel
- **User Story 1 Models**: T018, T019 can run in parallel
- **User Story 2 Tests**: T031, T032, T033 can run in parallel
- **User Story 2 Models**: T034, T035 can run in parallel
- **User Story 3 Tests**: T045, T046, T047, T048 can run in parallel
- **User Story 3 Services**: T049, T050, T051 can run in parallel
- **User Story 4 Tests**: T062, T063, T064 can run in parallel
- **User Story 4 Models**: T065, T066, T067 can run in parallel
- **User Story 5 Tests**: T077, T078, T079, T080 can run in parallel
- **Polish Phase**: T092, T093, T094, T096, T097, T100 can run in parallel

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 2 (Hardware Profile)
   - Developer C: User Story 4 (Curriculum Progress)
3. After US2 complete:
   - Developer A: User Story 3 (Hardware-Aware Chat) - depends on hardware profile
4. After all stories complete:
   - Team: Polish & Cross-Cutting Concerns

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
pytest backend/tests/unit/test_auth.py::test_register_student
pytest backend/tests/unit/test_auth.py::test_login_student
pytest backend/tests/integration/test_github_oauth.py
pytest backend/tests/unit/test_session_validator.py

# Launch all models for User Story 1 together:
# T018: Create User model in backend/models/user.py
# T019: Create StudentProfile model in backend/models/student_profile.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T013) - CRITICAL blocker
3. Complete Phase 3: User Story 1 (T014-T030)
4. **STOP and VALIDATE**: Test registration, login, GitHub OAuth, auth state in UI
5. Deploy/demo if ready - students can now register and sign in

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP: Authentication!)
3. Add User Story 2 → Test independently → Deploy/Demo (Hardware Profile!)
4. Add User Story 3 → Test independently → Deploy/Demo (Hardware-Aware Chat!)
5. Add User Story 4 → Test independently → Deploy/Demo (Curriculum Tracking!)
6. Add User Story 5 → Test independently → Deploy/Demo (Full Security!)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With 3 developers:

**Week 1**: Team completes Setup + Foundational together

**Week 2**:
- Dev A: User Story 1 (T014-T030) - Authentication
- Dev B: User Story 2 (T031-T044) - Hardware Profile
- Dev C: User Story 4 (T062-T076) - Curriculum Progress

**Week 3**:
- Dev A+B: User Story 3 (T045-T061) - Hardware-Aware Chat (needs US2 complete)
- Dev C: Complete User Story 4 if not done

**Week 4**:
- Team: User Story 5 (T077-T091) - Security hardening
- Team: Polish (T092-T102)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **Definition of Done**: Student can sign up, save hardware profile (Edge Kit/Sim Rig), chatbot acknowledges hardware in responses, API returns 401 without valid session
