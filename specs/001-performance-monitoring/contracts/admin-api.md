# API Contracts: Admin Stability Endpoints

**Created**: 2026-03-18
**Feature**: Phase 4-5 Stability Layer
**Branch**: 001-performance-monitoring
**Base Path**: `/api/admin`

---

## Overview

This document defines the API contracts for admin stability endpoints including re-indexing, performance stats, and health checks.

**Authentication**: All endpoints require admin authentication via JWT token
**Rate Limiting**: Re-indexing endpoint is rate-limited (10 requests/minute per user)

---

## Endpoint 1: POST /api/admin/reindex

**Purpose**: Trigger manual re-indexing of all files in the knowledge base.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body**: Empty (no request body required)

### Response

**Success (200 OK)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "total_files": 150,
  "message": "Re-indexing job created successfully"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| job_id | UUID | Unique identifier for the re-indexing job |
| status | String | Initial status: "queued" |
| total_files | Integer | Number of files to be re-indexed |
| message | String | Human-readable status message |

### Error Responses

**429 Too Many Requests** (Rate Limited):
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many re-index operations. Please try again later.",
  "details": {
    "retry_after_seconds": 60,
    "limit": 10
  }
}
```

**403 Forbidden** (Not Admin):
```json
{
  "error": "forbidden",
  "message": "Admin access required"
}
```

**401 Unauthorized** (Not Authenticated):
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

**500 Internal Server Error**:
```json
{
  "error": "internal_error",
  "message": "Failed to create re-indexing job"
}
```

### Rate Limiting

- **Limit**: 10 requests per minute per admin user
- **Window**: Sliding window (60 seconds)
- **Headers**: Include `Retry-After` header on 429 responses

---

## Endpoint 2: GET /api/admin/reindex/status

**Purpose**: Get status of re-indexing job (latest or by job ID).

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| job_id | UUID | No | - | Specific job ID (returns latest if omitted) |

**Example**:
```
GET /api/admin/reindex/status
GET /api/admin/reindex/status?job_id=550e8400-e29b-41d4-a716-446655440000
```

### Response

**Success (200 OK)** - Job Running:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "progress": {
    "processed_files": 45,
    "total_files": 150,
    "failed_files": 2,
    "percent_complete": 30
  },
  "current_file": "robotics_fundamentals_chapter_3.pdf",
  "timing": {
    "started_at": "2026-03-18T10:30:00Z",
    "elapsed_seconds": 120,
    "estimated_remaining_seconds": 280
  }
}
```

**Success (200 OK)** - Job Completed:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": {
    "processed_files": 150,
    "total_files": 150,
    "failed_files": 0,
    "percent_complete": 100
  },
  "current_file": null,
  "timing": {
    "started_at": "2026-03-18T10:30:00Z",
    "completed_at": "2026-03-18T10:37:30Z",
    "elapsed_seconds": 450,
    "estimated_remaining_seconds": 0
  }
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| job_id | UUID | Unique job identifier |
| status | String | queued, running, completed, cancelled, failed |
| progress | Object | Progress metrics |
| progress.processed_files | Integer | Files successfully processed |
| progress.total_files | Integer | Total files to process |
| progress.failed_files | Integer | Files that failed |
| progress.percent_complete | Integer | Percentage complete (0-100) |
| current_file | String|null | Currently processing file name |
| timing | Object | Timing information |
| timing.started_at | ISO 8601 | When job started |
| timing.completed_at | ISO 8601|null When job completed |
| timing.elapsed_seconds | Integer | Seconds since start |
| timing.estimated_remaining_seconds | Integer | Estimated time remaining |

### Error Responses

**404 Not Found** (Job ID not found):
```json
{
  "error": "not_found",
  "message": "Re-indexing job not found"
}
```

**403 Forbidden** (Not Admin):
```json
{
  "error": "forbidden",
  "message": "Admin access required"
}
```

---

## Endpoint 3: GET /api/admin/stats

**Purpose**: Get performance metrics and usage analytics.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| time_range | String | No | "1h" | Time range: "1h", "24h", "7d", "30d" |

**Example**:
```
GET /api/admin/stats
GET /api/admin/stats?time_range=24h
```

### Response

**Success (200 OK)**:
```json
{
  "rag_latency": {
    "avg_ms": 245.3,
    "p95_ms": 412.7,
    "p99_ms": 589.2,
    "sample_count": 1547,
    "time_range": "1h"
  },
  "llm_latency": {
    "avg_ms": 1823.5,
    "p95_ms": 2456.1,
    "p99_ms": 3102.8,
    "sample_count": 1547,
    "time_range": "1h"
  },
  "usage_analytics": {
    "total_queries": 1547,
    "total_tokens": 2456789,
    "unique_users": 42,
    "time_range": "1h"
  },
  "last_updated": "2026-03-18T11:30:00Z"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| rag_latency | Object | RAG pipeline latency metrics |
| rag_latency.avg_ms | Float | Average latency in milliseconds |
| rag_latency.p95_ms | Float | 95th percentile latency |
| rag_latency.p99_ms | Float | 99th percentile latency |
| rag_latency.sample_count | Integer | Number of samples |
| rag_latency.time_range | String | Time range for metrics |
| llm_latency | Object | LLM (Grok) call latency metrics |
| llm_latency.avg_ms | Float | Average latency in milliseconds |
| llm_latency.p95_ms | Float | 95th percentile latency |
| llm_latency.p99_ms | Float | 99th percentile latency |
| llm_latency.sample_count | Integer | Number of samples |
| usage_analytics | Object | Usage statistics |
| usage_analytics.total_queries | Integer | Total queries answered |
| usage_analytics.total_tokens | Integer | Total tokens used by fastembed |
| usage_analytics.unique_users | Integer | Number of unique users |
| last_updated | ISO 8601 | When metrics were last updated |

### Error Responses

**403 Forbidden** (Not Admin):
```json
{
  "error": "forbidden",
  "message": "Admin access required"
}
```

---

## Endpoint 4: GET /api/admin/health

**Purpose**: Get system health status for all critical services.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**No query parameters or body required.**

### Response

**Success (200 OK)** - All Healthy:
```json
{
  "services": {
    "postgresql": {
      "status": "healthy",
      "response_time_ms": 12,
      "last_checked": "2026-03-18T11:30:00Z"
    },
    "qdrant": {
      "status": "healthy",
      "response_time_ms": 45,
      "last_checked": "2026-03-18T11:30:00Z",
      "collection": "physical-ai-docusaurus-textbook",
      "document_count": 15234
    },
    "grok_api": {
      "status": "healthy",
      "response_time_ms": 234,
      "last_checked": "2026-03-18T11:30:00Z",
      "endpoint": "https://api.x.ai/v1/chat/completions"
    }
  },
  "overall_status": "healthy",
  "timestamp": "2026-03-18T11:30:00Z"
}
```

**Success (200 OK)** - Partial Outage:
```json
{
  "services": {
    "postgresql": {
      "status": "healthy",
      "response_time_ms": 15,
      "last_checked": "2026-03-18T11:30:00Z"
    },
    "qdrant": {
      "status": "unhealthy",
      "error": "Connection timeout after 5000ms",
      "response_time_ms": 5000,
      "last_checked": "2026-03-18T11:30:00Z"
    },
    "grok_api": {
      "status": "healthy",
      "response_time_ms": 245,
      "last_checked": "2026-03-18T11:30:00Z"
    }
  },
  "overall_status": "degraded",
  "timestamp": "2026-03-18T11:30:00Z"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| services | Object | Service health status |
| services.postgresql | Object | PostgreSQL health |
| services.qdrant | Object | Qdrant health |
| services.grok_api | Object | Grok API health |
| services.*.status | String | healthy, unhealthy, degraded |
| services.*.response_time_ms | Integer | Health check response time |
| services.*.error | String | Error message if unhealthy |
| services.*.last_checked | ISO 8601 | When health was checked |
| overall_status | String | healthy, degraded, or unhealthy |
| timestamp | ISO 8601 | Response timestamp |

**Overall Status Logic**:
- `healthy`: All services healthy
- `degraded`: One or more services unhealthy but core functionality available
- `unhealthy`: Critical service (PostgreSQL) unavailable

### Error Responses

**403 Forbidden** (Not Admin):
```json
{
  "error": "forbidden",
  "message": "Admin access required"
}
```

---

## Error Response Format

All error responses follow this standard format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    // Optional additional context
  }
}
```

**Common Error Codes**:
| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| unauthorized | 401 | Missing or invalid authentication |
| forbidden | 403 | Authenticated but not admin |
| not_found | 404 | Resource not found |
| rate_limit_exceeded | 429 | Too many requests |
| internal_error | 500 | Internal server error |

---

## Authentication

All endpoints require JWT authentication:

1. Include `Authorization: Bearer <token>` header
2. Token must be valid and not expired
3. User must have admin role

**Token Acquisition**:
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "secure_password"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Rate Limiting

**Endpoints with Rate Limiting**:
- `POST /api/admin/reindex`: 10 requests/minute per user

**Rate Limit Headers** (included in all responses):
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1679123456
```

**On Rate Limit Exceeded**:
```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/json

{
  "error": "rate_limit_exceeded",
  "message": "Too many re-index operations. Please try again later.",
  "details": {
    "retry_after_seconds": 60,
    "limit": 10
  }
}
```

---

## Versioning

**API Version**: v1 (implicit, no version prefix)
**Breaking Changes**: Will require version bump to v2

---

## Testing

**Test Commands**:
```bash
# Test re-index endpoint
curl -X POST http://localhost:8000/api/admin/reindex \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test status endpoint
curl http://localhost:8000/api/admin/reindex/status \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test stats endpoint
curl "http://localhost:8000/api/admin/stats?time_range=1h" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Test health endpoint
curl http://localhost:8000/api/admin/health \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```
