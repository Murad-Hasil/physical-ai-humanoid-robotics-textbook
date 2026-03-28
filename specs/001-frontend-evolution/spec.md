# Feature Specification: Frontend Evolution - Dashboard and Enhanced UX

**Feature Branch**: `001-frontend-evolution`
**Created**: 2026-03-16
**Status**: Draft
**Input**: User description: "Target: /phase-4-frontend-evolution Goals: 1. Interactive Hardware Dashboard: Create a /profile page in Docusaurus. UI must allow selecting: Workstation (RTX Specs), Edge Kit (Jetson Orin), and Robot (Unitree/Proxy) as per PDF Page 5. Use the PATCH /api/user/profile endpoint to sync with the backend. 2. Curriculum Roadmap (Weeks 1-13): Implement a visual "Learning Path" component based on the PDF Weekly Breakdown. Each week (e.g., Week 10: Humanoid Locomotion) should have a "Mark as Complete" toggle linked to the backend. 3. Enhanced Glassmorphism Chatbot: Upgrade the current chat widget with a "System Status" indicator. Indicator should show: `Active Hardware: [User's Selected Kit]`. Ensure Markdown rendering is perfect for ROS 2 code blocks and PDF-style technical notes. 4. Auth-Guarded UI: Secure the /profile and /roadmap routes. Show a "Login to Access AI Assistant" state for unauthenticated users. 5. Aesthetic Requirements: Theme: Dark Mode. Colors: Neon Blue accents, Cyberpunk-inspired Glassmorphism (semi-transparent backgrounds with blur). Constraints: Use `useAuth` hook and existing Axios configurations. All components must be placed in `docusaurus-textbook/src/components` or `docusaurus-textbook/src/pages`. Maintain 100% alignment with the PDF's Hardware and Curriculum structure."

## User Scenarios & Testing

### User Story 1 - Configure Hardware Profile via Dashboard (Priority: P1)

As a student, I want to configure my hardware setup through an interactive dashboard so that I receive personalized guidance tailored to my specific equipment (Workstation, Edge Kit, or Robot).

**Why this priority**: Hardware configuration is the foundation for personalized learning. Without a hardware profile, the system cannot provide tailored advice for ROS 2 commands, deployment strategies, or simulation setups.

**Independent Test**: Can be fully tested by a logged-in student accessing the /profile page, selecting their hardware (e.g., RTX 4070 Ti Workstation or Jetson Orin Nano Edge Kit), and verifying the selection is saved and reflected in the chatbot's system status indicator.

**Acceptance Scenarios**:

1. **Given** a logged-in student, **When** they navigate to /profile, **Then** they see an interactive hardware dashboard with PDF-specified options (Workstation, Edge Kit, Robot)
2. **Given** a student on the profile page, **When** they select "Jetson Orin Nano" as their Edge Kit, **Then** the selection is saved via PATCH /api/user/profile and confirmed with a success message
3. **Given** a student with a saved hardware profile, **When** they view the chatbot widget, **Then** they see "Active Hardware: Jetson Orin Nano" in the system status indicator
4. **Given** a student viewing their profile, **When** they change their robot from "Unitree Go2" to "Proxy", **Then** the change is reflected immediately and synced with the backend

---

### User Story 2 - Track Progress with Curriculum Roadmap (Priority: P2)

As a student, I want to visualize my learning journey through a 13-week roadmap with progress tracking so that I can see which weeks I've completed and what remains ahead.

**Why this priority**: Progress tracking provides motivation and helps students understand their position in the curriculum. The visual roadmap makes the learning path clear and achievable.

**Independent Test**: Can be fully tested by a student accessing the /roadmap page, viewing all 13 weeks with their titles (e.g., Week 10: Humanoid Locomotion), toggling weeks as complete, and verifying the progress is saved.

**Acceptance Scenarios**:

1. **Given** a logged-in student, **When** they navigate to /roadmap, **Then** they see a visual learning path showing all 13 weeks from the PDF Weekly Breakdown
2. **Given** a student viewing the roadmap, **When** they click "Mark as Complete" on Week 5, **Then** the week is marked complete and the progress is saved to the backend
3. **Given** a student with partial progress (e.g., Weeks 1-5 completed), **When** they view the roadmap, **Then** completed weeks are visually distinguished from remaining weeks
4. **Given** a student viewing the roadmap, **When** they hover over a week, **Then** they see additional details about that week's topics (e.g., "Week 10: Humanoid Locomotion")

---

### User Story 3 - Enhanced Glassmorphism Chatbot with Hardware Status (Priority: P3)

As a student, I want the chatbot widget to display my active hardware configuration and render technical content perfectly so that I can easily read ROS 2 code blocks and technical notes while chatting.

**Why this priority**: The chatbot is the primary interface for getting help. Clear hardware status visibility ensures students know their profile is active, and perfect markdown rendering is essential for understanding technical content.

**Independent Test**: Can be fully tested by a student opening the chatbot widget and verifying the system status indicator shows their hardware, code blocks are properly formatted, and markdown renders correctly.

**Acceptance Scenarios**:

1. **Given** a student with a saved hardware profile, **When** they open the chatbot widget, **Then** they see "Active Hardware: [Their Hardware]" in the system status indicator
2. **Given** a student asking a technical question, **When** the chatbot responds with ROS 2 code, **Then** the code is displayed in a properly formatted code block with syntax highlighting
3. **Given** a student viewing the chatbot, **When** the response includes technical notes from the PDF, **Then** the notes are rendered with proper formatting (bold, lists, etc.)
4. **Given** a student without a hardware profile, **When** they open the chatbot, **Then** they see "Active Hardware: Not Configured" with a prompt to set up their profile

---

### User Story 4 - Auth-Guarded Profile and Roadmap Routes (Priority: P4)

As a student, I want the profile and roadmap pages to be secured so that only authenticated users can access their personal data and progress tracking.

**Why this priority**: Security and privacy require that personal data (hardware profiles, progress) are only accessible to authenticated users. This also encourages account creation for full platform access.

**Independent Test**: Can be fully tested by an unauthenticated user attempting to access /profile or /roadmap and being shown a "Login to Access" state, while authenticated users can access these pages normally.

**Acceptance Scenarios**:

1. **Given** an unauthenticated visitor, **When** they navigate to /profile, **Then** they see a "Login to Access AI Assistant" state with a login button
2. **Given** an unauthenticated visitor, **When** they navigate to /roadmap, **Then** they see a "Login to Access" state with a login button
3. **Given** an authenticated student, **When** they navigate to /profile, **Then** they can access the hardware dashboard normally
4. **Given** an authenticated student, **When** they navigate to /roadmap, **Then** they can access the curriculum roadmap and track their progress

---

### User Story 5 - Cyberpunk-Inspired Dark Mode UI (Priority: P5)

As a student, I want a visually appealing dark mode interface with neon blue accents and glassmorphism effects so that the learning experience feels modern and engaging.

**Why this priority**: Aesthetics significantly impact user engagement and perceived quality. The cyberpunk/glassmorphism theme creates a distinctive, professional look that aligns with the cutting-edge nature of Physical AI education.

**Independent Test**: Can be fully tested by a student viewing any page and verifying dark mode is active, neon blue accents are present, and glassmorphism effects (semi-transparent backgrounds with blur) are applied to cards and widgets.

**Acceptance Scenarios**:

1. **Given** a student viewing any page, **When** the page loads, **Then** dark mode theme is active with appropriate dark backgrounds
2. **Given** a student viewing interactive elements, **When** they see buttons and cards, **Then** neon blue accents are visible on hover states and active elements
3. **Given** a student viewing the chatbot or dashboard, **When** they see panels and cards, **Then** glassmorphism effects (semi-transparent backgrounds with blur) are applied
4. **Given** a student using the platform, **When** they navigate between pages, **Then** the visual theme remains consistent across all components

---

### Edge Cases

- What happens when a student tries to access /profile without logging in? (Should show "Login to Access" state)
- How does the system handle hardware profile sync failures? (Should show error message and retry option)
- What happens when a student marks a week as complete but the backend request fails? (Should revert UI and show error)
- How does the chatbot display hardware status for users without a saved profile? (Should show "Not Configured" with setup prompt)
- What happens when markdown rendering fails for code blocks? (Should fallback to plain text with clear formatting)
- How does the UI handle very long week titles or descriptions in the roadmap? (Should truncate with ellipsis and show full text on hover)
- What happens if the useAuth hook returns loading state indefinitely? (Should timeout and show error after reasonable delay)
- How does the system handle students accessing the roadmap on mobile devices? (Should be responsive and maintain functionality)

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a /profile page with interactive hardware selection dashboard
- **FR-002**: System MUST allow students to select Workstation (RTX Specs), Edge Kit (Jetson Orin), and Robot (Unitree/Proxy) as per PDF Page 5
- **FR-003**: System MUST sync hardware profile changes with backend via PATCH /api/user/profile endpoint
- **FR-004**: System MUST provide a /roadmap page with visual 13-week learning path component
- **FR-005**: System MUST display each week from the PDF Weekly Breakdown with title and "Mark as Complete" toggle
- **FR-006**: System MUST save week completion status to backend when toggled
- **FR-007**: System MUST display "Active Hardware: [User's Hardware]" in chatbot system status indicator
- **FR-008**: System MUST render markdown perfectly for ROS 2 code blocks and PDF-style technical notes in chatbot
- **FR-009**: System MUST secure /profile and /roadmap routes behind authentication
- **FR-010**: System MUST show "Login to Access AI Assistant" state for unauthenticated users on protected routes
- **FR-011**: System MUST implement dark mode theme across all pages
- **FR-012**: System MUST apply neon blue accent colors to interactive elements and hover states
- **FR-013**: System MUST apply glassmorphism effects (semi-transparent backgrounds with blur) to cards, panels, and widgets
- **FR-014**: System MUST use the existing useAuth hook for authentication state management
- **FR-015**: System MUST use existing Axios configurations for API calls
- **FR-016**: System MUST place all new components in docusaurus-textbook/src/components or docusaurus-textbook/src/pages
- **FR-017**: System MUST maintain 100% alignment with PDF's Hardware and Curriculum structure

### Key Entities

- **Hardware Dashboard**: Interactive UI component for selecting and managing hardware profile (Workstation, Edge Kit, Robot) aligned with PDF Page 5 specifications
- **Curriculum Roadmap**: Visual learning path component showing 13-week progression with completion tracking
- **Week Module**: Individual curriculum unit (e.g., Week 10: Humanoid Locomotion) with completion status
- **System Status Indicator**: Chatbot widget element displaying active hardware configuration
- **Auth Guard**: Route protection mechanism that redirects unauthenticated users to login state

## Success Criteria

### Measurable Outcomes

- **SC-001**: Students can configure their hardware profile in under 2 minutes
- **SC-002**: 95% of hardware profile changes are successfully synced with backend on first attempt
- **SC-003**: Students can view and understand their curriculum progress within 30 seconds of accessing /roadmap
- **SC-004**: 90% of students successfully mark at least one week as complete during their first session
- **SC-005**: System status indicator displays correct hardware information in 100% of chatbot sessions
- **SC-006**: Code blocks and markdown render correctly in 100% of chatbot responses
- **SC-007**: Unauthenticated users are blocked from accessing /profile and /roadmap in 100% of attempts
- **SC-008**: 85% of students rate the visual design (dark mode, glassmorphism) as "appealing" or "very appealing"
- **SC-009**: Page load times for /profile and /roadmap are under 2 seconds on standard broadband
- **SC-010**: 80% of returning students have configured their hardware profile within their first 3 sessions
- **SC-011**: 75% of active students mark at least one week as complete per week of platform usage
