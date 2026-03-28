# Feature Specification: Qdrant Re-indexing and Consistency Check

**Feature Branch**: `001-qdrant-reindex`
**Created**: 2026-03-18
**Status**: Draft
**Input**: User description: "Target: /phase-4-reindex-sync Goals: 1. **Manual Re-indexing**: Create a backend service to clear and re-populate the Qdrant collection from existing files in `ingestion_logs`. 2. **Consistency Check**: Implement a logic that compares the number of files in PostgreSQL with the number of document IDs in Qdrant. 3. **Atomic Updates**: Ensure that during re-indexing, the old knowledge base remains searchable until the new one is ready (Blue-Green sync). Constraints: - Re-indexing must be triggered only by an Admin. - Progress must be reported to the frontend via status updates (e.g., "Processing file 3 of 10")."

## User Scenarios & Testing

### User Story 1 - Admin Initiates Manual Re-indexing (Priority: P1)

As an Admin user, I want to trigger a complete re-indexing of the Qdrant collection from existing files in the ingestion system, so that I can rebuild the knowledge base when it becomes corrupted or outdated.

**Why this priority**: This is the core functionality that enables all other re-indexing capabilities. Without the ability to manually trigger re-indexing, admins cannot recover from data corruption or sync issues.

**Independent Test**: Admin can initiate a re-indexing operation through the system interface, and the system begins processing files from the ingestion logs.

**Acceptance Scenarios**:

1. **Given** the admin is authenticated with admin privileges, **When** they initiate a re-indexing operation, **Then** the system validates permissions and begins the re-indexing process
2. **Given** a re-indexing operation is in progress, **When** the admin checks the status, **Then** they see real-time progress updates (e.g., "Processing file 3 of 10")
3. **Given** the re-indexing completes successfully, **When** the operation finishes, **Then** all documents from ingestion logs are available in the Qdrant collection

---

### User Story 2 - System Performs Consistency Check (Priority: P2)

As an Admin, I want the system to automatically verify that the number of files in PostgreSQL matches the number of document IDs in Qdrant, so that I can detect and address synchronization issues.

**Why this priority**: Consistency checking provides critical visibility into data integrity issues. It can be deployed independently as a monitoring/diagnostic tool even without the full re-indexing capability.

**Independent Test**: System can compare file counts between PostgreSQL and Qdrant and report whether they match or identify discrepancies.

**Acceptance Scenarios**:

1. **Given** files exist in both PostgreSQL and Qdrant, **When** a consistency check is performed, **Then** the system compares counts and reports match/mismatch status
2. **Given** a mismatch is detected, **When** the check completes, **Then** the system reports the specific discrepancy (e.g., "PostgreSQL: 150 files, Qdrant: 145 documents")
3. **Given** no files exist in either system, **When** a consistency check is performed, **Then** the system reports both counts as zero and indicates consistency

---

### User Story 3 - Blue-Green Re-indexing with Zero Downtime (Priority: P3)

As an Admin, I want the re-indexing process to maintain the existing knowledge base availability until the new index is fully ready, so that users can continue searching without interruption.

**Why this priority**: This ensures production stability during re-indexing operations. While valuable, it's an enhancement over basic re-indexing (P1) and can be added as an improvement to the core functionality.

**Independent Test**: During a re-indexing operation, existing search functionality remains operational and returns results from the current index until the new index is completely built and switched.

**Acceptance Scenarios**:

1. **Given** an active re-indexing operation is in progress, **When** a user performs a search, **Then** the search returns results from the existing index without interruption
2. **Given** the new index is fully built, **When** the system switches to the new index, **Then** the transition is atomic and immediate with no search downtime
3. **Given** a re-indexing operation fails midway, **When** the failure occurs, **Then** the existing index remains intact and searchable

---

### Edge Cases

- What happens when re-indexing is initiated while another re-indexing operation is already in progress?
- How does the system handle files in PostgreSQL that are corrupted or unreadable during re-indexing?
- What happens if Qdrant becomes unavailable during the middle of a re-indexing operation?
- How does the system handle extremely large ingestion logs (e.g., 10,000+ files) during re-indexing?
- What happens when the consistency check detects a mismatch - is automatic remediation attempted or only reported?

## Requirements

### Functional Requirements

- **FR-001**: System MUST restrict re-indexing operations to Admin users only
- **FR-002**: System MUST provide real-time progress updates during re-indexing (e.g., "Processing file 3 of 10")
- **FR-003**: System MUST compare the count of files in PostgreSQL with document IDs in Qdrant and report consistency status
- **FR-004**: System MUST maintain search availability on the existing index while building a new index (Blue-Green approach)
- **FR-005**: System MUST atomically switch from the old index to the new index once re-indexing is complete
- **FR-006**: System MUST prevent concurrent re-indexing operations from running simultaneously
- **FR-007**: System MUST handle failures gracefully, preserving the existing index if new index creation fails
- **FR-008**: System MUST read all files from the ingestion_logs source during re-indexing
- **FR-009**: System MUST clear the target Qdrant collection before populating it with new documents (for manual re-indexing)
- **FR-010**: System MUST log all re-indexing operations with timestamps and outcomes for audit purposes

### Key Entities

- **Re-indexing Operation**: A complete process of clearing and re-populating the Qdrant collection from ingestion log files, with progress tracking and status reporting
- **Consistency Check**: A verification process that compares file counts between PostgreSQL and Qdrant to detect synchronization issues
- **Index**: The searchable knowledge base in Qdrant containing vector embeddings of documents from ingestion logs
- **Admin User**: A user with elevated privileges authorized to trigger administrative operations like re-indexing
- **Progress Status**: Real-time information about the current state of a re-indexing operation (files processed, total files, current status)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Admin users can successfully initiate a re-indexing operation and observe progress updates in real-time
- **SC-002**: Consistency checks complete within 5 seconds and accurately report match/mismatch status between PostgreSQL and Qdrant counts
- **SC-003**: Search operations remain available with 100% uptime during Blue-Green re-indexing (zero downtime during index build)
- **SC-004**: Re-indexing operations process files at a rate of at least 10 files per second under normal load conditions
- **SC-005**: System correctly prevents non-admin users from initiating re-indexing operations 100% of the time
- **SC-006**: Atomic index switching completes in under 1 second with no search query failures during transition
- **SC-007**: Failed re-indexing operations leave the existing index intact and searchable in 100% of failure scenarios
