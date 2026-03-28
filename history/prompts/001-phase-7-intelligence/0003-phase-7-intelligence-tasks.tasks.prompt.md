---
id: 0003
title: phase-7-intelligence-tasks
stage: tasks
date: 2026-03-26
surface: agent
model: qwen-coder-plus
feature: 001-phase-7-intelligence
branch: 001-phase-7-intelligence
user: brownie
command: /sp.tasks Target: /phase-7-final-intelligence - Backend Database, AI Services, Frontend Smart UI, Content Ingestion
labels: ["tasks","phase-7","personalization","multi-language","curriculum","implementation"]
links:
  spec: specs/001-phase-7-intelligence/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase-7-intelligence/tasks.md
tests:
  - Task format validation (checkbox, ID, story labels, file paths)
  - User story independence verification
---

## Prompt

/sp.tasks
Target: /phase-7-final-intelligence

Instructions:
1. **Backend - Database**:
   - [ ] Add `gpu_type`, `experience_level`, and `edge_hardware` columns to the User model.
   - [ ] Run Alembic migration for these profile fields.
2. **Backend - AI Services**:
   - [ ] Implement `POST /api/ai/personalize` endpoint.
   - [ ] Implement `POST /api/ai/translate` endpoint.
3. **Frontend - Smart UI**:
   - [ ] Add Hardware/Skill selection fields to the Signup/Profile page.
   - [ ] Create the `AIContentControls` component (Personalize/Translate buttons).
   - [ ] Inject `AIContentControls` into the Docusaurus documentation layout.
4. **Content - Ingestion**:
   - [ ] Write/Generate 13-week Markdown modules.
   - [ ] Perform a "Global Re-index" via the Admin Panel to sync all new content.

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Response snapshot

Generated comprehensive tasks.md with 66 tasks organized by user stories for independent implementation:
- **Phase 1 (Setup)**: 6 tasks - environment verification, dependency installation
- **Phase 2 (Foundational)**: 11 tasks - skill_level model, curriculum tables, API routers, service stubs
- **Phase 3 (US1 - Smart Onboarding)**: 11 tasks - user profile APIs, HardwareProfileForm, SkillLevelSelector, signup/profile pages
- **Phase 4 (US2 - Personalization)**: 9 tasks - prompt templates, PersonalizationService, summary endpoint, DocItem swizzling
- **Phase 5 (US3 - Translation)**: 10 tasks - translation prompts, TranslationService, translation endpoints, TranslationToggle component
- **Phase 6 (US4 - Curriculum)**: 11 tasks - curriculum parser, ingestion script, batch ingestion, sample content creation
- **Phase 7 (Polish)**: 8 tasks - error boundaries, loading skeletons, accessibility, performance, security

Key features:
- 32 tasks marked [P] for parallel execution
- Each user story independently testable
- MVP scope defined (US1 only = 28 tasks)
- Parallel team strategy documented for 4 developers
- All tasks include exact file paths for LLM execution

## Outcome

- ✅ Impact: Actionable task list ready for immediate implementation with clear file paths and dependencies
- 🧪 Tests: Task format validated (checkbox, ID, story labels, file paths), user story independence verified
- 📁 Files: tasks.md (66 tasks across 7 phases)
- 🔁 Next prompts: /sp.implement to begin phased implementation
- 🧠 Reflection: User story organization enables parallel development and incremental MVP delivery

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully with all design artifacts available
- Graders run and results (PASS/FAIL): PASS - task format validation confirmed all 66 tasks follow checklist format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with /sp.implement starting from Phase 1
