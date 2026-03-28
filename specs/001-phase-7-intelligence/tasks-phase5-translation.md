# Tasks: Phase 7 - Translation Engine & API Activation (Phase 5)

**Input**: Design documents from `/specs/001-phase-7-intelligence/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)
**Previous Work**: Phases 1-4 complete (Setup, Foundational, Smart Onboarding, Personalization Engine)

**Tests**: Tests are OPTIONAL for this feature. Not included in this task list. Add manually if TDD approach is desired.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **Frontend**: `docusaurus-textbook/` at repository root
- Paths shown below are absolute from repository root

---

## Phase 1-2: Setup & Foundational (Already Complete ✓)

**Status**: 17/17 tasks complete

---

## Phase 3: User Story 1 - Smart Onboarding (Already Complete ✓)

**Status**: 11/11 tasks complete

---

## Phase 4: User Story 2 - Personalized Summaries (Already Complete ✓)

**Status**: PersonalizationService implemented

---

## Phase 5: User Story 3 - Multi-Language Translation (Priority: P3) 🎯

**Goal**: Implement Roman Urdu translation engine with technical term preservation and API endpoints

**Independent Test**: Toggle to Roman Urdu on any chapter, verify translation preserves technical terms (URDF, ROS 2, CUDA) while translating prose

### Implementation for User Story 3

- [ ] T029 [P] [US3] Implement `TranslationService.get_translation()` in `backend/services/translation_service.py`:
  - Query Translation table for chapter_id and language_code ('ur-Latn')
  - Return translation if exists with status check ('published' or 'in_review')
  - Return None if not found (triggers "AI Translation in progress" indicator)
  - Return dictionary with translated_content, status, updated_at, language_code

- [ ] T030 [P] [US3] Implement `TranslationService.create_or_update_translation()` in `backend/services/translation_service.py`:
  - Insert new Translation or update existing record
  - Call Grok API with TRANSLATION_PROMPT_TEMPLATE if content not provided manually
  - Set status to 'draft' for AI-generated, allow manual override to 'published'
  - Store translated_by field ("grok-2-ai" or user ID for manual)
  - Return dictionary with translation details

- [ ] T031 [P] [US3] Implement technical term validation in `backend/services/translation_service.py`:
  - Import TECHNICAL_TERMS_PRESERVATION set from translation prompts
  - Create `validate_translation_preservation()` function
  - Check if terms like "URDF", "ROS 2", "CUDA" appear in translation
  - Log warnings for potentially over-translated terms
  - Return list of validation issues for review

- [ ] T032 [P] [US3] Add caching logic using Translation table in `backend/services/translation_service.py`:
  - Query Translation table before calling Grok API
  - Return cached translation if status is 'published'
  - For 'draft' status, regenerate only if older than 7 days
  - Log cache hits vs API calls for cost tracking
  - Implement cache invalidation on content update

- [ ] T033 [P] [US3] Implement `GET /api/v1/chapters/{chapter_id}/translation` endpoint in `backend/api/v1/endpoints/translations.py`:
  - Extract chapter_id from path parameters
  - Get lang from query parameter (default: 'ur-Latn')
  - Get current user's language preference from JWT/auth context
  - Call `TranslationService.get_translation()`
  - Return 404 with error message if translation not found (frontend shows indicator)
  - Return 200 with `TranslationResponse` schema if found
  - Add structured logging for analytics

- [ ] T034 [P] [US3] Implement `PUT /api/v1/chapters/{chapter_id}/translation` endpoint in `backend/api/v1/endpoints/translations.py`:
  - Admin-only access check (verify current_user.is_admin)
  - Accept `TranslationUpdate` schema with translated_content, status, review_notes
  - Call `TranslationService.create_or_update_translation()`
  - Support manual translation updates by admins
  - Return `TranslationResponse` with updated translation
  - Log admin actions for audit trail

- [ ] T035 [P] [US3] Implement `GET /api/v1/translations/status` endpoint in `backend/api/v1/endpoints/translations.py`:
  - Query Translation table for counts grouped by status
  - Calculate total chapters from Chapter table
  - Calculate coverage percentage: (published_count / total_chapters) * 100
  - Group statistics by language_code
  - Return `TranslationStatsResponse` with:
    - total_chapters: int
    - translated_chapters: int
    - published_chapters: int
    - draft_chapters: int
    - coverage_percentage: float
    - by_language: Dict[language_code, stats]

- [ ] T036 [US3] Update DocItem wrapper in `docusaurus-textbook/src/theme/DocItem/index.tsx`:
  - Import TranslationToggle and TranslationProgress components
  - Add loading state management for translation fetch
  - Call GET `/api/v1/chapters/{id}/translation` on toggle activation
  - Handle 404 response by showing "AI Translation in progress" indicator
  - Handle 200 response by displaying translated content
  - Preserve code blocks and technical terms in rendered output

- [ ] T037 [US3] Add "AI Translation in progress" indicator in `docusaurus-textbook/src/components/translation/TranslationProgress.tsx`:
  - Display yellow pulse animation for 'draft' status
  - Show "AI Translation in progress" text per spec FR-017
  - Display orange indicator for 'in_review' status
  - Show green checkmark for 'published' status
  - Add tooltip with status description

- [ ] T038 [US3] Handle loading state in `docusaurus-textbook/src/components/translation/TranslationToggle.tsx`:
  - Show spinner/pulse animation while fetching translation
  - Disable toggle during fetch to prevent multiple requests
  - Display "Loading..." text during fetch
  - Re-enable toggle on response (success or error)

- [ ] T039 [US3] Add error handling for translation API calls in `docusaurus-textbook/src/theme/DocItem/index.tsx`:
  - Catch 404 errors and show "AI Translation in progress" indicator
  - Catch 500 errors and show user-friendly error message
  - Catch network errors and suggest retry
  - Log errors for debugging
  - Preserve English content as fallback per spec

**Checkpoint**: User Story 3 complete - Roman Urdu translation works with technical term preservation, "AI Translation in progress" indicator shows for unpublished translations

---

## Phase 6: User Story 2 - API Endpoint Completion (Priority: P2)

**Goal**: Complete API endpoints for personalized summaries with user context integration

**Independent Test**: Call summary endpoint with different user profiles, verify response includes hardware-aware and skill-level-aware content

### Implementation for User Story 2

- [ ] T040 [P] [US2] Implement `GET /api/v1/chapters/{chapter_id}/summary` endpoint in `backend/api/v1/endpoints/personalization.py`:
  - Extract chapter_id from path parameters
  - Get hardware_profile and skill_level from query params (optional)
  - If not provided, extract from current user's profile via JWT/auth context
  - Call `PersonalizationService.get_or_generate_summary()`
  - Return 404 if chapter not found
  - Return 200 with `ChapterSummaryResponse` schema
  - Add structured logging with chapter_id, hardware_profile, skill_level

- [ ] T041 [P] [US2] Add user context integration in `backend/api/v1/endpoints/personalization.py`:
  - Import `require_auth` decorator from auth middleware
  - Extract current_user from JWT token
  - Query StudentProfile and HardwareConfig for current user
  - Use user's hardware_type and skill_level as defaults
  - Allow query param overrides for admin testing
  - Handle unauthenticated users with default profile

- [ ] T042 [P] [US2] Add error handling and retry logic in `backend/api/v1/endpoints/personalization.py`:
  - Catch PersonalizationService errors
  - Handle GrokAPIError with graceful fallback
  - Return cached summary on API failure (if available)
  - Log error details for debugging
  - Return 503 Service Unavailable on persistent failure
  - Add retry-after header for rate limit scenarios

- [ ] T043 [US2] Update DocItem wrapper in `docusaurus-textbook/src/theme/DocItem/index.tsx`:
  - Import PersonalizedSummary component
  - Fetch summary on component mount when personalizationEnabled is true
  - Pass hardware_profile and skill_level from PersonalizationContext
  - Handle loading state with skeleton loader
  - Handle error state with user-friendly message
  - Re-fetch when context values change

**Checkpoint**: User Story 2 API complete - endpoints return personalized summaries with user context

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final polish and integration testing

- [ ] T044 [P] Add integration tests for translation flow in `backend/tests/api/test_translations.py`:
  - Test GET /api/v1/chapters/{id}/translation with existing translation
  - Test GET with non-existent translation (404 response)
  - Test PUT with admin credentials
  - Test GET /api/v1/translations/status
  - Verify technical terms preserved in responses

- [ ] T045 [P] Add integration tests for personalization flow in `backend/tests/api/test_personalization.py`:
  - Test GET /api/v1/chapters/{id}/summary with different hardware profiles
  - Test GET with different skill levels
  - Test user context extraction from JWT
  - Verify caching behavior (second call faster)
  - Test error handling with mocked API failures

- [ ] T046 [P] Add frontend integration tests in `docusaurus-textbook/src/__tests__/DocItem.test.tsx`:
  - Test translation toggle click triggers API call
  - Test "AI Translation in progress" indicator shows for 404
  - Test translated content displays correctly
  - Test personalized summary loads when enabled
  - Test loading states during API calls

- [ ] T047 [P] Performance optimization in `backend/services/translation_service.py`:
  - Add database indexes on (chapter_id, language_code)
  - Implement LRU cache for hot translations (optional Redis)
  - Add query optimization for status endpoint
  - Profile and optimize slow queries

- [ ] T048 [P] Security hardening in `backend/api/v1/endpoints/translations.py` and `personalization.py`:
  - Validate chapter_id is valid UUID
  - Sanitize translated content before returning
  - Rate limit translation requests per user
  - Audit admin translation updates
  - Add input validation for all query parameters

- [ ] T049 [P] Documentation updates in `docs/api/`:
  - Add API documentation for translation endpoints
  - Add API documentation for personalization endpoints
  - Document error codes and responses
  - Add usage examples with curl commands
  - Update README with Phase 5 features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phases 1-4**: ✅ Already complete
- **Phase 5 (US3)**: Can start immediately - depends on Translation table existing
- **Phase 6 (US2 API)**: Can start immediately - depends on PersonalizationService being complete
- **Phase 7 (Polish)**: Depends on Phases 5-6 completion

### User Story Dependencies

- **User Story 3 (P3 - Translation)**: No dependencies on other stories - independent
- **User Story 2 (P2 - Personalization API)**: Depends on PersonalizationService (complete)

### Within Each User Story

- Service implementation before endpoints
- Endpoints before frontend integration
- Core features before error handling
- Integration before polish

### Parallel Opportunities

**Phase 5 (US3) - Parallel Tasks**:
- T029 (get_translation), T030 (create_translation), T031 (validation) can run in parallel
- T033 (GET endpoint), T034 (PUT endpoint), T035 (status endpoint) can run in parallel
- T036 (DocItem), T037 (Progress), T038 (Toggle) frontend tasks can run in parallel

**Phase 6 (US2 API) - Parallel Tasks**:
- T040 (GET endpoint), T041 (user context), T042 (error handling) can run in parallel
- T043 (frontend integration) can run in parallel with backend tasks

**Team Parallel Strategy**:
- Developer A: Phase 5 Backend (TranslationService + endpoints)
- Developer B: Phase 5 Frontend (DocItem integration + indicators)
- Developer C: Phase 6 (Personalization API completion)

---

## Parallel Example: Phase 5 (User Story 3)

```bash
# Launch all service tasks together:
Task: "T029 [P] [US3] Implement TranslationService.get_translation()"
Task: "T030 [P] [US3] Implement TranslationService.create_or_update_translation()"
Task: "T031 [P] [US3] Implement technical term validation"

# Launch all endpoint tasks together:
Task: "T033 [P] [US3] Implement GET /api/v1/chapters/{id}/translation endpoint"
Task: "T034 [P] [US3] Implement PUT /api/v1/chapters/{id}/translation endpoint"
Task: "T035 [P] [US3] Implement GET /api/v1/translations/status endpoint"

# Launch all frontend tasks together:
Task: "T036 [US3] Update DocItem wrapper for translation"
Task: "T037 [US3] Add AI Translation in progress indicator"
Task: "T038 [US3] Handle loading state in TranslationToggle"
```

---

## Implementation Strategy

### MVP First (User Story 3 Core)

1. Complete T029-T032: TranslationService with caching
2. Complete T033: GET translation endpoint
3. Complete T036-T039: Frontend integration
4. **STOP and VALIDATE**: Test translation toggle on live chapter
5. Deploy/demo if ready

### Incremental Delivery

1. Add TranslationService → Test with sample content → Deploy
2. Add Translation API endpoints → Test with frontend → Deploy
3. Add "AI Translation in progress" indicator → Test UX → Deploy
4. Add admin translation update endpoint → Test admin flow → Deploy
5. Each increment adds value without breaking previous work

### Parallel Team Strategy

With multiple developers:

1. Team A: TranslationService backend (T029-T032, T033-T035)
2. Team B: Frontend integration (T036-T039)
3. Team C: Personalization API completion (T040-T043)
4. Merge and test integration together

---

## Task Summary

**Total Tasks**: 21 tasks (Phases 5-7 only)

**By Phase**:
- Phase 5 (US3 - Translation): 11 tasks
- Phase 6 (US2 - Personalization API): 4 tasks
- Phase 7 (Polish): 6 tasks

**Parallelizable Tasks**: 15 tasks marked with [P]

**MVP Scope** (Translation core only): 7 tasks (T029-T033, T036-T037)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group of 2-3 tasks
- Stop at checkpoints to validate story independently
- Technical term preservation CRITICAL for translation quality
- "AI Translation in progress" indicator REQUIRED per spec FR-017
- Cache translations to minimize Grok API costs
- User context from JWT required for personalized summaries
