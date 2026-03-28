---
id: 002
title: hardware-aware-auth-plan
stage: plan
date: 2026-03-16
surface: agent
model: qwen-code
feature: 001-hardware-aware-auth
branch: 001-hardware-aware-auth
user: brownie
command: /sp.plan Target: /phase-3-auth-personalization Instructions: 1. Technical Architecture: Design the schema for the UserProfile and HardwareConfig models. Fields must map to the PDF: gpu_vram, ubuntu_version, edge_kit_type (Orin Nano/NX), and robot_model (Go2/G1/Proxy). Plan the Better-Auth installation within the /backend/auth directory, using a database adapter (e.g., SQLite or PostgreSQL) that supports these JSON hardware fields. 2. Logic Design: Create a Context Injection Service: This service must fetch the user's hardware profile and prepend a "Hardware Constraint" instruction to the Grok API prompt. Logic Rule: If user hardware = "Jetson Orin Nano", Grok must prioritize "Inference" and "Sim-to-Real" advice from Page 8 of the PDF. 3. Curriculum Tracking: Map the "Weekly Breakdown" (Weeks 1-13) into a database table to allow students to mark modules as "Complete." 4. Security & Integration: Design a FastAPI middleware to validate Better-Auth session tokens for all /api/chat and /api/ingest calls. 5. UI Strategy: Plan how the Docusaurus frontend will display the "Hardware Setup" form for new students. Technical Risks: Token synchronization between Docusaurus (React) and the FastAPI backend. Ensuring the "Hardware Context" doesn't override the textbook's specific technical steps.
labels: ["authentication", "personalization", "hardware-aware", "rag", "better-auth", "pdf-curriculum", "technical-plan"]
links:
  spec: specs/001-hardware-aware-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-hardware-aware-auth/plan.md
  - specs/001-hardware-aware-auth/research.md
  - specs/001-hardware-aware-auth/data-model.md
  - specs/001-hardware-aware-auth/contracts/api-contracts.yaml
  - specs/001-hardware-aware-auth/quickstart.md
  - QWEN.md
tests:
  - null
---

## Prompt

Target: /phase-3-auth-personalization

Instructions:
1. **Technical Architecture**:
   - Design the schema for the `UserProfile` and `HardwareConfig` models. Fields must map to the PDF: `gpu_vram`, `ubuntu_version`, `edge_kit_type` (Orin Nano/NX), and `robot_model` (Go2/G1/Proxy).
   - Plan the **Better-Auth** installation within the `/backend/auth` directory, using a database adapter (e.g., SQLite or PostgreSQL) that supports these JSON hardware fields.
2. **Logic Design**:
   - Create a **Context Injection Service**: This service must fetch the user's hardware profile and prepend a "Hardware Constraint" instruction to the Grok API prompt.
   - *Logic Rule*: If user hardware = "Jetson Orin Nano", Grok must prioritize "Inference" and "Sim-to-Real" advice from Page 8 of the PDF.
3. **Curriculum Tracking**:
   - Map the "Weekly Breakdown" (Weeks 1-13) into a database table to allow students to mark modules as "Complete."
4. **Security & Integration**:
   - Design a FastAPI middleware to validate Better-Auth session tokens for all `/api/chat` and `/api/ingest` calls.
5. **UI Strategy**:
   - Plan how the Docusaurus frontend will display the "Hardware Setup" form for new students.

Technical Risks:
- Token synchronization between Docusaurus (React) and the FastAPI backend.
- Ensuring the "Hardware Context" doesn't override the textbook's specific technical steps.

## Response snapshot

Created comprehensive technical implementation plan for hardware-aware authentication and personalization:

**Phase 0 - Research (research.md)**:
- Better-Auth integration with FastAPI via session cookies + JWT
- Database schema design with JSONB for PDF-specified hardware profiles
- Context injection service architecture with PDF Page 5 and Page 8 logic
- FastAPI authentication middleware pattern
- Curriculum progress tracking schema (Weeks 1-13)
- Frontend hardware setup form strategy with PDF-based dropdowns
- Token synchronization between Docusaurus and FastAPI

**Phase 1 - Design**:
- data-model.md: 6 entities (User, StudentProfile, HardwareConfig, CurriculumProgress, ChatSession, ChatMessage) with PDF-specified CHECK constraints
- contracts/api-contracts.yaml: OpenAPI spec with 15+ endpoints, hardware enums, error taxonomy
- quickstart.md: 25-minute setup guide with environment config, GitHub OAuth, migration steps, testing procedures
- Updated QWEN.md with Active Technologies section

**Constitution Check**: All 5 gates passed (Sequential Phase Execution, Workflow Integrity, Contract Adherence, Tooling Constraints, Phase Completion Gates)

## Outcome

- ✅ Impact: Complete technical plan ready for task breakdown, covering Better-Auth integration, PDF hardware profiles, context injection service, curriculum tracking, and security
- 🧪 Tests: Constitution check re-evaluated post-design - all gates passed
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/api-contracts.yaml, quickstart.md, updated QWEN.md
- 🔁 Next prompts: Ready for /sp.tasks to break plan into testable implementation tasks
- 🧠 Reflection: Technical risks addressed via mitigation strategies: (1) Token sync via shared JWT secret, (2) Hardware context isolation via XML delimiters and explicit instructions to not override textbook steps

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed successfully
- Graders run and results (PASS/FAIL): N/A - plan phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task breakdown with /sp.tasks
