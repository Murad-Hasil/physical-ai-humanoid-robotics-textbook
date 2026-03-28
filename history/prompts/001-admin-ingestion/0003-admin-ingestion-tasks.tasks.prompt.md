---
id: 0003
title: Admin Ingestion Dashboard Task Breakdown
stage: tasks
date: 2026-03-17
surface: agent
model: qwen-coder
feature: 001-admin-ingestion
branch: 001-admin-ingestion
user: brownie
command: /sp.tasks Target: /phase-5-admin-ingestion - Admin authorization guard, ingestion UI, knowledge base table, system health monitor, navigation integration
labels: ["tasks", "admin", "ingestion", "implementation", "tdd"]
links:
  spec: specs/001-admin-ingestion/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-admin-ingestion/tasks.md
tests:
  - TDD approach per constitution (Test-First NON-NEGOTIABLE)
---

## Prompt

Target: /phase-5-admin-ingestion

Instructions:
1. **Admin Authorization Guard**:
   - Update the `useAuth` hook to detect the `admin` role from the JWT.
   - Implement a Higher-Order Component (HOC) or Middleware to protect `/admin` routes.
2. **Ingestion UI (Upload Center)**:
   - Create `src/pages/admin/ingest.jsx`.
   - Implement a File Upload component (Drag & Drop) that sends multipart/form-data to `POST /api/ingest`.
   - Add a loading state with a progress bar for large PDF processing.
3. **Knowledge Base Table**:
   - Build a dashboard view that lists all indexed documents.
   - Implement a "Delete" or "Re-index" button for each document to manage the RAG vector space.
4. **System Health Monitor**:
   - Create a simple dashboard showing Grok API connectivity status and Database connection pool health.
5. **Final Navigation Integration**:
   - Add an "Admin Panel" link to the Navbar that ONLY appears if the user has the `admin` role.

Definition of Done:
- Only an admin user can see and access the `/admin/ingest` page.
- Admin can upload a new Markdown file and immediately see it appear in the "Indexed Documents" list.
- The Chatbot successfully answers questions from the newly uploaded content.

## Response snapshot

Generated 100 actionable tasks organized by user stories:
- Phase 1 (Setup): 4 tasks - dependency installation, verification
- Phase 2 (Foundational): 9 tasks - models, migrations, auth dependency, performance monitor
- Phase 3 (US1 - File Upload): 22 tasks - TDD tests, service, endpoints, frontend components
- Phase 4 (US2 - View Files): 13 tasks - tests, list endpoint, table component
- Phase 5 (US3 - Re-index): 14 tasks - tests, background job, progress polling
- Phase 6 (US4 - Performance): 16 tasks - tests, metrics middleware, Grok health, dashboard
- Phase 7 (US5 - Access Control): 13 tasks - tests, AdminGuard, navbar integration
- Phase 8 (Polish): 9 tasks - documentation, testing, security hardening

Key features:
- TDD approach per constitution (tests before implementation)
- Each user story independently testable
- Parallel execution opportunities identified
- MVP scope defined (Phases 1-3, 35 tasks)
- Clear file paths for all tasks

## Outcome

- ✅ Impact: Actionable task list ready for immediate implementation
- 🧪 Tests: TDD approach enforced - tests must fail before implementation
- 📁 Files: tasks.md created with 100 tasks across 8 phases
- 🔁 Next prompts: Ready for /sp.implement (start implementation) or /sp.checklist (domain checklists)
- 🧠 Reflection: Tasks organized by user story enable parallel team execution; MVP clearly defined as US1 only

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully
- Graders run and results: PASS - all tasks follow checklist format with IDs, story labels, file paths
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with Phase 1 Setup tasks
