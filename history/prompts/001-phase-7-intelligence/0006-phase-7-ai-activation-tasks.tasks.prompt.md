---
id: 0006
title: phase-7-ai-activation-tasks
stage: tasks
date: 2026-03-26
surface: agent
model: qwen-coder-plus
feature: 001-phase-7-intelligence
branch: 001-phase-7-intelligence
user: brownie
command: /sp.tasks Target: /phase-4-5-ai-logic-activation - Personalization Engine, Translation Engine, API Logic & Error Handling
labels: ["tasks","phase-7","ai-activation","personalization","translation","curriculum","backend-services"]
links:
  spec: specs/001-phase-7-intelligence/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase-7-intelligence/tasks-ai-activation.md
tests:
  - Task format validation (checkbox, ID, story labels, file paths)
  - User story independence verification
  - API contract completeness check
tests_run:
  - OpenAPI spec cross-reference
  - Service layer dependency mapping
---

## Prompt

/sp.tasks
Target: /phase-4-5-ai-logic-activation

Instructions:
1. **Personalization Engine (Phase 4)**:
   - [ ] Implement `PersonalizationService.get_or_generate_summary()`.
   - [ ] Design System Prompts that inject `hardware_config` and `skill_level` into the summarization logic.
   - [ ] Implement caching: If a summary for a specific hardware/skill combo exists in `ChapterSummary`, return it; otherwise, generate and save.
2. **Translation Engine (Phase 5)**:
   - [ ] Implement `TranslationService.get_translation()`.
   - [ ] Create a "Technical Preservation" prompt: Ensure terms like "URDF", "Joint State", and "RTX" stay in English while the rest is Roman Urdu.
   - [ ] Implement the `Translation` table sync to avoid redundant API calls.
3. **API Logic & Error Handling**:
   - [ ] Complete the GET endpoints for Chapter Summary and Translation.
   - [ ] Implement a "Retry" logic if the Grok API rate limit is hit.
   - [ ] Add the "AI Translation in progress" fallback indicator as per the spec.

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Response snapshot

Generated comprehensive tasks-ai-activation.md with 38 tasks organized by user stories for Phases 4-7:

**Phase 4 (US2 - Personalization)**: 9 tasks
- Prompt templates with hardware context injection (sim_rig/edge_kit/unitree)
- PersonalizationService with cache-first strategy (ChapterSummary table)
- Grok API client with rate limiting and retry logic
- GET /api/v1/chapters/{id}/summary endpoint
- LRU caching optimization (optional Redis)
- Structured logging for cost tracking
- Frontend PersonalizedSummary component with loading states

**Phase 5 (US3 - Translation)**: 12 tasks
- Translation prompts with technical term preservation rules
- TranslationService with draft/in_review/published status tracking
- GET/PUT /api/v1/chapters/{id}/translation endpoints
- GET /api/v1/translations/status for coverage stats
- Technical term glossary validation (URDF, Joint State, RTX, etc.)
- Frontend TranslationToggle with "AI Translation in progress" indicator
- TranslationProgress component with status-based colors

**Phase 6 (US4 - Curriculum)**: 11 tasks
- Curriculum parser for markdown files with frontmatter
- CurriculumService with batch ingestion
- GET /api/v1/curriculum/weeks endpoints
- Batch ingestion script with progress logging
- Sample content structure (weeks 1-13)
- Docusaurus sidebar updates

**Phase 7 (Polish)**: 6 tasks
- Error boundaries, loading skeletons
- Accessibility (ARIA labels, keyboard nav)
- Performance optimization (React.memo, lazy loading)
- Security hardening (input validation, rate limiting)
- Documentation updates

**Key Features**:
- 22 tasks marked [P] for parallel execution
- Each user story independently testable
- MVP scope defined (US2 only = 9 tasks)
- Parallel team strategy for 3 developers
- Exponential backoff retry logic for Grok API rate limits
- Technical term preservation critical for translation quality

## Outcome

- ✅ Impact: Actionable task list for AI logic activation with clear file paths and dependencies
- 🧪 Tests: Task format validated, API contracts cross-referenced with OpenAPI spec
- 📁 Files: tasks-ai-activation.md (38 tasks across 4 phases)
- 🔁 Next prompts: /sp.implement to begin Phase 4-5 implementation
- 🧠 Reflection: Separated personalization and translation into parallel tracks for team efficiency

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully with all design artifacts available
- Graders run and results (PASS/FAIL): PASS - task format validation confirmed all 38 tasks follow checklist format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with /sp.implement starting from Phase 4 (Personalization)
