---
id: 007
title: frontend-evolution-tasks
stage: tasks
date: 2026-03-16
surface: agent
model: qwen-code
feature: 001-frontend-evolution
branch: 001-frontend-evolution
user: brownie
command: /sp.tasks Target: /phase-4-frontend-evolution Instructions: 1. Global State & Context: Create src/context/HardwareContext.js to store and sync the user's selected equipment globally. Wrap the Docusaurus app with the HardwareProvider. 2. Profile & Hardware Dashboard: Create src/pages/profile.js. Build a "Hardware Config" form with the following fields (as per PDF Page 5): Workstation GPU (e.g., RTX 4070 Ti, RTX 4090), Edge Kit (Jetson Orin Nano, Jetson Orin NX), Robot (Unitree Go2, Unitree G1, Proxy). Implement "Save" functionality using PATCH /api/user/profile. 3. Curriculum Progress UI: Create a Roadmap component that renders a 13-week timeline based on the PDF Weekly Breakdown. Add toggle switches for each week to mark them as "Completed" in the database. 4. Hardware-Aware Chat UI: Add a status header to the Chat Widget that displays the user's active hardware (e.g., "Mode: Jetson Orin Nano"). Ensure the chat automatically refreshes its context when the user changes hardware in the Profile. 5. Route Protection: Implement a redirect logic: If a user is not logged in (!user), they should be redirected from /profile to the login screen. Definition of Done: A student can log in and select "Jetson Orin Nano". The Chat Widget displays "Mode: Jetson Orin Nano". The 13-week curriculum reflects the progress saved in the PostgreSQL database.
labels: ["frontend", "dashboard", "ux", "glassmorphism", "curriculum", "auth-guard", "tasks"]
links:
  spec: specs/001-frontend-evolution/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-frontend-evolution/tasks.md
tests:
  - docusaurus-textbook/src/__tests__/HardwareProfile.test.js
  - docusaurus-textbook/src/__tests__/Roadmap.test.js
  - docusaurus-textbook/src/__tests__/ChatWidget.test.js
  - docusaurus-textbook/src/__tests__/authGuard.test.js
---

## Prompt

Target: /phase-4-frontend-evolution

Instructions:
1. **Global State & Context**:
   - Create `src/context/HardwareContext.js` to store and sync the user's selected equipment globally.
   - Wrap the Docusaurus app with the `HardwareProvider`.
2. **Profile & Hardware Dashboard**:
   - Create `src/pages/profile.js`.
   - Build a "Hardware Config" form with the following fields (as per PDF Page 5):
     - Workstation GPU (e.g., RTX 4070 Ti, RTX 4090)
     - Edge Kit (Jetson Orin Nano, Jetson Orin NX)
     - Robot (Unitree Go2, Unitree G1, Proxy)
   - Implement "Save" functionality using `PATCH /api/user/profile`.
3. **Curriculum Progress UI**:
   - Create a `Roadmap` component that renders a 13-week timeline based on the PDF Weekly Breakdown.
   - Add toggle switches for each week to mark them as "Completed" in the database.
4. **Hardware-Aware Chat UI**:
   - Add a status header to the Chat Widget that displays the user's active hardware (e.g., "Mode: Jetson Orin Nano").
   - Ensure the chat automatically refreshes its context when the user changes hardware in the Profile.
5. **Route Protection**:
   - Implement a redirect logic: If a user is not logged in (`!user`), they should be redirected from `/profile` to the login screen.

Definition of Done:
- A student can log in and select "Jetson Orin Nano".
- The Chat Widget displays "Mode: Jetson Orin Nano".
- The 13-week curriculum reflects the progress saved in the PostgreSQL database.

## Response snapshot

Created comprehensive tasks.md with 80 actionable tasks organized by user story:

**Phase 1 - Setup (4 tasks)**: Verify directory structure, install dependencies, configure Tailwind dark mode, verify useAuth hook

**Phase 2 - Foundational (5 tasks)**: HardwareContext.js, HardwareProvider, wrap Root.js, Axios config, cyberpunk CSS variables

**Phase 3 - US1 Hardware Profile (10 tasks)**: Profile page, HardwareProfileForm component, GPU/Edge Kit/Robot dropdowns, PATCH /api/user/profile integration, success/error handling, glassmorphism styling

**Phase 4 - US2 Curriculum Roadmap (10 tasks)**: Roadmap page, 13-week timeline component, "Mark as Complete" toggles, API integration, visual distinction for completed weeks, hover tooltips, responsive design

**Phase 5 - US3 Enhanced Chatbot (11 tasks)**: Locate existing chatbot, SystemStatus component, hardware display ("Mode: Jetson Orin Nano"), markdown rendering, syntax highlighting for ROS 2, auto-refresh on profile change

**Phase 6 - US4 Auth Guard (9 tasks)**: AuthGuard component, redirect logic, LoginPrompt component, wrap /profile and /roadmap, loading states

**Phase 7 - US5 Cyberpunk Theme (10 tasks)**: Dark mode palette, neon blue accents (#00f0ff), glassmorphism CSS class, apply theme to all components, glow effects

**Phase 8 - Polish (11 tasks)**: End-to-end testing, error handling, mobile responsiveness, documentation, linting

**Task Summary**:
- Total: 80 tasks
- Tests: 10 optional test tasks included
- Parallel opportunities: 20+ tasks marked [P]
- MVP scope: Phases 1-3 (19 tasks) for hardware profile only

**Definition of Done**:
- Student can log in and select "Jetson Orin Nano"
- Chat Widget displays "Mode: Jetson Orin Nano"
- 13-week curriculum reflects progress saved in PostgreSQL

## Outcome

- ✅ Impact: Actionable task list ready for immediate implementation, organized by user story for independent delivery
- 🧪 Tests: 10 optional test tasks included across all user stories
- 📁 Files: Created tasks.md with 80 tasks, 8 phases, dependency graph, parallel execution examples
- 🔁 Next prompts: Ready for /sp.implement to begin Phase 1 (Setup) implementation
- 🧠 Reflection: Tasks organized by user story enable parallel team execution - 3 developers can work on US1, US2, US4 simultaneously after Foundational phase

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully
- Graders run and results (PASS/FAIL): N/A - tasks phase
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with /sp.implement starting from Phase 1
