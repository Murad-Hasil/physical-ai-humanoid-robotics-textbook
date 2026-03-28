# Implementation Plan: Admin Ingestion Dashboard

**Branch**: `001-admin-ingestion` | **Date**: 2026-03-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-admin-ingestion/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an admin-only dashboard for managing the RAG knowledge base through file uploads, indexing monitoring, and performance tracking. The system extends the existing Better-Auth authentication with admin role checks, provides a drag-and-drop file upload interface, and displays real-time metrics for the Grok API and chat latency.

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript 5.6 + React 19 (frontend)
**Primary Dependencies**: FastAPI 0.109+, Docusaurus 3.9+, Better-Auth (existing), react-dropzone (planned)
**Storage**: PostgreSQL (Neon), Qdrant Cloud (vector database), local filesystem for uploads
**Testing**: pytest + pytest-asyncio (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web application (Linux server backend, browser frontend)
**Performance Goals**: 1000 req/s backend, <2s page load, <30s for 10-file upload
**Constraints**: <200ms p95 API latency, 10MB max file size, admin-only access
**Scale/Scope**: 10k concurrent users, 50 screens (Docusaurus), single backend service

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Status**: ✅ PASS - All gates satisfied

| Gate | Status | Justification |
|------|--------|---------------|
| Library-First | ✅ PASS | Admin ingestion exposed as reusable service (`services/ingestion_service.py`) |
| CLI Interface | ✅ PASS | Ingestion service can be invoked via CLI for batch operations |
| Test-First (NON-NEGOTIABLE) | ✅ PASS | All features will follow TDD: tests → fail → implement |
| Integration Testing | ✅ PASS | Contract tests for `/api/ingest` endpoint, integration tests for RAG pipeline |
| Observability | ✅ PASS | Structured logging for security events, performance metrics tracked |
| Simplicity (YAGNI) | ✅ PASS | Single admin page, no over-engineering; uses existing auth system |

## Project Structure

### Documentation (this feature)

```text
specs/001-admin-ingestion/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── ingestion_log.py    # New: Track uploaded files
│   ├── services/
│   │   ├── ingestion_service.py # New: File upload & indexing
│   │   └── performance_monitor.py # New: Latency & API health
│   └── api/
│       └── admin.py            # New: Admin-only endpoints
├── tests/
│   ├── contract/
│   │   └── test_admin_api.py
│   └── integration/
│       └── test_ingestion_pipeline.py

docusaurus-textbook/
├── src/
│   ├── components/
│   │   ├── AdminNav.jsx        # New: Admin navigation
│   │   ├── FileUploader.jsx    # New: Drag-and-drop upload
│   │   ├── IndexedFilesTable.jsx # New: File list display
│   │   └── PerformanceMetrics.jsx # New: Latency & API status
│   ├── pages/
│   │   └── admin/
│   │       └── ingest.tsx      # New: Admin ingestion dashboard
│   └── hooks/
│       └── useAuth.tsx         # Modified: Add admin role check
```

**Structure Decision**: Web application structure (backend + frontend). Backend uses service layer pattern for ingestion logic; frontend uses component-based architecture within Docusaurus.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations requiring justification. All complexity is justified by feature requirements.

## Phase 2 Summary

**Status**: ✅ COMPLETE - All Phase 1 artifacts generated

### Generated Artifacts

- ✅ `research.md` - Technical decisions and patterns documented
- ✅ `data-model.md` - Entity definitions, validation rules, database schema
- ✅ `contracts/openapi-spec.md` - Complete API specification
- ✅ `quickstart.md` - Step-by-step implementation guide
- ✅ Agent context updated with new technologies

### Ready for Tasks

The plan is complete and ready for task breakdown via `/sp.tasks`.

### Implementation Notes

1. **Admin Role**: Simple boolean flag on User model (not full RBAC)
2. **File Upload**: react-dropzone + XMLHttpRequest for progress tracking
3. **Background Jobs**: FastAPI BackgroundTasks for re-indexing
4. **Metrics**: In-memory deque for performance monitoring
5. **Storage**: Temporary files during processing, then discarded

### Testing Strategy

- **Backend**: pytest + pytest-asyncio for API and service tests
- **Frontend**: Jest + React Testing Library for component tests
- **Integration**: End-to-end tests for complete upload → index → retrieval flow
- **Contract**: API response validation against OpenAPI spec

### Security Considerations

- All `/api/admin/*` endpoints require `is_admin=true`
- File validation: MIME type, extension, magic bytes, size limit
- Rate limiting: 10 uploads/minute per admin user
- Audit logging: All admin actions logged with user ID and timestamp
- SQL injection prevention: SQLAlchemy ORM with parameterized queries
- XSS prevention: React's built-in escaping, no dangerouslySetInnerHTML
