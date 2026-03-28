---
id: 0002
title: Admin Ingestion Dashboard Technical Plan
stage: plan
date: 2026-03-17
surface: agent
model: qwen-coder
feature: 001-admin-ingestion
branch: 001-admin-ingestion
user: brownie
command: /sp.plan Target: /phase-5-admin-ingestion - Admin authorization, ingestion pipeline UI, knowledge monitor, Grok integration
labels: ["plan", "admin", "ingestion", "rag", "architecture"]
links:
  spec: specs/001-admin-ingestion/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-admin-ingestion/plan.md
  - specs/001-admin-ingestion/research.md
  - specs/001-admin-ingestion/data-model.md
  - specs/001-admin-ingestion/contracts/openapi-spec.md
  - specs/001-admin-ingestion/quickstart.md
tests:
  - Constitution check passed (all gates)
---

## Prompt

Target: /phase-5-admin-ingestion

Instructions:
1. **Admin Authorization**:
   - Define the logic to check for `admin` role in the `useAuth` hook.
   - Plan the redirection for non-admin users trying to access `/admin`.
2. **Ingestion Pipeline UI**:
   - Plan a "Drag & Drop" file upload component using `react-dropzone` or similar.
   - Design the feedback loop: Show progress bars and "Success/Failure" toasts for each file processed by the RAG backend.
3. **Knowledge Monitor**:
   - Plan a table view to display file names, upload dates, and chunk counts from the PostgreSQL database.
4. **Integration with Grok**:
   - Plan a simple toggle to switch between "Development" and "Production" mode for API calls.

## Response snapshot

Completed technical planning for Admin Ingestion Dashboard with:
- Technical context defined (Python 3.12, TypeScript 5.6, FastAPI, Docusaurus, PostgreSQL, Qdrant)
- Constitution check passed (all 6 gates satisfied)
- Research completed: 7 technical decisions documented with alternatives considered
- Data model: 4 entities (User extended, IngestionLog, ReindexJob, PerformanceMetric)
- API contracts: 8 endpoints with full OpenAPI specification
- Quickstart guide: Step-by-step implementation instructions
- Agent context updated with new technologies (react-dropzone, python-multipart)

## Outcome

- ✅ Impact: Complete technical architecture ready for task breakdown
- 🧪 Tests: Constitution check passed, all gates satisfied
- 📁 Files: plan.md, research.md, data-model.md, contracts/openapi-spec.md, quickstart.md
- 🔁 Next prompts: Ready for /sp.tasks (task breakdown) or /sp.checklist (domain checklists)
- 🧠 Reflection: Admin role implemented as simple boolean flag (YAGNI principle); background jobs for re-indexing avoid timeout issues

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully
- Graders run and results: PASS - constitution check passed, all artifacts generated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task breakdown with /sp.tasks
