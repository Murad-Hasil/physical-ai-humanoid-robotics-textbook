# Tasks: Phase 6 UI/UX Renaissance - Cyber Theme Overhaul

**Input**: Design documents from `/specs/001-ui-ux-renaissance/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, quickstart.md

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `docusaurus-textbook/src/`, `docusaurus-textbook/static/`
- Paths shown below use existing Docusaurus structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment verification

- [ ] T001 Verify Node.js 20.x installed: `node --version`
- [ ] T002 Verify dependencies installed: `cd docusaurus-textbook && npm install`
- [ ] T003 [P] Verify Tailwind CSS installed: `npm list tailwindcss`
- [ ] T004 [P] Verify font files exist in `docusaurus-textbook/static/fonts/` (Inter, JetBrains Mono)
- [ ] T005 [P] Start dev server: `npm start` and verify http://localhost:3000/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core CSS infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Define cyber-black background color in `docusaurus-textbook/src/css/custom.css` (--cyber-black: #111111)
- [x] T007 [P] Define neon color palette in `docusaurus-textbook/tailwind.config.js` (neon-blue: #00F3FF, neon-orange: #FF6B35)
- [x] T008 [P] Create grid overlay background pattern in `docusaurus-textbook/src/css/custom.css` (.cyber-grid-overlay)
- [x] T009 [P] Define custom animations in `docusaurus-textbook/tailwind.config.js` (glow, float, pulse-cyan, scanline)
- [x] T010 [P] Create .glass-panel utility class in `docusaurus-textbook/src/css/custom.css`
- [x] T011 [P] Create .neon-border utility class in `docusaurus-textbook/src/css/custom.css`
- [x] T012 [P] Create .cyber-button utility class in `docusaurus-textbook/src/css/custom.css`
- [ ] T013 Configure font-face declarations in `docusaurus-textbook/src/css/custom.css` (Inter, JetBrains Mono)
- [ ] T014 Add @supports queries for backdrop-filter fallback in `docusaurus-textbook/src/css/custom.css`
- [ ] T015 Add reduced-motion media query support in `docusaurus-textbook/src/css/custom.css`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Immersive First Impression (Priority: P1) 🎯 MVP

**Goal**: Create stunning homepage hero section with cyber-theme feature cards and neon CTA buttons

**Independent Test**: User lands on homepage and sees hero section with value proposition, floating 3D cards, and neon glow buttons

### Implementation for User Story 1

- [x] T016 [P] [US1] Create HeroSection component in `docusaurus-textbook/src/pages/index.tsx`
- [x] T017 [P] [US1] Create FeatureCards component (3 cards: Edge AI, RAG, Sim-to-Real)
- [x] T018 [P] [US1] Create SocialProof component in `docusaurus-textbook/src/pages/index.tsx` (GIAIC stats)
- [x] T019 [US1] Implement split-screen hero layout (text left, UI preview right) in `index.tsx`
- [x] T020 [US1] Add headline "Physical AI: The Humanoid Robotics OS" in `index.tsx`
- [x] T021 [US1] Create 3D floating cards for Edge AI, RAG, Sim-to-Real
- [x] T022 [US1] Implement float animation for feature cards using CSS animation
- [x] T023 [US1] Add neon glow effect to CTA buttons on hover in `index.tsx`
- [x] T024 [US1] Implement scanline animation on button hover in `cyber-button` class
- [x] T025 [US1] Add GIAIC stats section (13 weeks, 50+ lessons, 100% hands-on)
- [x] T026 [US1] Update homepage in `docusaurus-textbook/src/pages/index.tsx` to use new components
- [x] T027 [US1] Add 0.2s ease-in-out transitions to all interactive elements
- [ ] T028 [US1] Test hero section at 320px, 768px, 1024px, 1920px breakpoints
- [ ] T029 [US1] Verify 60 FPS animation performance in Chrome DevTools

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Seamless Navigation Experience (Priority: P2)

**Goal**: Implement transparent navbar with backdrop blur, glowing active indicators, and glassmorphic footer

**Independent Test**: User can navigate using transparent navbar with backdrop blur and sees glowing active page indicators

### Implementation for User Story 2

- [x] T030 [P] [US2] Redesign Navbar component in `docusaurus-textbook/src/theme/Navbar.tsx`
- [x] T031 [P] [US2] Create Footer component in `docusaurus-textbook/src/theme/Footer.tsx`
- [ ] T032 [P] [US2] Create SystemStatusIndicator component in `docusaurus-textbook/src/components/UI/SystemStatusIndicator.tsx`
- [x] T033 [US2] Add transparent background with backdrop-blur-md to navbar in `Navbar.tsx`
- [x] T034 [US2] Add thin cyan bottom border to navbar (border-b-2 border-neon-blue)
- [x] T035 [US2] Add User Profile dropdown with logout option in `Navbar.tsx`
- [x] T036 [US2] Add Admin badge (neon orange) for admin users in `Navbar.tsx`
- [ ] T037 [US2] Implement glowing active-link indicators in navbar
- [x] T038 [US2] Create 4-column footer layout in `Footer.tsx`
- [x] T039 [US2] Add glassmorphic tiles for social links in `Footer.tsx`
- [x] T040 [US2] Add "Powered by GIAIC & Grok" watermark in `Footer.tsx`
- [x] T041 [US2] Add system status indicators in footer (PostgreSQL, Qdrant, Grok API)
- [ ] T042 [US2] Implement mobile-responsive navbar with hamburger menu
- [ ] T043 [US2] Add keyboard navigation support for navbar dropdowns
- [ ] T044 [US2] Test navbar integration across all pages

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Enhanced Page Experiences (Priority: P3)

**Goal**: Redesign Docs, Roadmap, Dashboard, and Auth pages with cyber-theme consistency

**Independent Test**: Each redesigned page displays cyber-theme with appropriate visual enhancements

### Implementation for User Story 3

#### Roadmap Page

- [ ] T045 [P] [US3] Create MissionTimeline component in `docusaurus-textbook/src/components/UI/MissionTimeline.tsx`
- [ ] T046 [P] [US3] Create MissionStep component in `docusaurus-textbook/src/components/UI/MissionStep.tsx`
- [ ] T047 [US3] Implement vertical timeline layout in `MissionTimeline.tsx`
- [ ] T048 [US3] Add color-coded steps (completed=green, current=cyan, locked=gray) in `MissionStep.tsx`
- [ ] T049 [US3] Implement animated progress nodes with pulse effect
- [ ] T050 [US3] Update roadmap page in `docusaurus-textbook/src/pages/roadmap.tsx` to use timeline

#### Dashboard/Profile Page

- [ ] T051 [P] [US3] Create BentoBoxGrid component in `docusaurus-textbook/src/components/UI/BentoBoxGrid.tsx`
- [ ] T052 [P] [US3] Create HardwareStatCard component in `docusaurus-textbook/src/components/UI/HardwareStatCard.tsx`
- [ ] T053 [US3] Implement tactical HUD layout in `BentoBoxGrid.tsx`
- [ ] T054 [US3] Add GPU stats cards (RTX 4070 Ti, etc.) in `HardwareStatCard.tsx`
- [ ] T055 [US3] Add Robot stats cards (Unitree, etc.) in `HardwareStatCard.tsx`
- [ ] T056 [US3] Update profile page in `docusaurus-textbook/src/pages/profile.tsx` to use bento layout

#### Auth Pages (Login/Signup)

- [ ] T057 [P] [US3] Create ImmersiveAuthLayout component in `docusaurus-textbook/src/components/UI/ImmersiveAuthLayout.tsx`
- [ ] T058 [P] [US3] Create CyberForm component in `docusaurus-textbook/src/components/UI/CyberForm.tsx`
- [ ] T059 [US3] Implement full-screen layout without navbar/footer in `ImmersiveAuthLayout.tsx`
- [ ] T060 [US3] Add centered glassmorphic form in `CyberForm.tsx`
- [ ] T061 [US3] Implement biometric-style loading animation in `CyberForm.tsx`
- [ ] T062 [US3] Update login page in `docusaurus-textbook/src/pages/login.tsx` to use immersive layout
- [ ] T063 [US3] Update signup page in `docusaurus-textbook/src/pages/signup.tsx` to use immersive layout

#### Docs/Textbook Sidebar

- [ ] T064 [P] [US3] Create CyberSidebar component in `docusaurus-textbook/src/components/UI/CyberSidebar.tsx`
- [ ] T065 [US3] Add glowing active-link indicators in `CyberSidebar.tsx`
- [ ] T066 [US3] Implement glassmorphic panel background in `CyberSidebar.tsx`
- [ ] T067 [US3] Add neon-bordered code snippet container in `docusaurus-textbook/src/css/custom.css`
- [ ] T068 [US3] Style Docusaurus main content area with cyber-theme

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Chatbot HUD Integration

**Goal**: Transform chat widget into robotic assistant interface with glowing pulse effects

**Independent Test**: Chat widget displays as robotic HUD with glowing pulse icon when AI is thinking

### Implementation for Chatbot HUD

- [ ] T069 [P] Create RoboticChatWidget component in `docusaurus-textbook/src/theme/ChatBot/RoboticChatWidget.tsx`
- [ ] T070 [P] Create ThinkingPulseIndicator component in `docusaurus-textbook/src/components/UI/ThinkingPulseIndicator.tsx`
- [ ] T071 Implement glowing pulse animation for "thinking" state in `ThinkingPulseIndicator.tsx`
- [ ] T072 Add tactical HUD styling to chat widget container
- [ ] T073 Implement cyan glow effects for chatbot avatar
- [ ] T074 Add scanline effect to chat messages
- [ ] T075 Integrate robotic chat widget with existing chat system

**Checkpoint**: Chatbot HUD fully integrated and functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories

- [ ] T076 [P] Add accessibility audit with axe DevTools
- [ ] T077 [P] Verify WCAG 2.1 AA contrast ratios for all color combinations
- [ ] T078 [P] Test keyboard navigation across all components
- [ ] T079 [P] Add visible focus indicators to all interactive elements
- [ ] T080 Test reduced motion support (@prefers-reduced-motion)
- [ ] T081 Test graceful degradation on IE11 (solid backgrounds instead of backdrop blur)
- [ ] T082 Run Lighthouse audit (target: Performance 90+, Accessibility 95+)
- [ ] T083 [P] Test cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] T084 [P] Test mobile responsiveness at all breakpoints
- [ ] T085 [P] Optimize animation performance (verify 60 FPS in DevTools)
- [ ] T086 Document design system in `docusaurus-textbook/src/css/custom.css`
- [ ] T087 Update quickstart.md with component usage examples
- [ ] T088 Code cleanup: remove unused CSS, fix linting issues
- [ ] T089 Add component documentation comments in TypeScript files
- [ ] T090 Final visual regression testing across all pages

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Chatbot HUD (Phase 6)**: Depends on Foundational phase, can run parallel to user stories
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2

### Within Each User Story

- Components marked [P] can be created in parallel (different files)
- Implementation tasks should follow: Component creation → Layout → Styling → Animation → Integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005)
- All Foundational tasks marked [P] can run in parallel (T006-T012)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All components within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- Chatbot HUD tasks marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1 (Homepage Hero)

```bash
# Launch all US1 components in parallel (different files):
Task: "Create HeroSection component in src/components/Homepage/HeroSection.tsx"
Task: "Create FeatureCards component in src/components/Homepage/FeatureCards.tsx"
Task: "Create SocialProof component in src/components/Homepage/SocialProof.tsx"

# Then implement layouts and animations:
Task: "Implement split-screen hero layout in HeroSection.tsx"
Task: "Create 3D floating cards in FeatureCards.tsx"
Task: "Add neon glow effect to CTA buttons"

# Finally integrate:
Task: "Update homepage in src/pages/index.tsx to use new components"
```

---

## Parallel Example: User Story 2 (Navigation)

```bash
# Launch all US2 components in parallel:
Task: "Redesign Navbar component in src/theme/Navbar.tsx"
Task: "Create Footer component in src/theme/Footer.tsx"
Task: "Create SystemStatusIndicator component in src/components/UI/SystemStatusIndicator.tsx"

# Then implement features:
Task: "Add transparent background with backdrop-blur-md to navbar"
Task: "Add thin cyan bottom border to navbar"
Task: "Create 4-column footer layout"

# Finally integrate and test:
Task: "Test navbar integration across all pages"
```

---

## Parallel Example: User Story 3 (Page Redesign)

```bash
# Can be split across team members by page:

# Developer A: Roadmap
Task: "Create MissionTimeline component in src/components/UI/MissionTimeline.tsx"
Task: "Create MissionStep component in src/components/UI/MissionStep.tsx"
Task: "Update roadmap page in src/pages/roadmap.tsx"

# Developer B: Dashboard
Task: "Create BentoBoxGrid component in src/components/UI/BentoBoxGrid.tsx"
Task: "Create HardwareStatCard component in src/components/UI/HardwareStatCard.tsx"
Task: "Update profile page in src/pages/profile.tsx"

# Developer C: Auth Pages
Task: "Create ImmersiveAuthLayout component in src/components/UI/ImmersiveAuthLayout.tsx"
Task: "Create CyberForm component in src/components/UI/CyberForm.tsx"
Task: "Update login.tsx and signup.tsx"

# Developer D: Docs Sidebar
Task: "Create CyberSidebar component in src/components/UI/CyberSidebar.tsx"
Task: "Add glowing active-link indicators"
Task: "Style Docusaurus main content area"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test homepage hero, feature cards, neon buttons
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test homepage independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test navigation independently → Deploy/Demo
4. Add User Story 3 → Test redesigned pages independently → Deploy/Demo
5. Add Chatbot HUD → Test robotic assistant → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Homepage Hero)
   - Developer B: User Story 2 (Navigation & Footer)
   - Developer C: User Story 3 (Page Redesigns - split by page)
   - Developer D: Chatbot HUD (Phase 6)
3. Stories complete and integrate independently
4. Team reconvenes for Polish phase (Phase 7)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **Definition of Done**: All pages display cyber-theme consistently, 60 FPS animations, WCAG 2.1 AA compliant, cross-browser tested

---

## Task Summary

**Total Tasks**: 90

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 10 tasks
- Phase 3 (US1 - Homepage Hero): 14 tasks
- Phase 4 (US2 - Navigation): 15 tasks
- Phase 5 (US3 - Page Redesigns): 24 tasks
- Phase 6 (Chatbot HUD): 7 tasks
- Phase 7 (Polish): 15 tasks

**Parallel Opportunities**:
- Setup: 3 tasks can run in parallel
- Foundational: 7 tasks can run in parallel
- US1: 3 tasks can run in parallel initially
- US2: 3 tasks can run in parallel initially
- US3: 8 tasks can run in parallel (split across 4 developers)
- Chatbot HUD: 2 tasks can run in parallel
- Polish: 6 tasks can run in parallel

**Suggested MVP Scope**: Phases 1-3 (User Story 1 only) - 29 tasks
**Full Feature Scope**: All 7 phases - 90 tasks
