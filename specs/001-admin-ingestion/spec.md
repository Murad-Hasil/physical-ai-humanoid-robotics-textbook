# Feature Specification: Admin Ingestion Dashboard

**Feature Branch**: `001-admin-ingestion`
**Created**: 2026-03-17
**Status**: Draft
**Input**: User description: "Target: /phase-5-admin-ingestion Goals: 1. **Admin Ingestion Dashboard**: Create a protected `/admin/ingest` page. 2. **File Upload System**: Implement a UI to upload Markdown/PDF files directly to the backend's `/api/ingest` endpoint. 3. **Knowledge Base Management**: - Show a list of 'Currently Indexed Files' from the vector database. - Add a 'Re-index' button to refresh the RAG pipeline as new PDF chapters are added. 4. **Hardware Performance Logs**: - A section to view 'Chat Latency' and 'Grok API Status' to ensure the 13-week curriculum remains accessible. 5. **Security (Admin Only)**: - Restrict these routes so only users with an `admin` flag in the database can access them. Constraints: - Must use the existing Better-Auth role-based access control. - Ingestion UI must handle multiple file uploads simultaneously. - Use the same Neon-Blue/Glassmorphism theme for the Admin panel."

## User Scenarios & Testing

### User Story 1 - Admin File Upload (Priority: P1)

As an administrator, I want to upload multiple Markdown or PDF files through a web interface so that the content can be indexed and made available through the RAG system.

**Why this priority**: This is the core functionality of the ingestion system. Without the ability to upload files, administrators cannot add new content to the knowledge base, making all other features useless.

**Independent Test**: Can be fully tested by logging in as admin, navigating to the upload page, selecting multiple files, and verifying they are successfully uploaded and indexed.

**Acceptance Scenarios**:

1. **Given** an admin user is logged in, **When** they navigate to the admin ingestion page and select multiple PDF/Markdown files, **Then** all files are uploaded successfully and added to the indexing queue
2. **Given** an admin user is uploading files, **When** one file fails validation (wrong format), **Then** the error is shown for that specific file while other valid files continue uploading
3. **Given** an admin user has selected files, **When** they initiate the upload, **Then** they receive clear feedback on upload progress and completion status

---

### User Story 2 - View Indexed Files (Priority: P2)

As an administrator, I want to see a list of all currently indexed files in the knowledge base so that I can track what content is available and manage the RAG pipeline.

**Why this priority**: Visibility into the knowledge base is essential for administrators to understand the current state of the system and make informed decisions about what content needs to be added or refreshed.

**Independent Test**: Can be fully tested by logging in as admin, navigating to the ingestion page, and verifying that a list of indexed files is displayed with relevant metadata.

**Acceptance Scenarios**:

1. **Given** an admin user is on the ingestion page, **When** the page loads, **Then** a list of all indexed files is displayed with file names and indexing status
2. **Given** the knowledge base contains indexed files, **When** an admin views the list, **Then** each file shows when it was last indexed and its current status
3. **Given** no files have been indexed yet, **When** an admin views the page, **Then** a clear message indicates the knowledge base is empty with guidance to upload files

---

### User Story 3 - Re-index Knowledge Base (Priority: P3)

As an administrator, I want to trigger a re-index of the knowledge base so that I can refresh the RAG pipeline when new content is added or existing content is updated.

**Why this priority**: This provides administrators with control over the indexing process, ensuring content freshness without requiring manual backend intervention.

**Independent Test**: Can be fully tested by logging in as admin, clicking the re-index button, and verifying that the system processes the re-index request and updates file statuses.

**Acceptance Scenarios**:

1. **Given** an admin user is on the ingestion page, **When** they click the re-index button, **Then** the system begins re-indexing all files in the knowledge base
2. **Given** a re-index operation is in progress, **When** an admin views the page, **Then** they see the current status and progress of the re-indexing operation
3. **Given** a re-index operation completes, **When** the admin views the page, **Then** all files show updated timestamps and successful indexing status

---

### User Story 4 - Monitor System Performance (Priority: P4)

As an administrator, I want to view chat latency and Grok API status metrics so that I can ensure the 13-week curriculum remains accessible and performant.

**Why this priority**: Performance monitoring is critical for maintaining system reliability, but it's a supporting feature that depends on the core ingestion functionality being in place.

**Independent Test**: Can be fully tested by logging in as admin, viewing the performance section, and verifying that latency metrics and API status are displayed accurately.

**Acceptance Scenarios**:

1. **Given** an admin user is on the ingestion page, **When** they view the performance section, **Then** current chat latency metrics are displayed
2. **Given** the Grok API is operational, **When** an admin views the status, **Then** the API status shows as healthy with relevant connection information
3. **Given** the Grok API experiences issues, **When** an admin views the status, **Then** the system displays appropriate warnings or error states

---

### User Story 5 - Access Control Enforcement (Priority: P5)

As a system owner, I want to ensure that only users with admin privileges can access the ingestion dashboard so that sensitive content management operations are restricted to authorized personnel.

**Why this priority**: Security is fundamental but is treated as P5 because it's an enforcement layer that applies to all other features rather than standalone functionality.

**Independent Test**: Can be fully tested by attempting to access the admin ingestion page with both admin and non-admin user accounts, verifying that access is granted only to admins.

**Acceptance Scenarios**:

1. **Given** a user is logged in with admin privileges, **When** they navigate to `/admin/ingest`, **Then** they are granted access to the ingestion dashboard
2. **Given** a user is logged in without admin privileges, **When** they attempt to navigate to `/admin/ingest`, **Then** they are denied access and redirected to an appropriate page
3. **Given** a user is not logged in, **When** they attempt to access `/admin/ingest`, **Then** they are redirected to the authentication page

---

### Edge Cases

- What happens when a user uploads a file larger than the system's maximum allowed size?
- How does the system handle simultaneous upload requests from multiple admin users?
- What happens when the Grok API is temporarily unavailable during re-indexing?
- How does the system handle corrupted or malformed PDF/Markdown files during upload?
- What occurs if the vector database is unreachable during the indexing process?
- How are partial uploads handled when a user's session expires mid-upload?

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a protected `/admin/ingest` page accessible only to users with admin privileges
- **FR-002**: System MUST allow administrators to upload multiple Markdown and PDF files simultaneously through a web interface
- **FR-003**: System MUST display a list of all currently indexed files in the knowledge base with metadata (file name, indexing status, last indexed timestamp)
- **FR-004**: System MUST provide a re-index button that triggers a refresh of the entire RAG pipeline
- **FR-005**: System MUST display chat latency metrics in a dedicated performance monitoring section
- **FR-006**: System MUST display Grok API connection status and health information
- **FR-007**: System MUST enforce role-based access control using the existing Better-Auth system to restrict access to admin users only
- **FR-008**: System MUST provide real-time feedback during file upload operations (progress indicators, success/error messages)
- **FR-009**: System MUST validate uploaded files are in supported formats (Markdown or PDF) before processing
- **FR-010**: System MUST handle upload errors gracefully, allowing valid files to proceed while reporting errors for invalid files
- **FR-011**: System MUST apply the Neon-Blue/Glassmorphism visual theme consistent with the existing admin panel design
- **FR-012**: System MUST prevent non-admin users from accessing any ingestion-related endpoints or pages

### Clarified Requirements

- **FR-013**: System MUST retain uploaded files indefinitely until manually deleted by an administrator
- **FR-014**: System MUST support uploading files up to 10MB per file

### Key Entities

- **Admin User**: A user with elevated privileges who can access the ingestion dashboard and perform content management operations
- **Knowledge Base**: The collection of all indexed files stored in the vector database that powers the RAG system
- **Indexed File**: A file that has been processed through the ingestion pipeline and is available for retrieval through the RAG system
- **Upload Session**: A single upload operation that may contain multiple files submitted by an administrator
- **Performance Metrics**: System health data including chat latency measurements and Grok API status information
- **Re-index Operation**: A background process that refreshes the entire knowledge base by re-processing all indexed files

## Success Criteria

### Measurable Outcomes

- **SC-001**: Administrators can upload 10 files simultaneously in under 30 seconds (for typical curriculum files under 5MB each)
- **SC-002**: The indexed files list loads and displays within 2 seconds of page load
- **SC-003**: Re-indexing operation can be initiated with a single click and provides status updates at least every 5 seconds
- **SC-004**: Non-admin users are denied access to the ingestion dashboard 100% of the time (zero unauthorized access incidents)
- **SC-005**: Chat latency metrics are displayed and refresh automatically at least every 60 seconds
- **SC-006**: System provides clear visual feedback for all upload operations (success, error, or in-progress states visible within 1 second of action)
- **SC-007**: 95% of administrators can successfully complete a file upload on their first attempt without assistance
