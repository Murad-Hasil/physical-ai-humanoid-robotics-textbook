---
id: 003
title: hardware-aware-auth-tasks
stage: tasks
date: 2026-03-16
surface: agent
model: qwen-code
feature: 001-hardware-aware-auth
branch: 001-hardware-aware-auth
user: brownie
command: /sp.tasks Target: /phase-3-auth-personalization Instructions: 1. Auth Foundation: Install and configure Better-Auth in /backend/auth. Implement User registration and login endpoints. Create a session-check middleware for FastAPI. 2. Hardware & Profile Database: Create SQLAlchemy/Prisma models for HardwareProfile with the following fields: workstation_gpu (e.g., RTX 4070 Ti), vram_gb (integer, e.g., 12), edge_kit (Enum: Orin_Nano, Orin_NX), robot (Enum: Go2, G1, Proxy). Create a CurriculumProgress table tracking Weeks 1 through 13. 3. Intelligence Layer (Personalization): Develop a get_user_context function that formats the Hardware Profile into a string. Update services/rag_pipeline.py to accept this context and prepend it to the Grok API system prompt. 4. API Integration: Secure the existing POST /api/chat and POST /api/ingest endpoints. Add a GET /api/user/profile and PATCH /api/user/profile endpoint for hardware updates. 5. Frontend Hooks: Create a placeholder React component in Docusaurus to test the Auth state (Login/Logout). Definition of Done: Student can sign up and save their "Edge Kit" or "Sim Rig" settings. Chatbot acknowledges the user's specific hardware in its responses. API returns 401 Unauthorized if no valid session is present.
labels: ["authentication", "personalization", "hardware-aware", "rag", "better-auth", "pdf-curriculum", "tasks"]
links:
  spec: specs/001-hardware-aware-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-hardware-aware-auth/tasks.md
tests:
  - backend/tests/unit/test_auth.py
  - backend/tests/unit/test_hardware.py
  - backend/tests/unit/test_curriculum.py
  - backend/tests/integration/test_github_oauth.py
  - backend/tests/integration/test_chat_personalization.py
  - backend/tests/integration/test_protected_endpoints.py
---

## Prompt

Target: /phase-3-auth-personalization

Instructions:
1. **Auth Foundation**:
   - Install and configure Better-Auth in `/backend/auth`.
   - Implement User registration and login endpoints.
   - Create a session-check middleware for FastAPI.
2. **Hardware & Profile Database**:
   - Create SQLAlchemy/Prisma models for `HardwareProfile` with the following fields:
     - `workstation_gpu` (e.g., RTX 4070 Ti)
     - `vram_gb` (integer, e.g., 12)
     - `edge_kit` (Enum: Orin_Nano, Orin_NX)
     - `robot` (Enum: Go2, G1, Proxy)
   - Create a `CurriculumProgress` table tracking Weeks 1 through 13.
3. **Intelligence Layer (Personalization)**:
   - Develop a `get_user_context` function that formats the Hardware Profile into a string.
   - Update `services/rag_pipeline.py` to accept this context and prepend it to the Grok API system prompt.
4. **API Integration**:
   - Secure the existing `POST /api/chat` and `POST /api/ingest` endpoints.
   - Add a `GET /api/user/profile` and `PATCH /api/user/profile` endpoint for hardware updates.
5. **Frontend Hooks**:
   - Create a placeholder React component in Docusaurus to test the Auth state (Login/Logout).

Definition of Done:
- Student can sign up and save their "Edge Kit" or "Sim Rig" settings.
- Chatbot acknowledges the user's specific hardware in its responses.
- API returns 401 Unauthorized if no valid session is present.

## Response snapshot

Created comprehensive tasks.md with 102 actionable tasks organized by user story:

**Phase 1 - Setup (5 tasks)**: Directory structure, dependencies (better-auth, sqlalchemy, bcrypt, python-jose), environment config, Alembic migrations

**Phase 2 - Foundational (8 tasks)**: Better-Auth config, database engine, base models, session validator, auth middleware, PDF hardware constants, logging, initial migration

**Phase 3 - US1 Authentication (17 tasks)**: User/StudentProfile models, auth service, GitHub OAuth, auth endpoints (/register, /login, /logout, /me), useAuth hook, LoginButton component, AuthProvider wrapper, 4 test tasks

**Phase 4 - US2 Hardware Profile (14 tasks)**: HardwareConfig model with PDF enums and CHECK constraints, hardware API endpoints (/hardware-config), validation for sim_rig/edge_kit, HardwareProfileForm component, useHardwareProfile hook, profile page, 3 test tasks

**Phase 5 - US3 Hardware-Aware Chat (17 tasks)**: HardwareContextService with PDF Page 5/Page 8 logic, RAG pipeline integration, Grok prompt injection, chat endpoint updates, hardware_profile_snapshot in ChatMessage, 4 test tasks

**Phase 6 - US4 Curriculum Progress (15 tasks)**: CurriculumProgress model with week 1-13 constraints, progress API endpoints, curriculum service, CurriculumProgress component, progress page, 3 test tasks

**Phase 7 - US5 Security (15 tasks)**: Protect /api/chat, /api/ingest endpoints, 401 error handling, rate limiting, CSRF protection, security logging, 4 test tasks

**Phase 8 - Polish (11 tasks)**: Chat history, migrations, documentation, testing, validation, security hardening

**Task Summary**:
- Total: 102 tasks
- Tests: 22 test tasks (optional, included for validation)
- Backend: ~65 tasks
- Frontend: ~25 tasks
- Parallel opportunities: 40+ tasks marked [P]
- MVP scope: Phases 1-3 (30 tasks) for authentication only

## Outcome

- ✅ Impact: Actionable task list ready for immediate implementation, organized by user story for independent delivery
- 🧪 Tests: 22 test tasks included across all user stories (contract tests, integration tests, validation tests)
- 📁 Files: Created tasks.md with 102 tasks, 8 phases, dependency graph, parallel execution examples
- 🔁 Next prompts: Ready for /sp.implement to begin Phase 1 (Setup) implementation
- 🧠 Reflection: Tasks organized by user story enable parallel team execution - 3 developers can work on US1, US2, US4 simultaneously after Foundational phase

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully
- Graders run and results (PASS/FAIL): N/A - tasks phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with /sp.implement starting from Phase 1
