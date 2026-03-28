# Tasks: Phase 7 Final Intelligence - AI Logic Activation (Phases 4-5)

**Input**: Design documents from `/specs/001-phase-7-intelligence/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)
**Previous Work**: Phase 1-3 complete (Setup, Foundational, Smart Onboarding)

**Tests**: Tests are OPTIONAL for this feature. Not included in this task list. Add manually if TDD approach is desired.

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

## Phase 1: Setup (Already Complete ✓)

**Status**: 6/6 tasks complete

---

## Phase 2: Foundational (Already Complete ✓)

**Status**: 11/11 tasks complete

---

## Phase 3: User Story 1 - Smart Onboarding (Already Complete ✓)

**Status**: 11/11 tasks complete

---

## Phase 4: User Story 2 - Personalized Chapter Summaries (Priority: P2) 🎯

**Goal**: Implement AI-powered personalization engine that generates hardware-aware and skill-level-aware chapter summaries

**Independent Test**: View any chapter with different user profiles (RTX/Jetson/Unitree × beginner/intermediate/advanced) and verify summary content changes appropriately

### Implementation for User Story 2

- [ ] T029 [P] [US2] Create prompt templates in `backend/llm/prompts/personalization.py`:
  - `PERSONALIZATION_PROMPT_TEMPLATE` with hardware context injection
  - Hardware-specific guidelines (sim_rig: desktop GPU, edge_kit: power efficiency, unitree: real-time)
  - Skill-level adjustments (beginner: simple, intermediate: technical, advanced: optimization)
  - Output format preservation rules for markdown

- [ ] T030 [P] [US2] Implement `PersonalizationService.get_or_generate_summary()` in `backend/services/personalization_service.py`:
  - Check database cache first (ChapterSummary table lookup)
  - Call Grok API with prompt template if not cached
  - Store generated summary in database with unique constraint
  - Return dictionary with summary_content, generated_at, hardware_profile_type, skill_level

- [ ] T031 [P] [US2] Implement Grok API client integration in `backend/llm/grok_client.py`:
  - Add `generate_personalized_summary()` method
  - Configure API endpoint, headers, authentication
  - Handle rate limiting with retry logic (exponential backoff)
  - Parse response and extract summary content

- [ ] T032 [P] [US2] Implement `GET /api/v1/chapters/{chapter_id}/summary` endpoint in `backend/api/v1/endpoints/personalization.py`:
  - Extract chapter_id from path parameters
  - Get hardware_profile and skill_level from query params (optional)
  - If not provided, use current user's profile from auth context
  - Call `PersonalizationService.get_or_generate_summary()`
  - Return `ChapterSummaryResponse` with 200 status
  - Handle 404 for non-existent chapters

- [ ] T033 [US2] Add caching optimization in `backend/services/personalization_service.py`:
  - Implement LRU cache for hot summaries (optional Redis integration)
  - Add cache invalidation logic for content updates
  - Log cache hits vs API calls for monitoring

- [ ] T034 [US2] Implement error handling and retry logic in `backend/services/personalization_service.py`:
  - Catch Grok API rate limit errors (429)
  - Implement exponential backoff (1s, 2s, 4s, 8s max 3 retries)
  - Log retry attempts and failures
  - Return graceful fallback message on persistent failure

- [ ] T035 [US2] Add structured logging to personalization service in `backend/services/personalization_service.py`:
  - Log summary generation events with chapter_id, hardware_profile, skill_level
  - Log token usage for cost tracking
  - Log generation time for performance monitoring
  - Use `logger.info()`, `logger.error()` appropriately

- [ ] T036 [US2] Create `PersonalizedSummary` React component in `docusaurus-textbook/src/components/personalization/PersonalizedSummary.tsx`:
  - Fetch summary from GET `/api/v1/chapters/{id}/summary`
  - Display personalized markdown content with proper formatting
  - Handle loading state with skeleton loader
  - Handle error state with user-friendly message
  - Re-fetch when hardware profile or skill level changes

- [ ] T037 [US2] Update DocItem wrapper in `docusaurus-textbook/src/theme/DocItem/index.tsx`:
  - Import `PersonalizedSummary` component
  - Conditionally render based on `personalizationEnabled` state
  - Pass chapter_id from props
  - Add glassmorphism styling for summary container

**Checkpoint**: User Story 2 complete - personalized summaries generate correctly for all hardware/skill combinations

---

## Phase 5: User Story 3 - Multi-Language Translation (Priority: P3)

**Goal**: Implement Roman Urdu translation engine with technical term preservation

**Independent Test**: View any chapter, toggle to Roman Urdu, verify content translates while preserving code blocks, technical terms, and API names

### Implementation for User Story 3

- [ ] T038 [P] [US3] Create prompt templates in `backend/llm/prompts/translation.py`:
  - `TRANSLATION_PROMPT_TEMPLATE` with preservation rules
  - Technical term glossary (CUDA, ROS, PyTorch, TensorFlow, URDF, etc.)
  - Rules: DO NOT translate code blocks, function names, APIs, commands
  - Rules: Translate ONLY explanatory prose
  - Style guidelines for conversational Roman Urdu
  - Output format preservation for markdown

- [ ] T039 [P] [US3] Implement `TranslationService.get_translation()` in `backend/services/translation_service.py`:
  - Query Translation table for chapter_id and language_code
  - Return translation if exists with status check
  - Return None if not found (frontend shows English with indicator)
  - Return dictionary with translated_content, status, updated_at

- [ ] T040 [P] [US3] Implement `TranslationService.create_or_update_translation()` in `backend/services/translation_service.py`:
  - Insert or update Translation record
  - Call Grok API with translation prompt if content not provided
  - Set status to 'draft' for AI-generated translations
  - Support manual status updates (draft → in_review → published)
  - Return dictionary with translation details

- [ ] T041 [P] [US3] Implement Grok API integration for translation in `backend/llm/grok_client.py`:
  - Add `generate_translation()` method
  - Configure API endpoint, headers, authentication
  - Handle rate limiting with retry logic
  - Parse response and extract translated content
  - Validate translation preserves technical terms

- [ ] T042 [P] [US3] Implement `GET /api/v1/chapters/{chapter_id}/translation` endpoint in `backend/api/v1/endpoints/translations.py`:
  - Extract chapter_id from path parameters
  - Get lang from query parameter (default: 'ur-Latn')
  - Call `TranslationService.get_translation()`
  - Return 404 if translation not found (triggers "AI Translation in progress" indicator)
  - Return `TranslationResponse` with 200 status if found

- [ ] T043 [P] [US3] Implement `PUT /api/v1/chapters/{chapter_id}/translation` endpoint in `backend/api/v1/endpoints/translations.py`:
  - Admin-only access check (verify is_admin flag)
  - Accept `TranslationUpdate` schema with translated_content, status, review_notes
  - Call `TranslationService.create_or_update_translation()`
  - Return `TranslationResponse` with updated translation

- [ ] T044 [P] [US3] Implement `GET /api/v1/translations/status` endpoint in `backend/api/v1/endpoints/translations.py`:
  - Query Translation table for counts by status
  - Calculate coverage percentage (published / total chapters)
  - Group statistics by language_code
  - Return `TranslationStatsResponse` with total_chapters, translated_chapters, coverage_percentage, by_language

- [ ] T045 [US3] Add technical term preservation validation in `backend/services/translation_service.py`:
  - Create `TECHNICAL_TERMS` set with common AI/robotics terms
  - Validate translation preserves terms in English
  - Log warnings for over-translated terms
  - Optional: Auto-correct common mistakes

- [ ] T046 [US3] Add structured logging to translation service in `backend/services/translation_service.py`:
  - Log translation requests with chapter_id, language_code
  - Log translation status changes
  - Log API calls and token usage
  - Track translation coverage metrics

- [ ] T047 [US3] Update TranslationToggle component in `docusaurus-textbook/src/components/translation/TranslationToggle.tsx`:
  - Fetch translation on toggle activation
  - Show loading state while fetching
  - Display "AI Translation in progress" indicator for 404 responses
  - Cache fetched translations in component state

- [ ] T048 [US3] Update TranslationProgress component in `docusaurus-textbook/src/components/translation/TranslationProgress.tsx`:
  - Fetch translation status from backend
  - Display appropriate indicator (draft: yellow, in_review: orange, published: green)
  - Add tooltip with status description
  - Animate "in progress" indicator with pulse effect

- [ ] T049 [US3] Update DocItem wrapper in `docusaurus-textbook/src/theme/DocItem/index.tsx`:
  - Import `TranslationProgress` component
  - Show progress indicator for draft translations
  - Handle translation not found state gracefully
  - Display "AI Translation in progress" message per spec FR-017

**Checkpoint**: User Story 3 complete - Roman Urdu translation works with technical term preservation

---

## Phase 6: User Story 4 - Curriculum Content Access (Priority: P4)

**Goal**: Populate system with all 13 weeks of curriculum content and enable batch ingestion

**Independent Test**: Browse curriculum structure, verify all 13 weeks accessible with chapters, personalized summaries, and translations applied

### Implementation for User Story 4

- [ ] T050 [P] [US4] Create curriculum parser in `backend/ingestion/curriculum_parser.py`:
  - `parse_week_folder(folder_path)` function
  - Extract week metadata from `_category_.json`
  - Parse chapter markdown files with frontmatter
  - Return structured week data dictionary

- [ ] T051 [P] [US4] Implement `CurriculumService.ingest_week()` in `backend/services/curriculum_service.py`:
  - Create or update CurriculumWeek record
  - Create or update Chapter records with content
  - Handle chapter ordering and relationships
  - Return ingested week details

- [ ] T052 [P] [US4] Implement `CurriculumService.get_all_weeks()` in `backend/services/curriculum_service.py`:
  - Query all CurriculumWeek records ordered by week_number
  - Optionally include chapter list
  - Return list of week dictionaries

- [ ] T053 [P] [US4] Implement `CurriculumService.get_week_by_number()` in `backend/services/curriculum_service.py`:
  - Query specific week by week_number
  - Include all chapters with content
  - Return week dictionary with chapters or None

- [ ] T054 [P] [US4] Implement `GET /api/v1/curriculum/weeks` endpoint in `backend/api/v1/endpoints/curriculum.py`:
  - List all weeks with optional include_chapters query param
  - Return array of `CurriculumWeekResponse`
  - Add pagination for large curriculum (optional)

- [ ] T055 [P] [US4] Implement `GET /api/v1/curriculum/weeks/{week_number}` endpoint in `backend/api/v1/endpoints/curriculum.py`:
  - Get week details with all chapters
  - Support `include_personalized_summaries` query param
  - Return `CurriculumWeekDetailResponse` with 200 status
  - Handle 404 for non-existent weeks

- [ ] T056 [P] [US4] Implement `POST /api/v1/curriculum/ingest` endpoint in `backend/api/v1/endpoints/curriculum.py`:
  - Admin-only access check
  - Accept `CurriculumIngestRequest` with weeks array
  - Call `CurriculumService.ingest_week()` for each week
  - Support `regenerate_summaries` flag
  - Return job status response with job_id

- [ ] T057 [US4] Create batch ingestion script in `backend/ingestion/ingest_curriculum.py`:
  - CLI argument parser for content path
  - Iterate through week folders (week-01 to week-13)
  - Parse and ingest each week using curriculum_parser
  - Optional summary regeneration flag
  - Progress logging with completion summary

- [ ] T058 [US4] Create sample curriculum content structure in `docusaurus-textbook/docs/`:
  - Create week-01/ through week-13/ directories
  - Create `_category_.json` template for each week
  - Create sample chapter markdown files with frontmatter
  - Include tags and hardware_relevant fields

- [ ] T059 [US4] Update Docusaurus sidebar in `docusaurus-textbook/sidebars.ts`:
  - Add curriculum section with all 13 weeks
  - Configure category links for each week
  - Ensure proper navigation structure
  - Test sidebar rendering

- [ ] T060 [US4] Run initial content ingestion:
  - Execute: `python -m ingestion.ingest_curriculum --path ../docusaurus-textbook/docs --regenerate-summaries`
  - Verify weeks and chapters in database
  - Verify summaries generated for all combinations
  - Log ingestion statistics

**Checkpoint**: User Story 4 complete - all 13 weeks accessible with personalization and translation

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T061 [P] Add error boundaries in `docusaurus-textbook/src/components/errors/ErrorBoundary.tsx`:
  - Catch API errors gracefully
  - Display user-friendly error messages
  - Retry logic for transient failures
  - Log errors for debugging

- [ ] T062 [P] Add loading skeletons in `docusaurus-textbook/src/components/loading/`:
  - `SummarySkeleton.tsx` for personalized summaries
  - `TranslationSkeleton.tsx` for translation content
  - Match glassmorphism theme styling

- [ ] T063 [P] Implement accessibility features:
  - ARIA labels for TranslationToggle and PersonalizationToggle
  - Keyboard navigation support for all interactive elements
  - Screen reader compatibility
  - WCAG 2.1 AA contrast compliance verification

- [ ] T064 [P] Performance optimization:
  - Add React.memo for PersonalizedSummary and TranslationToggle components
  - Implement lazy loading for translation components
  - Optimize API calls with React Query or SWR (optional)
  - Profile and optimize re-renders

- [ ] T065 [P] Security hardening:
  - Validate all user inputs in API endpoints
  - Sanitize markdown content before rendering
  - Rate limit personalization and translation API calls
  - Audit admin endpoints for unauthorized access

- [ ] T066 [P] Documentation updates:
  - Update `README.md` with Phase 7 features
  - Add API documentation examples in Swagger
  - Create user guide for personalization and translation features
  - Document environment variables and configuration

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1-3**: ✅ Already complete (Setup, Foundational, Smart Onboarding)
- **Phase 4 (US2)**: Can start immediately - depends on Phase 2 foundational services
- **Phase 5 (US3)**: Can start immediately - independent of US2, can run in parallel
- **Phase 6 (US4)**: Can start after Phase 2 - benefits from US2 personalization
- **Phase 7 (Polish)**: Depends on Phases 4-6 completion

### User Story Dependencies

- **User Story 2 (P2)**: No dependencies on other stories - can implement independently
- **User Story 3 (P3)**: No dependencies on other stories - can implement in parallel with US2
- **User Story 4 (P4)**: Benefits from US2 (personalized summaries) but can start independently

### Within Each User Story

- Prompt templates before service implementation
- Services before endpoints
- Core implementation before integration
- Backend before frontend integration

### Parallel Opportunities

**Phase 4 (US2) - Parallel Tasks**:
- T029 (prompts), T030 (service), T031 (Grok client) can run in parallel
- T032 (endpoint) can start after T030 (service) begins
- T036 (frontend component) can run in parallel with backend tasks

**Phase 5 (US3) - Parallel Tasks**:
- T038 (prompts), T039-T040 (service), T041 (Grok client) can run in parallel
- T042-T044 (endpoints) can run in parallel once service starts
- T047-T049 (frontend) can run in parallel with backend

**Team Parallel Strategy**:
- Developer A: Phase 4 (Personalization - US2)
- Developer B: Phase 5 (Translation - US3)
- Developer C: Phase 6 (Curriculum - US4)

---

## Parallel Example: Phase 4 (User Story 2)

```bash
# Launch all prompt and service tasks together:
Task: "T029 [P] [US2] Create prompt templates in backend/llm/prompts/personalization.py"
Task: "T030 [P] [US2] Implement PersonalizationService.get_or_generate_summary()"
Task: "T031 [P] [US2] Implement Grok API client integration"

# Launch frontend component in parallel:
Task: "T036 [P] [US2] Create PersonalizedSummary React component"
```

---

## Implementation Strategy

### MVP First (User Story 2 Only)

1. Complete Phase 4: User Story 2 (Personalization)
2. **STOP and VALIDATE**: Test personalized summaries with different hardware/skill combinations
3. Deploy/demo if ready

### Incremental Delivery

1. Add User Story 2 (Personalization) → Test independently → Deploy/Demo
2. Add User Story 3 (Translation) → Test independently → Deploy/Demo
3. Add User Story 4 (Curriculum) → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team A: User Story 2 (Personalization engine)
2. Team B: User Story 3 (Translation engine)
3. Team C: User Story 4 (Curriculum ingestion)
4. Stories complete and integrate independently
5. Merge all stories together for Phase 7 release

---

## Task Summary

**Total Tasks**: 38 tasks (Phases 4-7 only)

**By Phase**:
- Phase 4 (US2 - Personalization): 9 tasks
- Phase 5 (US3 - Translation): 12 tasks
- Phase 6 (US4 - Curriculum): 11 tasks
- Phase 7 (Polish): 6 tasks

**Parallelizable Tasks**: 22 tasks marked with [P]

**MVP Scope** (User Story 2 only): 9 tasks

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group of 2-3 tasks
- Stop at checkpoints to validate story independently
- Grok API rate limiting requires retry logic with exponential backoff
- Technical term preservation critical for Roman Urdu translation quality
- "AI Translation in progress" indicator required for unpublished translations (spec FR-017)
