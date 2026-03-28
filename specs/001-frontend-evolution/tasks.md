# Tasks: Frontend Evolution - Dashboard and Enhanced UX

**Input**: Design documents from `/specs/001-frontend-evolution/`
**Prerequisites**: spec.md (user stories with priorities)

**Tests**: Tests are OPTIONAL - included for critical functionality validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `docusaurus-textbook/src/components/`, `docusaurus-textbook/src/pages/`, `docusaurus-textbook/src/context/`, `docusaurus-textbook/src/hooks/`
- **Backend**: Already implemented (Phase 3) - `backend/api/`, `backend/services/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Verify docusaurus-textbook directory structure exists
- [ ] T002 [P] Install required dependencies: axios (if not already installed)
- [ ] T003 [P] Verify Tailwind CSS is configured for dark mode in docusaurus-textbook/tailwind.config.js
- [ ] T004 [P] Verify existing useAuth hook is available in docusaurus-textbook/src/hooks/useAuth.js

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create global hardware context in docusaurus-textbook/src/context/HardwareContext.js with state for hardware profile
- [ ] T006 [P] Create HardwareProvider component in docusaurus-textbook/src/context/HardwareContext.js to wrap app
- [ ] T007 Update docusaurus-textbook/src/theme/Root.js to include HardwareProvider wrapper
- [ ] T008 [P] Create Axios configuration file in docusaurus-textbook/src/utils/api.js with base URL and interceptors
- [ ] T009 [P] Define CSS variables for cyberpunk theme in docusaurus-textbook/src/css/custom.css (neon blue, dark backgrounds, glassmorphism)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Configure Hardware Profile via Dashboard (Priority: P1) 🎯 MVP

**Goal**: Create interactive /profile page with hardware selection dashboard synced to backend

**Independent Test**: Can be fully tested by a logged-in student accessing /profile, selecting hardware (e.g., Jetson Orin Nano), and verifying it saves via PATCH /api/user/profile

### Tests for User Story 1 (OPTIONAL) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Test hardware profile form renders all PDF-specified options in docusaurus-textbook/src/__tests__/HardwareProfile.test.js
- [ ] T011 [P] [US1] Test PATCH /api/user/profile integration in docusaurus-textbook/src/__tests__/api.test.js

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create profile page component in docusaurus-textbook/src/pages/profile.js with basic layout
- [ ] T013 [P] [US1] Create HardwareProfileForm component in docusaurus-textbook/src/components/HardwareProfileForm.jsx with form fields
- [ ] T014 [US1] Add Workstation GPU dropdown field (RTX 4070 Ti, RTX 4090) in docusaurus-textbook/src/components/HardwareProfileForm.jsx
- [ ] T015 [US1] Add Edge Kit dropdown field (Jetson Orin Nano, Jetson Orin NX) in docusaurus-textbook/src/components/HardwareProfileForm.jsx
- [ ] T016 [US1] Add Robot dropdown field (Unitree Go2, Unitree G1, Proxy) in docusaurus-textbook/src/components/HardwareProfileForm.jsx
- [ ] T017 [US1] Implement form submission with PATCH /api/user/profile in docusaurus-textbook/src/components/HardwareProfileForm.jsx using Axios
- [ ] T018 [US1] Add success/error notification handling in docusaurus-textbook/src/components/HardwareProfileForm.jsx
- [ ] T019 [US1] Add loading state during API calls in docusaurus-textbook/src/components/HardwareProfileForm.jsx
- [ ] T020 [US1] Integrate HardwareContext to update global state on save in docusaurus-textbook/src/components/HardwareProfileForm.jsx
- [ ] T021 [US1] Add glassmorphism styling to profile page in docusaurus-textbook/src/pages/profile.js

**Checkpoint**: At this point, User Story 1 should be fully functional - students can configure hardware and it syncs to backend

---

## Phase 4: User Story 2 - Track Progress with Curriculum Roadmap (Priority: P2)

**Goal**: Create visual 13-week learning path with completion tracking

**Independent Test**: Can be fully tested by a student accessing /roadmap, viewing all 13 weeks, toggling weeks as complete, and verifying progress saves to backend

### Tests for User Story 2 (OPTIONAL) ⚠️

- [ ] T022 [P] [US2] Test roadmap renders all 13 weeks in docusaurus-textbook/src/__tests__/Roadmap.test.js
- [ ] T023 [P] [US2] Test week completion toggle API integration in docusaurus-textbook/src/__tests__/api.test.js

### Implementation for User Story 2

- [ ] T024 [P] [US2] Create roadmap page in docusaurus-textbook/src/pages/roadmap.js with basic layout
- [ ] T025 [P] [US2] Create Roadmap component in docusaurus-textbook/src/components/Roadmap.jsx with 13-week timeline
- [ ] T026 [US2] Define week data structure with titles from PDF (Week 1-13) in docusaurus-textbook/src/components/Roadmap.jsx
- [ ] T027 [US2] Add "Mark as Complete" toggle switch for each week in docusaurus-textbook/src/components/Roadmap.jsx
- [ ] T028 [US2] Implement API call to save week completion in docusaurus-textbook/src/components/Roadmap.jsx using Axios
- [ ] T029 [US2] Add visual distinction for completed weeks (color change, checkmark) in docusaurus-textbook/src/components/Roadmap.jsx
- [ ] T030 [US2] Add hover tooltip showing week details (e.g., "Week 10: Humanoid Locomotion") in docusaurus-textbook/src/components/Roadmap.jsx
- [ ] T031 [US2] Fetch existing progress from backend on page load in docusaurus-textbook/src/components/Roadmap.jsx
- [ ] T032 [US2] Add glassmorphism styling to roadmap cards in docusaurus-textbook/src/components/Roadmap.jsx
- [ ] T033 [US2] Make roadmap responsive for mobile devices in docusaurus-textbook/src/components/Roadmap.jsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - hardware profile and progress tracking functional

---

## Phase 5: User Story 3 - Enhanced Glassmorphism Chatbot with Hardware Status (Priority: P3)

**Goal**: Upgrade chatbot widget with system status indicator showing active hardware and perfect markdown rendering

**Independent Test**: Can be fully tested by a student opening chatbot and verifying system status shows their hardware, code blocks render correctly, and markdown displays properly

### Tests for User Story 3 (OPTIONAL) ⚠️

- [ ] T034 [P] [US3] Test system status indicator displays hardware in docusaurus-textbook/src/__tests__/ChatWidget.test.js
- [ ] T035 [P] [US3] Test markdown rendering for code blocks in docusaurus-textbook/src/__tests__/MarkdownRenderer.test.js

### Implementation for User Story 3

- [ ] T036 [P] [US3] Locate existing chatbot widget component (search in docusaurus-textbook/src/components/)
- [ ] T037 [P] [US3] Create SystemStatus component in docusaurus-textbook/src/components/SystemStatus.jsx to display active hardware
- [ ] T038 [US3] Integrate SystemStatus into chatbot widget header
- [ ] T039 [US3] Connect SystemStatus to HardwareContext to display user's hardware (e.g., "Mode: Jetson Orin Nano")
- [ ] T040 [US3] Add "Not Configured" state for users without hardware profile with link to /profile
- [ ] T041 [US3] Verify markdown renderer is configured (react-markdown or similar)
- [ ] T042 [US3] Add syntax highlighting for ROS 2 code blocks (prismjs or highlight.js)
- [ ] T043 [US3] Test markdown rendering with PDF-style technical notes (bold, lists, code)
- [ ] T044 [US3] Add glassmorphism styling to chatbot widget
- [ ] T045 [US3] Add neon blue accent colors to chatbot interactive elements
- [ ] T046 [US3] Implement auto-refresh of hardware status when profile changes in HardwareContext

**Checkpoint**: At this point, User Stories 1-3 should all work - hardware profile, roadmap, and enhanced chatbot functional

---

## Phase 6: User Story 4 - Auth-Guarded Profile and Roadmap Routes (Priority: P4)

**Goal**: Secure /profile and /roadmap routes behind authentication with redirect for unauthenticated users

**Independent Test**: Can be fully tested by an unauthenticated user attempting to access /profile or /roadmap and being shown "Login to Access" state

### Tests for User Story 4 (OPTIONAL) ⚠️

- [ ] T047 [P] [US4] Test unauthenticated redirect from /profile in docusaurus-textbook/src/__tests__/authGuard.test.js
- [ ] T048 [P] [US4] Test unauthenticated redirect from /roadmap in docusaurus-textbook/src/__tests__/authGuard.test.js

### Implementation for User Story 4

- [ ] T049 [P] [US4] Create AuthGuard component in docusaurus-textbook/src/components/AuthGuard.jsx with authentication check
- [ ] T050 [US4] Implement redirect logic using useAuth hook in docusaurus-textbook/src/components/AuthGuard.jsx
- [ ] T051 [US4] Create "Login to Access AI Assistant" state component in docusaurus-textbook/src/components/LoginPrompt.jsx
- [ ] T052 [US4] Add login button that triggers useAuth login flow in docusaurus-textbook/src/components/LoginPrompt.jsx
- [ ] T053 [US4] Wrap /profile page with AuthGuard in docusaurus-textbook/src/pages/profile.js
- [ ] T054 [US4] Wrap /roadmap page with AuthGuard in docusaurus-textbook/src/pages/roadmap.js
- [ ] T055 [US4] Add loading state while authentication check is in progress in docusaurus-textbook/src/components/AuthGuard.jsx
- [ ] T056 [US4] Test authenticated users can access pages normally
- [ ] T057 [US4] Add glassmorphism styling to LoginPrompt component

**Checkpoint**: At this point, User Stories 1-4 should all work - routes are protected, only authenticated users can access

---

## Phase 7: User Story 5 - Cyberpunk-Inspired Dark Mode UI (Priority: P5)

**Goal**: Apply consistent dark mode theme with neon blue accents and glassmorphism effects across all components

**Independent Test**: Can be fully tested by a student viewing any page and verifying dark mode, neon blue accents, and glassmorphism effects are applied

### Tests for User Story 5 (OPTIONAL) ⚠️

- [ ] T058 [P] [US5] Test dark mode is active on all pages in docusaurus-textbook/src/__tests__/theme.test.js
- [ ] T059 [P] [US5] Test glassmorphism effects are applied to cards in docusaurus-textbook/src/__tests__/styling.test.js

### Implementation for User Story 5

- [ ] T060 [P] [US5] Define dark mode color palette in docusaurus-textbook/tailwind.config.js (dark backgrounds, text colors)
- [ ] T061 [P] [US5] Define neon blue accent color (#00f0ff or similar) in docusaurus-textbook/tailwind.config.js
- [ ] T062 [US5] Create glassmorphism CSS class in docusaurus-textbook/src/css/custom.css (semi-transparent background, backdrop-blur)
- [ ] T063 [US5] Apply dark mode background to all pages (profile, roadmap, home)
- [ ] T064 [US5] Apply neon blue hover effects to buttons and interactive elements
- [ ] T065 [US5] Apply glassmorphism to all cards and panels (profile cards, roadmap weeks, chatbot)
- [ ] T066 [US5] Ensure consistent theme across navigation and header
- [ ] T067 [US5] Test theme consistency across all components
- [ ] T068 [US5] Add subtle glow effects to neon blue elements (box-shadow with neon color)
- [ ] T069 [US5] Optimize glassmorphism performance (will-change property for backdrop-filter)

**Checkpoint**: All user stories should now be complete with consistent cyberpunk theme

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, testing, and documentation

- [ ] T070 [P] Test complete user flow: login → configure hardware → view roadmap → use chatbot
- [ ] T071 [P] Test error handling for failed API calls (network errors, 401, 500)
- [ ] T072 [P] Test loading states for all async operations
- [ ] T073 [P] Verify mobile responsiveness for /profile and /roadmap
- [ ] T074 [P] Add error boundaries to catch React errors
- [ ] T075 [P] Document component usage in docusaurus-textbook/src/components/README.md
- [ ] T076 [P] Verify all API endpoints use correct base URL from environment
- [ ] T077 [P] Run linter and fix any issues (eslint, prettier)
- [ ] T078 [P] Test with different user accounts and hardware configurations
- [ ] T079 [P] Verify chatbot hardware status updates when profile changes
- [ ] T080 [P] Create user guide for new students in docusaurus-textbook/docs/user-guide.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 for hardware context
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Cross-cutting, applies to all stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Components before integration
- Basic functionality before styling
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T002, T003, T004 can run in parallel
- **Foundational Phase**: T005, T006, T008, T009 can run in parallel
- **User Story 1**: T012, T013 can run in parallel
- **User Story 2**: T024, T025 can run in parallel
- **User Story 3**: T036, T037 can run in parallel
- **User Story 4**: T049, T051 can run in parallel
- **User Story 5**: T060, T061, T062 can run in parallel
- **Polish Phase**: T070-T080 can run in parallel

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Hardware Profile)
   - Developer B: User Story 2 (Curriculum Roadmap)
   - Developer C: User Story 4 (Auth Guard)
3. After US1 complete:
   - Developer A: User Story 3 (Enhanced Chatbot) - needs hardware context from US1
4. After all stories complete:
   - Team: User Story 5 (Polish & Theme) + Phase 8

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Test hardware profile form renders all PDF-specified options"
Task: "Test PATCH /api/user/profile integration"

# Launch all components for User Story 1 together:
Task: "Create profile page component in docusaurus-textbook/src/pages/profile.js"
Task: "Create HardwareProfileForm component in docusaurus-textbook/src/components/HardwareProfileForm.jsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test hardware profile configuration
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP: Hardware Profile!)
3. Add User Story 2 → Test independently → Deploy/Demo (Roadmap!)
4. Add User Story 3 → Test independently → Deploy/Demo (Enhanced Chatbot!)
5. Add User Story 4 → Test independently → Deploy/Demo (Auth Guard!)
6. Add User Story 5 → Test independently → Deploy/Demo (Full Theme!)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With 3 developers:

**Week 1**: Team completes Setup + Foundational together

**Week 2**:
- Dev A: User Story 1 (T012-T021) - Hardware Profile
- Dev B: User Story 2 (T024-T033) - Curriculum Roadmap
- Dev C: User Story 4 (T049-T057) - Auth Guard

**Week 3**:
- Dev A: User Story 3 (T036-T046) - Enhanced Chatbot (needs US1 complete)
- Dev B+C: Complete User Story 5 (T060-T069) - Theme

**Week 4**:
- Team: Polish & Cross-Cutting (T070-T080)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests included)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **Definition of Done**: Student can log in, select "Jetson Orin Nano", chatbot displays "Mode: Jetson Orin Nano", 13-week curriculum reflects progress saved in PostgreSQL
