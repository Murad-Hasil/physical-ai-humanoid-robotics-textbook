# Tasks: Phase 7 Final Intelligence

**Input**: Design documents from `/specs/001-phase-7-intelligence/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification or if user requests TDD approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **Frontend**: `docusaurus-textbook/` at repository root
- Paths shown below are absolute from repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create Alembic migration for Phase 7 models in `backend/migrations/versions/`
- [ ] T002 [P] Install additional backend dependencies (redis for caching if needed) in `backend/requirements.txt`
- [ ] T003 [P] Install additional frontend dependencies in `docusaurus-textbook/package.json`
- [ ] T004 [P] Create directory structure for new components:
  - `docusaurus-textbook/src/context/`
  - `docusaurus-textbook/src/components/onboarding/`
  - `docusaurus-textbook/src/components/personalization/`
  - `docusaurus-textbook/src/components/translation/`
  - `docusaurus-textbook/src/services/`
  - `backend/services/`
  - `backend/llm/prompts/`
  - `backend/ingestion/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create `backend/models/curriculum.py` with CurriculumWeek, Chapter, ChapterSummary, Translation models
- [ ] T006 [P] Extend `backend/models/student_profile.py` with `skill_level` column
- [ ] T007 [P] Create Alembic migration for `skill_level` column and new curriculum tables
- [ ] T008 [P] Run migration: `alembic upgrade head` and verify tables created
- [ ] T009 [P] Create Pydantic schemas in `backend/schemas/user_profile.py` (SkillLevel, HardwareType enums, StudentProfileUpdate, HardwareConfigCreate)
- [ ] T010 [P] Create Pydantic schemas in `backend/schemas/curriculum.py` (CurriculumWeekBase, ChapterBase, ChapterSummaryResponse, TranslationResponse)
- [ ] T011 [P] Create `backend/services/curriculum_service.py` with CRUD operations for curriculum content
- [ ] T012 [P] Create `backend/llm/prompts/personalization.py` with PERSONALIZATION_PROMPT template
- [ ] T013 [P] Create `backend/llm/prompts/translation.py` with TRANSLATION_PROMPT template and technical term glossary
- [ ] T014 [P] Create `docusaurus-textbook/src/context/PersonalizationContext.tsx` with PersonalizationProvider
- [ ] T015 [P] Create `docusaurus-textbook/src/services/api.ts` base API client with auth interceptors
- [ ] T016 [P] Create `docusaurus-textbook/src/services/personalization.ts` API service layer
- [ ] T017 [P] Create `docusaurus-textbook/src/services/translations.ts` API service layer

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Smart Onboarding with Hardware Profile (Priority: P1) 🎯 MVP

**Goal**: Enable users to provide hardware setup and skill level during signup so the system can personalize content

**Independent Test**: Can be fully tested by completing the signup flow with various hardware configurations and verifying the data is captured and stored correctly

### Implementation for User Story 1

- [ ] T018 [P] [US1] Create `backend/api/v1/endpoints/user_profiles.py` with GET/PUT endpoints for user profile management
- [ ] T019 [P] [US1] Create `backend/api/v1/endpoints/hardware_config.py` with PUT endpoint for hardware config updates
- [ ] T020 [US1] Register user profile and hardware config routers in `backend/main.py`
- [ ] T021 [P] [US1] Create `docusaurus-textbook/src/components/onboarding/SkillLevelSelector.tsx` with beginner/intermediate/advanced options
- [ ] T022 [P] [US1] Create `docusaurus-textbook/src/components/onboarding/HardwareProfileForm.tsx` with hardware type selector and conditional fields
- [ ] T023 [US1] Create `docusaurus-textbook/src/pages/signup.tsx` integrating email/password, SkillLevelSelector, and HardwareProfileForm
- [ ] T024 [US1] Create `docusaurus-textbook/src/pages/profile.tsx` with HardwareProfileForm and SkillLevelSelector for editing
- [ ] T025 [US1] Update PersonalizationContext to sync with backend on auth state changes
- [ ] T026 [US1] Add localStorage persistence for unauthenticated users in PersonalizationContext
- [ ] T027 [US1] Add validation for hardware profile fields (GPU VRAM range, required fields per hardware type)
- [ ] T028 [US1] Add error handling and toast notifications for profile save failures

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - users can signup with hardware profile and edit it later

---

## Phase 4: User Story 2 - Personalized Chapter Summaries (Priority: P2)

**Goal**: Dynamically generate chapter summaries based on user's hardware profile and skill level

**Independent Test**: Can be fully tested by viewing any chapter with different user profiles and verifying the summary content changes appropriately

### Implementation for User Story 2

- [ ] T029 [P] [US2] Create `backend/services/personalization_service.py` with `get_or_generate_summary()` method
- [ ] T030 [P] [US2] Create `backend/llm/grok_client.py` wrapper for Grok API calls (reuse existing if available)
- [ ] T031 [US2] Implement `generate_personalized_summary()` method in PersonalizationService using Grok API
- [ ] T032 [US2] Implement `get_personalized_summary()` endpoint in `backend/api/v1/endpoints/personalization.py`
- [ ] T033 [US2] Add caching logic: check database first, generate only if not exists
- [ ] T034 [US2] Add admin endpoint for regenerating summaries in `backend/api/v1/endpoints/personalization.py`
- [ ] T035 [P] [US2] Create `docusaurus-textbook/src/components/personalization/PersonalizedSummary.tsx` component
- [ ] T036 [P] [US2] Create `docusaurus-textbook/src/components/personalization/HardwareIndicator.tsx` component
- [ ] T037 [US2] Swizzle Docusaurus DocItem: `npx docusaurus swizzle @docusaurus/theme-classic DocItem --typescript --eject`
- [ ] T038 [US2] Update `docusaurus-textbook/src/theme/DocItem/index.tsx` to include PersonalizedSummary and HardwareIndicator
- [ ] T039 [US2] Add personalization toggle logic (show/hide personalized summaries based on user preference)
- [ ] T040 [US2] Add loading states and error handling for summary fetching
- [ ] T041 [US2] Add CSS styling for personalized summary components in `docusaurus-textbook/src/css/custom.css`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - chapter summaries adapt to user hardware and skill level

---

## Phase 5: User Story 3 - Multi-Language Translation Toggle (Priority: P3)

**Goal**: Enable users to toggle chapter content between English and Roman Urdu

**Independent Test**: Can be fully tested by viewing any chapter, activating the translation toggle, and verifying the content switches between English and Roman Urdu

### Implementation for User Story 3

- [ ] T042 [P] [US3] Create `backend/services/translation_service.py` with `get_or_generate_translation()` method
- [ ] T043 [US3] Implement `generate_translation()` method using Grok API with preservation rules
- [ ] T044 [US3] Create `backend/api/v1/endpoints/translations.py` with GET endpoint for chapter translation
- [ ] T045 [US3] Create admin PUT endpoint for updating translations in `backend/api/v1/endpoints/translations.py`
- [ ] T046 [US3] Create GET `/api/v1/translations/status` endpoint for translation coverage stats
- [ ] T047 [P] [US3] Create `docusaurus-textbook/src/components/translation/TranslationToggle.tsx` component
- [ ] T048 [P] [US3] Create `docusaurus-textbook/src/components/translation/TranslationProgress.tsx` component
- [ ] T049 [US3] Update DocItem wrapper to include TranslationToggle in header
- [ ] T050 [US3] Implement language switching logic in PersonalizationContext
- [ ] T051 [US3] Add API call to fetch translation when toggle is activated
- [ ] T052 [US3] Implement "AI Translation in progress" indicator for draft translations
- [ ] T053 [US3] Add fallback to English content when translation not available (FR-017)
- [ ] T054 [US3] Persist language preference in localStorage and sync with backend for authenticated users
- [ ] T055 [US3] Add CSS styling for translation toggle and in-progress indicator in `docusaurus-textbook/src/css/custom.css`

**Checkpoint**: All user stories should now be independently functional - users can toggle between English and Roman Urdu

---

## Phase 6: User Story 4 - Complete Curriculum Content Access (Priority: P4)

**Goal**: Populate system with all 13 weeks of technical curriculum content, including Weeks 7-8 (Neural Networks & RL)

**Independent Test**: Can be fully tested by browsing the curriculum structure and verifying all 13 weeks of content are accessible and properly organized. Specifically verify Weeks 7-8 content is indexed and chatbot can answer RL questions.

### Implementation for User Story 4

- [ ] T056 [P] [US4] Create `backend/ingestion/curriculum_parser.py` with `parse_week_folder()` function
- [ ] T057 [P] [US4] Create `backend/ingestion/ingest_curriculum.py` batch ingestion script
- [ ] T058 [US4] Create POST `/api/v1/curriculum/ingest` endpoint in `backend/api/v1/endpoints/curriculum.py`
- [ ] T059 [US4] Create GET `/api/v1/curriculum/weeks` endpoint for listing all weeks
- [ ] T060 [US4] Create GET `/api/v1/curriculum/weeks/{week_number}` endpoint for week details
- [ ] T061 [US4] Create curriculum folder structure: `docusaurus-textbook/docs/week-01/` through `week-13/`
- [ ] T062 [US4] Create `_category_.json` files for each week with metadata
- [ ] T063 [US4] Update `docusaurus-textbook/sidebars.js` to include weeks 1-13
- [ ] T064 [US4] Execute ingestion script to populate database with curriculum content
- [ ] T065 [US4] Verify Chapter table has entries for all 13 weeks
- [ ] T066 [US4] Implement progress tracking integration (update `total_weeks_completed` in StudentProfile)
- [ ] T067 [US4] Add curriculum overview page showing all 13 weeks with progress indicators
- [ ] T068 [US4] Test personalized summaries are generated for all ingested chapters

### RL & Advanced Content Specific Tasks (Weeks 7-8)

**Goal**: Ensure Weeks 7-8 (Neural Networks & Reinforcement Learning) are properly ingested with technical term handling

**Independent Test**: Verify "Translate to Urdu" button correctly handles technical terms like "Proximal Policy Optimization" and "Reward Function". Chatbot should answer: "Explain the PPO algorithm for humanoid walking."

- [ ] T069 [P] [US4] Verify `docusaurus-textbook/docs/week-07/neural-networks-robotics.md` exists and contains proper frontmatter
- [ ] T070 [P] [US4] Verify `docusaurus-textbook/docs/week-08/reinforcement-learning.md` exists and contains proper frontmatter
- [ ] T071 [US4] Add RL-specific technical terms to translation glossary in `backend/llm/prompts/translation.py`:
  - "Proximal Policy Optimization", "PPO", "Reward Function", "Policy Gradient", "Value Function", "Actor-Critic"
- [ ] T072 [US4] Execute ingestion script for Weeks 7-8: `python -m ingestion.ingest_curriculum --path docs/week-07 docs/week-08`
- [ ] T073 [US4] Verify Chapter table shows 8 weeks of data (Weeks 1-8 complete)
- [ ] T074 [US4] Test translation toggle on Week 8 RL content - verify technical terms preserved in English
- [ ] T075 [US4] Test chatbot query: "Explain the PPO algorithm for humanoid walking" - verify RAG retrieves Week 8 content
- [ ] T076 [US4] Test chatbot query: "How do neural networks apply to robotics?" - verify RAG retrieves Week 7 content
- [ ] T077 [US4] Verify personalized summaries for RL content adapt to hardware (edge vs desktop training considerations)

**Checkpoint**: Complete curriculum is accessible with personalization applied to all 13 weeks. Weeks 7-8 RL content specifically tested for translation quality and chatbot retrieval.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories

- [ ] T078 [P] Update `.env.example` with all new environment variables (GROK_API_KEY, QDRANT_URL, etc.)
- [ ] T079 [P] Add structured logging to all new services (personalization, translation, curriculum)
- [ ] T080 [P] Add database indexes for performance:
  - `idx_chapter_summaries_lookup` on (chapter_id, hardware_profile_type, skill_level)
  - `idx_translations_chapter_lang` on (chapter_id, language_code)
- [ ] T081 [P] Add API documentation comments to all new endpoints
- [ ] T082 [P] Verify Swagger UI at `/docs` shows all new endpoints correctly
- [ ] T083 [P] Run quickstart.md validation - ensure all setup steps work
- [ ] T084 [P] Test signup flow end-to-end with different hardware profiles
- [ ] T085 [P] Test translation toggle across multiple chapters including RL content
- [ ] T086 [P] Verify personalized summaries load within 2 seconds (p90)
- [ ] T087 [P] Add "AI Translation in progress" indicator styling per spec
- [ ] T088 [P] Verify glassmorphism theme consistency across all new components
- [ ] T089 [P] Update README.md with Phase 7 feature documentation
- [ ] T090 [P] Verify admin endpoints are properly protected with is_admin check
- [ ] T091 [P] Test curriculum ingestion with sample markdown files
- [ ] T092 [P] Verify chatbot can answer: "What is Domain Randomization in Isaac Gym?"
- [ ] T093 [P] Verify chatbot can answer: "Explain the PPO algorithm for humanoid walking"
- [ ] T094 [P] Test translation preservation of RL technical terms (PPO, Reward Function, Policy Gradient)
- [ ] T095 [P] Verify Weeks 7-8 content appears in sidebar and is accessible
- [ ] T096 [P] Run end-to-end test: Signup → Set Hardware → View Week 8 → Toggle Translation → Ask Chatbot

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent, but benefits from US2 personalization

### Within Each User Story

- Models before services
- Services before endpoints
- Backend endpoints before frontend integration
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all backend tasks for User Story 1 together:
Task: "Create user_profiles endpoint in backend/api/v1/endpoints/user_profiles.py"
Task: "Create hardware_config endpoint in backend/api/v1/endpoints/hardware_config.py"

# Launch all frontend components for User Story 1 together:
Task: "Create SkillLevelSelector.tsx component"
Task: "Create HardwareProfileForm.tsx component"
```

---

## Parallel Example: User Story 2

```bash
# Launch service and endpoint tasks together:
Task: "Create personalization_service.py with get_or_generate_summary()"
Task: "Create grok_client.py wrapper for API calls"

# Launch frontend components together:
Task: "Create PersonalizedSummary.tsx component"
Task: "Create HardwareIndicator.tsx component"
```

---

## Parallel Example: User Story 3

```bash
# Launch translation service and endpoints together:
Task: "Create translation_service.py"
Task: "Create translations.py endpoint"

# Launch frontend components together:
Task: "Create TranslationToggle.tsx"
Task: "Create TranslationProgress.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test signup flow with hardware profile
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo (Complete!)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Smart Onboarding)
   - Developer B: User Story 2 (Personalized Summaries)
   - Developer C: User Story 3 (Translation Toggle)
   - Developer D: User Story 4 (Curriculum Ingestion)
3. Stories complete and integrate independently
4. Team reconvenes for Phase 7: Polish

---

## Task Summary

**Total Tasks**: 96

**By Phase**:
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 13 tasks
- Phase 3 (US1 - Smart Onboarding): 11 tasks
- Phase 4 (US2 - Personalized Summaries): 13 tasks
- Phase 5 (US3 - Translation Toggle): 14 tasks
- Phase 6 (US4 - Curriculum Content): 22 tasks (13 general + 9 RL-specific for Weeks 7-8)
- Phase 7 (Polish): 19 tasks

**By User Story**:
- US1 (P1): 11 tasks
- US2 (P2): 13 tasks
- US3 (P3): 14 tasks
- US4 (P4): 22 tasks (includes Weeks 7-8 RL content ingestion)

**Parallel Opportunities**:
- Phase 1: 3/4 tasks can run in parallel
- Phase 2: 11/13 tasks can run in parallel
- Phase 3: 4/11 tasks can run in parallel
- Phase 4: 4/13 tasks can run in parallel
- Phase 5: 4/14 tasks can run in parallel
- Phase 6: 4/22 tasks can run in parallel (RL verification tasks)
- Phase 7: 17/19 tasks can run in parallel

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
