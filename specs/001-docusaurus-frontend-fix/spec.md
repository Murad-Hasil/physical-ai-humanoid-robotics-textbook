# Feature Specification: Docusaurus Frontend Fix

**Feature Branch**: `001-docusaurus-frontend-fix`
**Created**: 2026-03-17
**Status**: Draft
**Input**: User description: "Target: /docusaurus-frontend-fix Goals: 1. **Physical Page Creation**: Formally define the creation of src/pages/login.jsx, src/pages/signup.jsx, src/pages/profile.jsx (Hardware Dashboard), and src/pages/roadmap.jsx (13-Week Curriculum). 2. **Navigation Integration**: Explicitly require the modification of docusaurus.config.js to include Navbar links for all new pages. 3. **Global Chatbot Injection**: Specify the mounting of the ChatWidget in a global layout/theme wrapper (Root.jsx) to ensure 100% visibility. 4. **Hardware-UI Sync**: UI components must fetch and display data from the Phase 3 PostgreSQL backend (Hardware Profile & Auth). 5. **Aesthetic Consistency**: Apply Dark-theme Glassmorphism (Neon Blue/Blur) to all newly specified pages. Constraints: - All new routes must be accessible via the Navbar. - The 13-week curriculum must strictly map to the PDF Page 4 structure. - Redirection logic must be explicitly defined for protected routes (/profile and /roadmap)."

## User Scenarios & Testing

### User Story 1 - Student Login (Priority: P1)

As a registered student, I want to log in to the platform so I can access my personalized hardware dashboard and curriculum roadmap.

**Why this priority**: Authentication is the foundation for all personalized features. Without login, users cannot access protected resources.

**Independent Test**: Can be fully tested by navigating to /login, entering valid credentials, and verifying successful authentication and redirection to the dashboard.

**Acceptance Scenarios**:

1. **Given** I am on the login page, **When** I enter valid email and password, **Then** I am authenticated and redirected to the hardware dashboard
2. **Given** I am on the login page, **When** I enter invalid credentials, **Then** I see an error message and remain on the login page
3. **Given** I am not logged in, **When** I try to access /profile, **Then** I am redirected to the login page

---

### User Story 2 - Student Registration (Priority: P2)

As a new student, I want to create an account so I can access the platform's features.

**Why this priority**: Registration enables new users to join the platform, but it's secondary to login for existing users.

**Independent Test**: Can be fully tested by navigating to /signup, filling the registration form, and verifying account creation.

**Acceptance Scenarios**:

1. **Given** I am on the signup page, **When** I enter valid registration details, **Then** my account is created and I am logged in automatically
2. **Given** I am on the signup page, **When** I enter an email that already exists, **Then** I see an error message indicating the email is already registered
3. **Given** I have just registered, **When** I complete signup, **Then** I am redirected to the hardware dashboard

---

### User Story 3 - Hardware Dashboard Access (Priority: P1)

As a logged-in student, I want to view my hardware profile dashboard so I can see my assigned hardware (GPU, Jetson Kit, or Unitree Robot) and track my progress.

**Why this priority**: This is the core feature that provides personalized hardware context for the curriculum.

**Independent Test**: Can be fully tested by logging in, navigating to /profile, and verifying hardware profile information is displayed correctly.

**Acceptance Scenarios**:

1. **Given** I am logged in with an RTX GPU profile, **When** I navigate to /profile, **Then** I see my GPU model (e.g., RTX 4070 Ti) and related specifications
2. **Given** I am logged in with a Jetson Kit profile, **When** I navigate to /profile, **Then** I see my Jetson model (e.g., Jetson Orin Nano) and related specifications
3. **Given** I am logged in with a Unitree Robot profile, **When** I navigate to /profile, **Then** I see my robot model and related specifications
4. **Given** I am not logged in, **When** I try to access /profile, **Then** I am redirected to the login page

---

### User Story 4 - 13-Week Curriculum Roadmap (Priority: P1)

As a logged-in student, I want to view my 13-week curriculum roadmap so I can track my progress through the program.

**Why this priority**: The roadmap is essential for students to understand their learning journey and track progress.

**Independent Test**: Can be fully tested by logging in, navigating to /roadmap, and verifying the 13-week curriculum structure is displayed with progress tracking.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I navigate to /roadmap, **Then** I see a visual 13-week curriculum tracker
2. **Given** I am on the roadmap page, **When** I view week details, **Then** I see the curriculum structure matching the PDF Page 4 content
3. **Given** I have completed some weeks, **When** I view the roadmap, **Then** I see my progress visually indicated (completed vs. remaining weeks)
4. **Given** I am not logged in, **When** I try to access /roadmap, **Then** I am redirected to the login page

---

### User Story 5 - Global Chatbot Access (Priority: P2)

As any user (logged in or not), I want to access the AI chatbot from any page so I can get help while reading the textbook.

**Why this priority**: The chatbot enhances the learning experience but is not core to authentication or curriculum tracking.

**Independent Test**: Can be fully tested by navigating to any page and verifying the chatbot widget is visible and functional in the bottom-right corner.

**Acceptance Scenarios**:

1. **Given** I am on any page of the textbook, **When** I look at the bottom-right corner, **Then** I see the chatbot widget
2. **Given** the chatbot is visible, **When** I click on it, **Then** the chat interface expands for interaction
3. **Given** I am using the chatbot, **When** I navigate to a different page, **Then** the chatbot remains accessible

---

### User Story 6 - Navigation Access (Priority: P3)

As any user, I want to easily navigate between key pages (Hardware Dashboard, Roadmap, Login) via the navbar so I can access features quickly.

**Why this priority**: Navigation is important for usability but depends on the pages being created first.

**Independent Test**: Can be fully tested by verifying navbar links are present and functional across all pages.

**Acceptance Scenarios**:

1. **Given** I am on any page, **When** I look at the navbar, **Then** I see "Hardware Dashboard" link in the left position
2. **Given** I am on any page, **When** I look at the navbar, **Then** I see "13-Week Roadmap" link in the left position
3. **Given** I am on any page, **When** I look at the navbar, **Then** I see "Login" link in the right position
4. **Given** I click on any navbar link, **When** the navigation occurs, **Then** I am taken to the correct page

---

### Edge Cases

- What happens when a user tries to access /profile or /roadmap without being authenticated? (Should redirect to /login)
- How does the system handle session expiration while on a protected page? (Should redirect to login)
- What happens when hardware profile data is not available for a logged-in user? (Should show appropriate message or default state)
- How does the chatbot behave on mobile/responsive views? (Should remain accessible but adapt to screen size)
- What happens when the backend authentication service is unavailable? (Should show graceful error message)

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a login page at /login with email and password input fields
- **FR-002**: System MUST provide a signup page at /signup for new student registration
- **FR-003**: System MUST provide a hardware dashboard page at /profile displaying user's hardware profile
- **FR-004**: System MUST provide a curriculum roadmap page at /roadmap showing 13-week progress tracker
- **FR-005**: System MUST display navigation links in the navbar for all new pages (Hardware Dashboard, 13-Week Roadmap on left; Login on right)
- **FR-006**: System MUST display the chatbot widget on every page of the textbook
- **FR-007**: System MUST redirect unauthenticated users to /login when accessing /profile or /roadmap
- **FR-008**: System MUST authenticate users against the Better-Auth backend service
- **FR-009**: System MUST fetch and display hardware profile data (RTX GPUs, Jetson Kits, Unitree Robots) from the PostgreSQL backend
- **FR-010**: System MUST apply consistent dark-theme glassmorphism styling (neon blue/blur effects) to all new pages
- **FR-011**: System MUST display the 13-week curriculum structure according to the PDF Page 4 specification
- **FR-012**: System MUST wrap all pages with AuthProvider and HardwareProvider context providers
- **FR-013**: System MUST visually indicate completed vs. remaining weeks in the roadmap

### Key Entities

- **User**: A student registered in the system with authentication credentials (email, password) and associated hardware profile
- **Hardware Profile**: User's assigned hardware configuration (RTX GPU, Jetson Kit, or Unitree Robot) with specific model details
- **Curriculum Week**: One of 13 weeks in the program, containing learning objectives and progress status
- **Authentication Session**: User's logged-in state managed by Better-Auth backend

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can complete login in under 30 seconds from entering credentials to reaching the dashboard
- **SC-002**: Users can complete registration in under 2 minutes from entering details to reaching the dashboard
- **SC-003**: 100% of pages display the chatbot widget in the bottom-right corner within 2 seconds of page load
- **SC-004**: All navbar links are functional and navigate to correct pages with 100% success rate
- **SC-005**: Protected routes (/profile, /roadmap) redirect unauthenticated users to /login 100% of the time
- **SC-006**: Hardware dashboard correctly displays user's hardware profile information for 100% of hardware types (RTX, Jetson, Unitree)
- **SC-007**: 13-week roadmap displays all weeks with correct curriculum structure matching PDF specification
- **SC-008**: All new pages render with consistent glassmorphism styling (dark theme, neon blue accents, blur effects)
