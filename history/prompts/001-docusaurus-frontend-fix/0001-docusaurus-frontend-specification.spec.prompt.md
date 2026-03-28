---
id: 0001
title: Docusaurus Frontend Specification
stage: spec
date: 2026-03-17
surface: agent
model: qwen-coder-plus
feature: 001-docusaurus-frontend-fix
branch: 001-docusaurus-frontend-fix
user: brownie
command: /sp.implement Target: /docusaurus-frontend-fix
labels: ["specification","frontend","docusaurus","authentication","hardware-dashboard"]
links:
  spec: specs/001-docusaurus-frontend-fix/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-docusaurus-frontend-fix/spec.md
  - specs/001-docusaurus-frontend-fix/checklists/requirements.md
tests:
  - null
---

## Prompt

Target: /docusaurus-frontend-fix

Instructions:
1. **Create Missing Pages**:
   - Create `src/pages/login.jsx`: Must include a glassmorphic login form (Email/Password) connected to the Better-Auth backend.
   - Create `src/pages/signup.jsx`: For new student registration.
   - Create `src/pages/profile.jsx`: This is the **Hardware Dashboard**. Include dropdowns for RTX GPUs, Jetson Kits, and Unitree Robots (as per PDF Page 5).
   - Create `src/pages/roadmap.jsx`: A visual 13-week tracker using the PDF's curriculum data.

2. **Navbar Integration (CRITICAL)**:
   - Modify `docusaurus.config.js`. 
   - Add `{to: '/profile', label: 'Hardware Dashboard', position: 'left'}`.
   - Add `{to: '/roadmap', label: '13-Week Roadmap', position: 'left'}`.
   - Add `{to: '/login', label: 'Login', position: 'right'}`.

3. **Global Chatbot Mounting**:
   - Open `src/theme/Root.jsx` (or create it if it doesn't exist).
   - Wrap the children with the `AuthProvider` and `HardwareProvider`.
   - Mount the `ChatWidget` component here so it is visible on EVERY page of the textbook.

4. **Styling**:
   - Use Tailwind classes: `bg-slate-900/50 backdrop-blur-md border border-blue-500/20` for all cards to give that "Cyberpunk/Neon" look you want.

Definition of Done:
- Browser refresh karne par Navbar mein "Hardware Dashboard" aur "Login" nazar aa raha hai.
- `/login` page par form display ho raha hai.
- Chatbot bottom-right corner mein visible hai.

## Response snapshot

Created feature specification for Docusaurus Frontend Fix with:
- 6 user stories covering login, signup, hardware dashboard, roadmap, chatbot, and navigation
- 13 functional requirements
- 4 key entities defined
- 8 measurable success criteria
- Specification quality checklist created and validated (all items passed)

## Outcome

- ✅ Impact: Specification defines complete frontend feature with login, signup, hardware dashboard, roadmap, chatbot integration, and navbar navigation
- 🧪 Tests: Acceptance scenarios defined for all user stories; ready for task creation
- 📁 Files: 2 files created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.plan to create technical implementation plan
- 🧠 Reflection: Specification intentionally avoids implementation details (React, Tailwind, Better-Auth mentioned in user input but not in spec)

## Evaluation notes (flywheel)

- Failure modes observed: None - specification passed all quality checks on first review
- Graders run and results (PASS/FAIL): PASS - All checklist items validated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.plan for technical architecture
