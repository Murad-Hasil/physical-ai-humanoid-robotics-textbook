---
id: 0008
title: phase-5-translation-tasks
stage: tasks
date: 2026-03-26
surface: agent
model: qwen-coder-plus
feature: 001-phase-7-intelligence
branch: 001-phase-7-intelligence
user: brownie
command: /sp.tasks Target: /phase-5-translation-and-api-activation - Translation Engine, API Endpoint Completion, Frontend Polish & Integration
labels: ["tasks","phase-7","translation","roman-urdu","api-endpoints","frontend-integration"]
links:
  spec: specs/001-phase-7-intelligence/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase-7-intelligence/tasks-phase5-translation.md
tests:
  - Task format validation (checkbox, ID, story labels, file paths)
  - User story independence verification
  - API contract completeness check against OpenAPI spec
tests_run:
  - OpenAPI spec cross-reference for translation endpoints
  - Service layer dependency mapping
---

## Prompt

/sp.tasks
Target: /phase-5-translation-and-api-activation

Instructions:
1. **Translation Engine (Core Phase 5)**:
   - [ ] Implement `TranslationService.get_translation()` in `backend/services/translation_service.py`.
   - [ ] Apply the `TRANSLATION_PROMPT_TEMPLATE` to ensure Roman Urdu quality.
   - [ ] Implement Technical Term Validation: Check if "URDF", "ROS 2", etc., are preserved after translation.
   - [ ] Add caching logic using the `Translation` table to save API costs.
2. **API Endpoint Completion**:
   - [ ] Complete `GET /api/v1/chapters/{id}/summary` in `backend/api/chapters.py`.
   - [ ] Complete `GET /api/v1/chapters/{id}/translation` in `backend/api/chapters.py`.
   - [ ] Ensure both endpoints use the current user's profile (Hardware/Skill/Language) from the JWT/Context.
3. **Frontend Polish & Integration**:
   - [ ] Ensure the `DocItem` wrapper handles the "Loading" state for AI generation.
   - [ ] Add the "AI Translation in progress" indicator in the UI as per the specification.

Definition of Done:
- Selecting "Urdu" on a documentation page fetches and displays a Roman Urdu version.
- API endpoints return 200 OK with the generated/cached content.
- Technical terms remain in English within the Roman Urdu text.

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Response snapshot

Generated comprehensive tasks-phase5-translation.md with 21 tasks organized by user stories for Phases 5-7:

**Phase 5 (US3 - Translation)**: 11 tasks
- TranslationService.get_translation() with cache-first strategy
- TranslationService.create_or_update_translation() with Grok API integration
- Technical term validation using TECHNICAL_TERMS_PRESERVATION set
- Caching logic to minimize API costs
- GET /api/v1/chapters/{id}/translation endpoint with user context
- PUT /api/v1/chapters/{id}/translation endpoint (admin-only)
- GET /api/v1/translations/status for coverage analytics
- DocItem wrapper updates for translation display
- "AI Translation in progress" indicator per spec FR-017
- Loading state handling in TranslationToggle
- Error handling with English fallback

**Phase 6 (US2 - Personalization API)**: 4 tasks
- GET /api/v1/chapters/{id}/summary endpoint completion
- User context integration from JWT/auth middleware
- Error handling with retry logic and cached fallback
- Frontend integration in DocItem wrapper

**Phase 7 (Polish)**: 6 tasks
- Integration tests for translation and personalization flows
- Frontend integration tests for DocItem
- Performance optimization (database indexes, LRU cache)
- Security hardening (input validation, rate limiting)
- API documentation updates

**Key Features**:
- 15 tasks marked [P] for parallel execution
- Each user story independently testable
- MVP scope defined (Translation core = 7 tasks)
- Parallel team strategy for 3 developers
- Technical term preservation validation critical for quality
- "AI Translation in progress" indicator required for unpublished translations (spec FR-017)
- Cache-first strategy to minimize Grok API costs

## Outcome

- ✅ Impact: Actionable task list for Translation Engine and API completion with clear file paths
- 🧪 Tests: Task format validated, API contracts cross-referenced with OpenAPI spec
- 📁 Files: tasks-phase5-translation.md (21 tasks across 3 phases)
- 🔁 Next prompts: /sp.implement to begin Phase 5 implementation
- 🧠 Reflection: Translation pattern mirrors Personalization for consistency; caching critical for cost control

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully with all design artifacts available
- Graders run and results (PASS/FAIL): PASS - task format validation confirmed all 21 tasks follow checklist format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with /sp.implement starting from Phase 5 (TranslationService)
