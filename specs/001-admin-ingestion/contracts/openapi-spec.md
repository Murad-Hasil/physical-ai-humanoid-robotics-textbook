# API Contracts: Admin Ingestion Dashboard

**Feature**: 001-admin-ingestion  
**Date**: 2026-03-17  
**Version**: 1.0.0

## Overview

All admin endpoints require authentication and admin privileges. Requests without valid admin credentials receive `403 Forbidden`.

### Base URL
```
http://localhost:8000/api/admin
```

### Authentication
All endpoints require Bearer token in Authorization header:
```
Authorization: Bearer <access_token>
```

### Common Response Codes
- `200 OK`: Successful request
- `201 Created`: Resource created (upload successful)
- `202 Accepted`: Request accepted for processing (background job)
- `400 Bad Request`: Invalid request (validation failed)
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: User not admin
- `404 Not Found`: Resource not found
- `413 Payload Too Large`: File exceeds 10MB limit
- `415 Unsupported Media Type`: Invalid file type
- `500 Internal Server Error`: Server error

---

## Endpoints

### 1. Upload Single File

**Endpoint**: `POST /ingest/upload`

**Purpose**: Upload and index a single PDF or Markdown file

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body** (multipart/form-data):
```
file: <binary> (PDF or Markdown file, max 10MB)
```

**Success Response** (`201 Created`):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "file_name": "chapter-1.pdf",
  "file_size": 2048576,
  "file_type": "application/pdf",
  "status": "processing",
  "created_at": "2026-03-17T10:30:00Z",
  "message": "File uploaded successfully, processing started"
}
```

**Error Response** (`400 Bad Request`):
```json
{
  "error": "validation_error",
  "message": "File type not allowed. Only PDF and Markdown files are accepted.",
  "details": {
    "provided_type": "image/png",
    "allowed_types": ["application/pdf", "text/markdown", "text/plain"]
  }
}
```

**Error Response** (`413 Payload Too Large`):
```json
{
  "error": "file_too_large",
  "message": "File size exceeds 10MB limit",
  "details": {
    "file_size": 15728640,
    "max_size": 10485760
  }
}
```

---

### 2. Upload Multiple Files

**Endpoint**: `POST /ingest/upload-batch`

**Purpose**: Upload and index multiple files simultaneously

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body** (multipart/form-data):
```
files: <binary[]> (Array of PDF or Markdown files, max 10 files, each max 10MB)
```

**Success Response** (`201 Created`):
```json
{
  "batch_id": "batch-550e8400-e29b-41d4-a716-446655440000",
  "total_files": 5,
  "accepted_files": 5,
  "rejected_files": 0,
  "uploads": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "file_name": "chapter-1.pdf",
      "status": "processing"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "file_name": "chapter-2.pdf",
      "status": "processing"
    }
  ],
  "message": "Batch upload accepted, processing started"
}
```

**Partial Success Response** (`207 Multi-Status`):
```json
{
  "batch_id": "batch-550e8400-e29b-41d4-a716-446655440000",
  "total_files": 5,
  "accepted_files": 3,
  "rejected_files": 2,
  "uploads": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "file_name": "chapter-1.pdf",
      "status": "processing"
    },
    {
      "file_name": "invalid-image.png",
      "status": "rejected",
      "error": "Unsupported file type"
    }
  ],
  "message": "Batch upload partially accepted"
}
```

---

### 3. List Indexed Files

**Endpoint**: `GET /ingest/files`

**Purpose**: Retrieve list of all indexed files with metadata

**Request Headers**:
```
Authorization: Bearer <token>
```

**Query Parameters** (optional):
```
?limit=50&offset=0&status=completed&sort=created_at&order=desc
```

**Success Response** (`200 OK`):
```json
{
  "total": 127,
  "limit": 50,
  "offset": 0,
  "files": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "file_name": "chapter-1.pdf",
      "file_size": 2048576,
      "file_type": "application/pdf",
      "status": "completed",
      "chunk_count": 45,
      "uploaded_by": {
        "id": "user-123",
        "email": "admin@example.com"
      },
      "uploaded_at": "2026-03-15T14:30:00Z",
      "indexed_at": "2026-03-15T14:30:15Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "file_name": "chapter-2.pdf",
      "file_size": 1536000,
      "file_type": "application/pdf",
      "status": "completed",
      "chunk_count": 38,
      "uploaded_by": {
        "id": "user-123",
        "email": "admin@example.com"
      },
      "uploaded_at": "2026-03-15T14:35:00Z",
      "indexed_at": "2026-03-15T14:35:12Z"
    }
  ]
}
```

**Empty Response** (`200 OK`):
```json
{
  "total": 0,
  "limit": 50,
  "offset": 0,
  "files": [],
  "message": "No files indexed yet. Upload files to get started."
}
```

---

### 4. Delete Indexed File

**Endpoint**: `DELETE /ingest/files/{file_id}`

**Purpose**: Remove an indexed file from the knowledge base

**Request Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
```
file_id: UUID (the ingestion log ID)
```

**Success Response** (`200 OK`):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "file_name": "chapter-1.pdf",
  "status": "deleted",
  "message": "File and associated chunks removed from knowledge base"
}
```

**Error Response** (`404 Not Found`):
```json
{
  "error": "not_found",
  "message": "File not found",
  "details": {
    "file_id": "550e8400-e29b-41d4-a716-446655440001"
  }
}
```

---

### 5. Trigger Re-index

**Endpoint**: `POST /ingest/reindex`

**Purpose**: Trigger background re-indexing of all files

**Request Headers**:
```
Authorization: Bearer <token>
```

**Request Body**: None

**Success Response** (`202 Accepted`):
```json
{
  "job_id": "job-550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Re-indexing job queued. Check status at /api/admin/ingest/reindex/status"
}
```

**Error Response** (`409 Conflict`):
```json
{
  "error": "conflict",
  "message": "Re-indexing already in progress",
  "details": {
    "current_job_id": "job-550e8400-e29b-41d4-a716-446655440000",
    "status": "running",
    "progress": 45
  }
}
```

---

### 6. Get Re-index Status

**Endpoint**: `GET /ingest/reindex/status`

**Purpose**: Check current re-indexing job progress

**Request Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (`200 OK`):
```json
{
  "job_id": "job-550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "total_files": 127,
  "processed_files": 57,
  "failed_files": 0,
  "current_file": "chapter-15.pdf",
  "progress_percent": 45,
  "started_at": "2026-03-17T10:30:00Z",
  "estimated_completion": "2026-03-17T10:35:00Z"
}
```

**No Active Job** (`200 OK`):
```json
{
  "status": "idle",
  "message": "No active re-indexing job",
  "last_job": {
    "job_id": "job-550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "total_files": 120,
    "processed_files": 120,
    "failed_files": 0,
    "completed_at": "2026-03-16T15:45:00Z"
  }
}
```

---

### 7. Get Performance Metrics

**Endpoint**: `GET /metrics`

**Purpose**: Retrieve chat latency and API performance metrics

**Request Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (`200 OK`):
```json
{
  "chat_latency": {
    "avg_latency_ms": 245.7,
    "p95_latency_ms": 389.2,
    "p99_latency_ms": 512.8,
    "request_count": 847,
    "sample_window_minutes": 60
  },
  "api_latency": {
    "avg_latency_ms": 87.3,
    "p95_latency_ms": 142.1,
    "p99_latency_ms": 198.5,
    "request_count": 1523,
    "sample_window_minutes": 60
  },
  "last_updated": "2026-03-17T10:30:00Z"
}
```

---

### 8. Check Grok API Status

**Endpoint**: `GET /grok/status`

**Purpose**: Verify Grok API connectivity and health

**Request Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (`200 OK`):
```json
{
  "status": "healthy",
  "response_time_ms": 127,
  "endpoint": "https://api.x.ai/v1/chat/completions",
  "last_checked": "2026-03-17T10:30:00Z",
  "details": {
    "api_version": "v1",
    "rate_limit_remaining": 4850,
    "rate_limit_reset": "2026-03-17T11:00:00Z"
  }
}
```

**Error Response** (`200 OK` with unhealthy status):
```json
{
  "status": "unhealthy",
  "error": "Connection timeout",
  "response_time_ms": 5000,
  "endpoint": "https://api.x.ai/v1/chat/completions",
  "last_checked": "2026-03-17T10:30:00Z",
  "details": {
    "error_type": "timeout",
    "retry_after_seconds": 60
  }
}
```

---

## Error Response Format

All error responses follow a consistent structure:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "Additional context"
  }
}
```

### Common Error Codes

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `unauthorized` | 401 | Missing or invalid authentication token |
| `forbidden` | 403 | User lacks admin privileges |
| `validation_error` | 400 | Request validation failed |
| `file_too_large` | 413 | File exceeds 10MB limit |
| `unsupported_media_type` | 415 | Invalid file format |
| `not_found` | 404 | Resource not found |
| `conflict` | 409 | Resource conflict (e.g., job already running) |
| `internal_error` | 500 | Unexpected server error |

---

## Rate Limiting

All admin endpoints are subject to rate limiting:

- **Upload endpoints**: 10 requests per minute per admin user
- **Other endpoints**: 60 requests per minute per admin user

**Rate Limit Headers**:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1647518400
```

**Rate Limit Exceeded** (`429 Too Many Requests`):
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many upload requests. Please try again later.",
  "details": {
    "retry_after_seconds": 45
  }
}
```

---

## Pagination

List endpoints support pagination with consistent parameters:

**Request**:
```
GET /ingest/files?limit=50&offset=0
```

**Response**:
```json
{
  "total": 127,
  "limit": 50,
  "offset": 0,
  "has_more": true,
  "files": [...]
}
```

**Pagination Parameters**:
- `limit`: Number of items per page (default: 50, max: 100)
- `offset`: Starting position (default: 0)

---

## Versioning

API version is included in the response headers:
```
X-API-Version: 1.0.0
```

Breaking changes will increment the major version. All v1.x.x endpoints maintain backward compatibility.
