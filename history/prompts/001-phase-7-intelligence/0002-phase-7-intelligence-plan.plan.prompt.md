---
id: 0002
title: phase-7-intelligence-plan
stage: plan
date: 2026-03-26
surface: agent
model: qwen-coder-plus
feature: 001-phase-7-intelligence
branch: 001-phase-7-intelligence
user: brownie
command: /sp.plan Target: /phase-7-final-intelligence - Data Collection, Intelligence Hooks, Frontend Integration, Content Strategy
labels: ["plan","phase-7","personalization","multi-language","architecture","design"]
links:
  spec: specs/001-phase-7-intelligence/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase-7-intelligence/plan.md
  - specs/001-phase-7-intelligence/research.md
  - specs/001-phase-7-intelligence/data-model.md
  - specs/001-phase-7-intelligence/contracts/openapi.yaml
  - specs/001-phase-7-intelligence/contracts/frontend-components.tsx
  - specs/001-phase-7-intelligence/quickstart.md
tests:
  - Plan validation against spec requirements
  - API contract completeness check
tests_run:
  - Constitution Check (post-design)
---

## Prompt

/sp.plan
Target: /phase-7-final-intelligence

Instructions:
1. **Data Collection (Goal 3)**:
   - Map new fields (`gpu_type`, `skill_level`) to the `users` table.
   - Design the API payload for the updated signup/profile update flow.
2. **Intelligence Hooks (Goal 1 & 2)**:
   - Design a `PersonalizationService` and `TranslationService` in FastAPI.
   - Plan the prompt engineering to utilize User Profile data for context-aware rewriting.
3. **Frontend Integration**:
   - Plan the placement of "Personalize" and "Translate" buttons within the `DocItem` theme wrapper.
   - Plan the state management for toggling between original and AI-generated text.
4. **Content Strategy (Goal 4)**:
   - Structure 13 Markdown files based on the PDF's weekly modules for batch ingestion into Qdrant.

## Response snapshot

Completed Phase 1 planning for Phase 7 Final Intelligence. Created comprehensive implementation plan with:
- **Research (research.md)**: Resolved 6 unknowns (user model extension, Grok prompt engineering, Roman Urdu translation patterns, curriculum structure, Docusaurus customization, caching strategy)
- **Data Model (data-model.md)**: Defined 4 new models (CurriculumWeek, Chapter, ChapterSummary, Translation), extended StudentProfile with skill_level, complete migration strategy
- **API Contracts (openapi.yaml)**: 12 RESTful endpoints for user profiles, personalization, translations, curriculum management with full OpenAPI 3.0 spec
- **Frontend Contracts (frontend-components.tsx)**: 8 React components with TypeScript interfaces, context provider, API service layer, glassmorphism styling guidelines
- **Quickstart (quickstart.md)**: Complete setup guide for backend/frontend, testing procedures, debugging tips, common issues

Key architectural decisions:
- skill_level added to StudentProfile (not User) to avoid Better-Auth conflicts
- Hybrid caching: database storage for summaries + optional Redis for hot paths
- React Context + localStorage for frontend state management
- Docusaurus theme swizzling for DocItem customization
- Prompt engineering with explicit preservation rules for Roman Urdu translation

## Outcome

- ✅ Impact: Complete architectural plan ready for task breakdown with all research questions resolved
- 🧪 Tests: Constitution Check passed (post-design), all gates validated
- 📁 Files: 6 planning artifacts (plan.md, research.md, data-model.md, contracts/*, quickstart.md)
- 🔁 Next prompts: /sp.tasks to break implementation into testable tasks
- 🧠 Reflection: Research-first approach ensured all unknowns resolved before detailed design

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed successfully with all clarifications resolved in research phase
- Graders run and results (PASS/FAIL): PASS - Constitution Check validated after Phase 1 design
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.tasks for implementation breakdown
