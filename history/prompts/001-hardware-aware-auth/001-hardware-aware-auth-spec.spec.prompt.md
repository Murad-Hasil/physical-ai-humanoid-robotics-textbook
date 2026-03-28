---
id: 001
title: hardware-aware-auth-spec
stage: spec
date: 2026-03-16
surface: agent
model: qwen-code
feature: 001-hardware-aware-auth
branch: 001-hardware-aware-auth
user: brownie
command: /sp.specify Target: /phase-3-auth-personalization Goals: 1. Strict PDF Hardware Profile: Implement a user profile system that stores the specific hardware mentioned in the PDF (Workstation: RTX 4070 Ti+ 12GB VRAM / Ubuntu 22.04, Edge Kit: Jetson Orin Nano/NX, Sensors: RealSense D435i, Robot: Unitree Go2/G1/Proxy). 2. Better-Auth Integration: Set up email/password and GitHub authentication for students. 3. Hardware-Aware RAG Logic: Modify the /chat endpoint so it retrieves the user's hardware profile and injects it into the Grok API prompt. The AI must tailor its advice based on whether the student is on a "Sim Rig" or an "Edge Kit". 4. Curriculum Milestone Tracking: Create a progress tracker for the "Weekly Breakdown" (Weeks 1-13) as defined in the PDF. 5. Backend Protection: Secure all API endpoints (chat, ingest, profile) using Better-Auth session/JWT tokens. Constraints: - Database must support hardware-specific JSON fields. - System prompts for Grok must prioritize the "Hardware Reality" section of the PDF (Page 5). - All code must reside in /backend/auth or /phase-3-auth-personalization.
labels: ["authentication", "personalization", "hardware-aware", "rag", "better-auth", "pdf-curriculum"]
links:
  spec: specs/001-hardware-aware-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-hardware-aware-auth/spec.md
  - specs/001-hardware-aware-auth/checklists/requirements.md
tests:
  - null
---

## Prompt

Target: /phase-3-auth-personalization Goals: 1. **Strict PDF Hardware Profile**: Implement a user profile system that stores the specific hardware mentioned in the PDF (Workstation: RTX 4070 Ti+ 12GB VRAM / Ubuntu 22.04, Edge Kit: Jetson Orin Nano/NX, Sensors: RealSense D435i, Robot: Unitree Go2/G1/Proxy). 2. **Better-Auth Integration**: Set up email/password and GitHub authentication for students. 3. **Hardware-Aware RAG Logic**: Modify the `/chat` endpoint so it retrieves the user's hardware profile and injects it into the Grok API prompt. The AI must tailor its advice based on whether the student is on a "Sim Rig" or an "Edge Kit". 4. **Curriculum Milestone Tracking**: Create a progress tracker for the "Weekly Breakdown" (Weeks 1-13) as defined in the PDF. 5. **Backend Protection**: Secure all API endpoints (chat, ingest, profile) using Better-Auth session/JWT tokens. Constraints: - Database must support hardware-specific JSON fields. - System prompts for Grok must prioritize the "Hardware Reality" section of the PDF (Page 5). - All code must reside in `/backend/auth` or `/phase-3-auth-personalization`.

## Response snapshot

Created feature specification for hardware-aware authentication and personalization system including:
- 5 prioritized user stories (authentication, hardware profile from PDF, hardware-aware chatbot, curriculum progress tracking, secure API access)
- 18 functional requirements covering authentication, PDF-specified hardware profiles, hardware-aware RAG responses, and curriculum tracking
- 6 key entities (Student, StudentProfile, HardwareProfile, CurriculumProgress, ChatSession, ChatMessage)
- 11 measurable success criteria focused on user experience, security, and hardware-aware response accuracy
- Specification quality checklist created and all items passed validation
- No [NEEDS CLARIFICATION] markers remain - made informed guesses based on PDF specifications and industry standards
- Hardware profiles explicitly tied to PDF "Hardware Reality" section (Page 5) with Sim Rig vs Edge Kit differentiation

## Outcome

- ✅ Impact: Complete feature specification ready for planning phase, covering authentication, PDF-based hardware personalization, and curriculum tracking
- 🧪 Tests: Specification validated against quality checklist - all 16 items passed
- 📁 Files: Created spec.md and checklists/requirements.md in specs/001-hardware-aware-auth/
- 🔁 Next prompts: Ready for /sp.plan to create technical architecture plan
- 🧠 Reflection: Feature description was detailed with specific PDF hardware references, enabling comprehensive spec creation without clarification questions. Hardware-aware response accuracy metrics (SC-010, SC-011) added to ensure personalization effectiveness.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully
- Graders run and results (PASS/FAIL): N/A - spec phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to technical planning phase with /sp.plan
