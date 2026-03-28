---
id: 006
title: frontend-evolution-spec
stage: spec
date: 2026-03-16
surface: agent
model: qwen-code
feature: 001-frontend-evolution
branch: 001-frontend-evolution
user: brownie
command: /sp.specify Target: /phase-4-frontend-evolution Goals: 1. Interactive Hardware Dashboard: Create a /profile page in Docusaurus. UI must allow selecting: Workstation (RTX Specs), Edge Kit (Jetson Orin), and Robot (Unitree/Proxy) as per PDF Page 5. Use the PATCH /api/user/profile endpoint to sync with the backend. 2. Curriculum Roadmap (Weeks 1-13): Implement a visual "Learning Path" component based on the PDF Weekly Breakdown. Each week (e.g., Week 10: Humanoid Locomotion) should have a "Mark as Complete" toggle linked to the backend. 3. Enhanced Glassmorphism Chatbot: Upgrade the current chat widget with a "System Status" indicator. Indicator should show: Active Hardware: [User's Selected Kit]. Ensure Markdown rendering is perfect for ROS 2 code blocks and PDF-style technical notes. 4. Auth-Guarded UI: Secure the /profile and /roadmap routes. Show a "Login to Access AI Assistant" state for unauthenticated users. 5. Aesthetic Requirements: Theme: Dark Mode. Colors: Neon Blue accents, Cyberpunk-inspired Glassmorphism (semi-transparent backgrounds with blur). Constraints: Use useAuth hook and existing Axios configurations. All components must be placed in docusaurus-textbook/src/components or docusaurus-textbook/src/pages. Maintain 100% alignment with the PDF's Hardware and Curriculum structure.
labels: ["frontend", "dashboard", "ux", "glassmorphism", "curriculum", "auth-guard"]
links:
  spec: specs/001-frontend-evolution/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-frontend-evolution/spec.md
  - specs/001-frontend-evolution/checklists/requirements.md
tests:
  - null
---

## Prompt

Target: /phase-4-frontend-evolution

Goals:
1. **Interactive Hardware Dashboard**:
   - Create a `/profile` page in Docusaurus.
   - UI must allow selecting: Workstation (RTX Specs), Edge Kit (Jetson Orin), and Robot (Unitree/Proxy) as per PDF Page 5.
   - Use the `PATCH /api/user/profile` endpoint to sync with the backend.
2. **Curriculum Roadmap (Weeks 1-13)**:
   - Implement a visual "Learning Path" component based on the PDF Weekly Breakdown.
   - Each week (e.g., Week 10: Humanoid Locomotion) should have a "Mark as Complete" toggle linked to the backend.
3. **Enhanced Glassmorphism Chatbot**:
   - Upgrade the current chat widget with a "System Status" indicator.
   - Indicator should show: `Active Hardware: [User's Selected Kit]`.
   - Ensure Markdown rendering is perfect for ROS 2 code blocks and PDF-style technical notes.
4. **Auth-Guarded UI**:
   - Secure the `/profile` and `/roadmap` routes.
   - Show a "Login to Access AI Assistant" state for unauthenticated users.
5. **Aesthetic Requirements**:
   - Theme: Dark Mode.
   - Colors: Neon Blue accents, Cyberpunk-inspired Glassmorphism (semi-transparent backgrounds with blur).

Constraints:
- Use `useAuth` hook and existing Axios configurations.
- All components must be placed in `docusaurus-textbook/src/components` or `docusaurus-textbook/src/pages`.
- Maintain 100% alignment with the PDF's Hardware and Curriculum structure.

## Response snapshot

Created feature specification for Frontend Evolution including:

**5 User Stories with priorities:**
- P1: Configure Hardware Profile via Dashboard (interactive /profile page)
- P2: Track Progress with Curriculum Roadmap (13-week visual learning path)
- P3: Enhanced Glassmorphism Chatbot (system status indicator, markdown rendering)
- P4: Auth-Guarded Profile and Roadmap Routes (login protection)
- P5: Cyberpunk-Inspired Dark Mode UI (neon blue, glassmorphism effects)

**17 Functional Requirements:**
- Hardware dashboard with PDF-specified options (Workstation, Edge Kit, Robot)
- Curriculum roadmap with 13-week progression and completion tracking
- Chatbot enhancements (system status, markdown rendering)
- Route protection for /profile and /roadmap
- Aesthetic requirements (dark mode, neon blue, glassmorphism)

**11 Success Criteria:**
- Hardware profile setup in under 2 minutes (SC-001)
- 95% sync success rate (SC-002)
- Progress understanding within 30 seconds (SC-003)
- 90% student engagement with roadmap (SC-004)
- 100% system status accuracy (SC-005)
- 100% markdown rendering accuracy (SC-006)
- 100% auth guard effectiveness (SC-007)
- 85% design satisfaction (SC-008)
- <2 second page load times (SC-009)
- 80% hardware profile adoption (SC-010)
- 75% weekly engagement (SC-011)

**Key Entities:** Hardware Dashboard, Curriculum Roadmap, Week Module, System Status Indicator, Auth Guard

**8 Edge Cases:** Auth failures, sync failures, mobile responsiveness, loading states, markdown fallbacks

**Specification Quality:** All 16 checklist items passed validation

## Outcome

- ✅ Impact: Complete feature specification ready for planning phase, covering hardware dashboard, curriculum roadmap, enhanced chatbot, auth guards, and cyberpunk aesthetics
- 🧪 Tests: Specification validated against quality checklist - all 16 items passed
- 📁 Files: Created spec.md and checklists/requirements.md in specs/001-frontend-evolution/
- 🔁 Next prompts: Ready for /sp.plan to create technical architecture plan
- 🧠 Reflection: Feature description was detailed with specific aesthetic requirements (glassmorphism, neon blue, dark mode), enabling comprehensive spec creation without clarification questions. All requirements maintain alignment with PDF Hardware and Curriculum structure as specified.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully
- Graders run and results (PASS/FAIL): N/A - spec phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to technical planning phase with /sp.plan
