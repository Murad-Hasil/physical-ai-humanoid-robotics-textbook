# Feature Specification: Hardware-Aware Authentication and Personalization

**Feature Branch**: `001-hardware-aware-auth`
**Created**: 2026-03-16
**Status**: Draft
**Input**: User description: "Target: /phase-3-auth-personalization Goals: 1. Strict PDF Hardware Profile: Implement a user profile system that stores the specific hardware mentioned in the PDF (Workstation: RTX 4070 Ti+ 12GB VRAM / Ubuntu 22.04, Edge Kit: Jetson Orin Nano/NX, Sensors: RealSense D435i, Robot: Unitree Go2/G1/Proxy). 2. Better-Auth Integration: Set up email/password and GitHub authentication for students. 3. Hardware-Aware RAG Logic: Modify the /chat endpoint so it retrieves the user's hardware profile and injects it into the Grok API prompt. The AI must tailor its advice based on whether the student is on a Sim Rig or an Edge Kit. 4. Curriculum Milestone Tracking: Create a progress tracker for the Weekly Breakdown (Weeks 1-13) as defined in the PDF. 5. Backend Protection: Secure all API endpoints (chat, ingest, profile) using Better-Auth session/JWT tokens. Constraints: - Database must support hardware-specific JSON fields. - System prompts for Grok must prioritize the Hardware Reality section of the PDF (Page 5). - All code must reside in /backend/auth or /phase-3-auth-personalization."

## User Scenarios & Testing

### User Story 1 - Student Registration and Authentication (Priority: P1)

As a student, I want to create an account and sign in securely so that I can access my personalized learning experience and save my progress.

**Why this priority**: Authentication is the foundational feature that enables all other personalization capabilities. Without user accounts, the system cannot track progress, store hardware profiles, or provide hardware-aware responses.

**Independent Test**: Can be fully tested by registering a new student account, signing in, and verifying access to protected resources. Delivers immediate value by securing student data and enabling session management.

**Acceptance Scenarios**:

1. **Given** a visitor is on the site, **When** they click "Sign Up" and provide valid email/password, **Then** they receive a confirmation and can access their account
2. **Given** a visitor wants to use GitHub, **When** they click "Sign in with GitHub" and authorize, **Then** they are logged in without creating a separate password
3. **Given** a registered student, **When** they enter correct credentials, **Then** they are authenticated and maintain their session across pages
4. **Given** an authenticated student, **When** they click "Sign Out", **Then** their session is terminated and they cannot access protected resources

---

### User Story 2 - Configure Hardware Profile from PDF (Priority: P2)

As a student, I want to save my hardware setup (Workstation with RTX 4070 Ti, Edge Kit with Jetson Orin, sensors, robot) so that I receive guidance tailored to my specific equipment.

**Why this priority**: Hardware-aware responses are the core differentiator of this personalization feature. The PDF defines specific hardware configurations (Page 5 "Hardware Reality"), and students need the ability to specify which setup they're using to receive relevant advice.

**Independent Test**: Can be fully tested by a logged-in student creating, viewing, and updating their hardware profile with PDF-specified hardware options, then verifying the information is saved correctly.

**Acceptance Scenarios**:

1. **Given** a logged-in student, **When** they navigate to their profile and select their hardware type (Sim Rig with RTX 4070 Ti or Edge Kit with Jetson Orin), **Then** the information is saved and displayed on subsequent visits
2. **Given** a student with a saved hardware profile, **When** they update their robot model (e.g., Unitree Go2 to G1), **Then** the changes are reflected immediately
3. **Given** a new student without a hardware profile, **When** they view their profile, **Then** they see predefined options matching the PDF hardware list

---

### User Story 3 - Receive Hardware-Aware Chatbot Responses (Priority: P3)

As a student, I want the chatbot to automatically adjust its technical advice based on my hardware setup (Sim Rig vs Edge Kit) so that I receive instructions that work with my actual equipment.

**Why this priority**: This is the primary value proposition of the personalization system - delivering contextually relevant guidance that respects the "Hardware Reality" constraints from the PDF without requiring students to repeatedly specify their equipment.

**Independent Test**: Can be fully tested by asking the chatbot a technical question (e.g., deployment instructions) and verifying the response includes hardware-specific instructions matching the student's saved profile (Sim Rig vs Edge Kit).

**Acceptance Scenarios**:

1. **Given** a student with a Sim Rig (RTX 4070 Ti) saved in their profile, **When** they ask about running simulations, **Then** the response includes workstation-optimized commands and assumes Ubuntu 22.04 environment
2. **Given** a student with an Edge Kit (Jetson Orin Nano), **When** they ask about deployment, **Then** the advice references resource-constrained edge deployment practices
3. **Given** a student with a Unitree Go2 robot, **When** they ask about robot control, **Then** the response includes Go2-specific configuration
4. **Given** a student without a hardware profile, **When** they ask a technical question, **Then** the chatbot provides generic instructions or prompts them to select their hardware from the PDF list

---

### User Story 4 - Track Weekly Curriculum Progress (Priority: P4)

As a student, I want the system to track my progress through the 13-week curriculum so that I can monitor which weeks I've completed and what remains.

**Why this priority**: Progress tracking provides motivation and helps students understand where they are in their journey through the PDF-defined curriculum structure, but it's dependent on authentication being in place first.

**Independent Test**: Can be fully tested by a student completing a week and verifying their progress is recorded and visible in their profile.

**Acceptance Scenarios**:

1. **Given** a student completes Week 1, **When** they mark it as completed, **Then** their profile shows Week 1 as completed with the completion date
2. **Given** a student with partial progress (e.g., Weeks 1-5 completed), **When** they view their profile, **Then** they see a summary showing completed weeks and remaining weeks
3. **Given** a returning student, **When** they sign in, **Then** their previously completed weeks are still visible
4. **Given** a student near completion, **When** they view progress, **Then** they can see how many weeks remain until curriculum completion

---

### User Story 5 - Access Protected API Endpoints Securely (Priority: P5)

As a student, I want all my interactions with the chatbot and profile management to be secure so that my data and conversations are protected.

**Why this priority**: Security is essential for protecting student data, but it's largely transparent to users once implemented correctly. This story ensures all API endpoints require valid authentication.

**Independent Test**: Can be fully tested by attempting to access protected endpoints without authentication (should fail) and with valid authentication (should succeed).

**Acceptance Scenarios**:

1. **Given** an unauthenticated user, **When** they try to access the chat endpoint, **Then** they receive an authentication error
2. **Given** an authenticated student, **When** they access the chat endpoint, **Then** their requests are processed successfully
3. **Given** an authenticated student, **When** they access their profile endpoint, **Then** they can view and update their own data only
4. **Given** a student with an expired session, **When** they try to access protected endpoints, **Then** they are prompted to log in again

---

### Edge Cases

- What happens when a student tries to access protected endpoints without authentication? (System should reject with appropriate error)
- How does the system handle concurrent sessions from the same student on multiple devices?
- What happens when a student with a saved hardware profile asks questions unrelated to hardware? (Should provide relevant answer without forcing hardware context)
- How does the system handle students who sign in via GitHub but then try to use email/password with the same email?
- What happens when chat history grows very large? (Pagination or archival strategy needed)
- How does the system handle incomplete or outdated hardware profiles? (Should gracefully degrade to generic responses)
- What happens if a student selects hardware they don't actually own? (System trusts student input but may note potential mismatches)
- How does the system handle the "Hardware Reality" constraints from PDF Page 5 when student's profile doesn't match? (Should guide student toward PDF-specified hardware)

## Requirements

### Functional Requirements

- **FR-001**: System MUST allow students to register with email and password
- **FR-002**: System MUST allow students to authenticate via GitHub OAuth
- **FR-003**: System MUST securely store and hash student passwords
- **FR-004**: System MUST maintain student sessions using secure tokens (JWT or session-based)
- **FR-005**: System MUST allow students to create and update their hardware profile with PDF-specified options (Workstation: RTX 4070 Ti+ 12GB VRAM / Ubuntu 22.04, Edge Kit: Jetson Orin Nano/NX, Sensors: RealSense D435i, Robot: Unitree Go2/G1/Proxy)
- **FR-006**: System MUST track and store which curriculum weeks (Weeks 1-13) each student has completed
- **FR-007**: System MUST save and retrieve chat conversation history for authenticated students
- **FR-008**: System MUST require valid authentication tokens for all API endpoints (chat, ingest, profile)
- **FR-009**: System MUST automatically inject student hardware profile context into chatbot responses
- **FR-010**: System MUST provide hardware context metadata to the Grok API for personalized responses that respect the "Hardware Reality" section (PDF Page 5)
- **FR-011**: System MUST allow students to view their curriculum progress summary showing completed and remaining weeks
- **FR-012**: System MUST allow students to view and search their past chat conversations
- **FR-013**: System MUST provide frontend components/hooks for authentication state management in Docusaurus
- **FR-014**: System MUST use secure cookies for session management
- **FR-015**: System MUST log security-relevant events (login attempts, authentication failures)
- **FR-016**: System MUST differentiate between "Sim Rig" and "Edge Kit" hardware types when generating responses
- **FR-017**: System MUST support JSON fields in database for flexible hardware-specific configurations
- **FR-018**: System MUST allow students to select from predefined hardware options matching the PDF specifications

### Key Entities

- **Student**: Represents an authenticated student with credentials (email/password or GitHub OAuth), unique identifier, and account metadata
- **StudentProfile**: Extended student information including curriculum progress, hardware configuration, and preferences linked to a Student
- **HardwareProfile**: Specific hardware details (hardware type: Sim Rig/Edge Kit, GPU model, edge device, sensors, robot model) associated with a StudentProfile, aligned with PDF "Hardware Reality" specifications
- **CurriculumProgress**: Record of completed curriculum weeks (Weeks 1-13) linked to a StudentProfile with completion timestamps
- **ChatSession**: A conversation session between a student and the chatbot, containing metadata (timestamp, duration, hardware context used)
- **ChatMessage**: Individual messages within a ChatSession, including student queries and chatbot responses with timestamps

## Success Criteria

### Measurable Outcomes

- **SC-001**: Students can complete registration and first login in under 3 minutes
- **SC-002**: 95% of authentication attempts succeed on the first try for valid credentials
- **SC-003**: Students can set up their hardware profile from PDF options in under 2 minutes
- **SC-004**: 90% of chatbot responses include relevant hardware-specific guidance when student has a saved profile
- **SC-005**: System maintains student sessions without unexpected logouts for at least 7 days of active use
- **SC-006**: 85% of students successfully locate and view their curriculum progress within their first week
- **SC-007**: Chat history retrieval completes in under 2 seconds for students with up to 100 past conversations
- **SC-008**: Zero security incidents related to authentication bypass or unauthorized data access in first 30 days
- **SC-009**: 80% of returning students have a completed hardware profile within their first 3 sessions
- **SC-010**: Students on Edge Kits receive edge-specific advice in 95% of deployment-related queries
- **SC-011**: Students on Sim Rigs receive workstation-optimized advice in 95% of simulation-related queries
