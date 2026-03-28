# Data Model: Phase 4-5 Stability Layer

**Created**: 2026-03-18
**Feature**: Performance Monitoring Dashboard + Stability Layer
**Branch**: 001-performance-monitoring

---

## Entity 1: ReindexJob (Existing)

**Purpose**: Track background re-indexing operations from creation to completion.

### Schema

```sql
CREATE TABLE reindex_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(50) NOT NULL DEFAULT 'queued',
    total_files INTEGER NOT NULL,
    processed_files INTEGER NOT NULL DEFAULT 0,
    failed_files INTEGER NOT NULL DEFAULT 0,
    current_file VARCHAR(500),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_reindex_jobs_status ON reindex_jobs(status);
```

### Fields

| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID | No | auto | Unique job identifier |
| status | String(50) | No | 'queued' | Job status: queued, running, completed, cancelled, failed |
| total_files | Integer | No | - | Total number of files to re-index |
| processed_files | Integer | No | 0 | Number of files successfully processed |
| failed_files | Integer | No | 0 | Number of files that failed |
| current_file | String(500) | Yes | NULL | Name of file currently being processed |
| started_at | DateTime | Yes | NULL | When job execution started |
| completed_at | DateTime | Yes | NULL | When job completed (any status) |
| created_at | DateTime | No | NOW() | When job was created |
| created_by_user_id | UUID | No | - | Admin user who triggered re-indexing |

### Status Enum Values

```python
class ReindexStatus(str, Enum):
    QUEUED = "queued"           # Job created, waiting to start
    RUNNING = "running"         # Currently processing files
    COMPLETED = "completed"     # Successfully finished
    CANCELLED = "cancelled"     # Manually cancelled by user
    FAILED = "failed"           # Encountered error
```

### Relationships

- **created_by_user** (User): Many-to-one relationship
  - A user can trigger multiple re-index jobs
  - When user is deleted, all their jobs are cascade-deleted

### Validation Rules

1. `total_files` must be > 0
2. `processed_files` must be >= 0 and <= `total_files`
3. `failed_files` must be >= 0 and <= `total_files`
4. `processed_files + failed_files` must be <= `total_files`
5. `started_at` must be set when status changes to 'running'
6. `completed_at` must be set when status changes to 'completed', 'cancelled', or 'failed'
7. `current_file` must be NULL when status is not 'running'

### State Transitions

```
queued → running → completed
              ↘ cancelled
              ↘ failed
```

**Transition Rules**:
- `queued → running`: Set `started_at`, update `current_file`
- `running → completed`: Set `completed_at`, clear `current_file`
- `running → cancelled`: Set `completed_at`, clear `current_file`
- `running → failed`: Set `completed_at`, clear `current_file`, set `error_message`
- `queued → cancelled`: Set `completed_at` (job never started)

---

## Entity 2: PerformanceMetric (Optional - if persisting)

**Note**: Current implementation uses in-memory PerformanceMonitor singleton. This entity is for future persistence needs.

**Purpose**: Persist performance metrics for historical analysis and dashboards.

### Proposed Schema

```sql
CREATE TABLE performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(10) NOT NULL,
    latency_ms FLOAT NOT NULL,
    step_type VARCHAR(50),  -- embedding, search, context_assembly, llm_call
    status_code INTEGER NOT NULL,
    user_id UUID
);

CREATE INDEX idx_metrics_timestamp ON performance_metrics(timestamp);
CREATE INDEX idx_metrics_endpoint ON performance_metrics(endpoint);
CREATE INDEX idx_metrics_step_type ON performance_metrics(step_type);
```

### Fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | UUID | No | Unique identifier |
| timestamp | DateTime | No | When metric was recorded |
| endpoint | String(500) | No | API endpoint path |
| method | String(10) | No | HTTP method (GET, POST, etc.) |
| latency_ms | Float | No | Request duration in milliseconds |
| step_type | String(50) | Yes | RAG step type (for detailed tracking) |
| status_code | Integer | No | HTTP response status code |
| user_id | UUID | Yes | User ID if authenticated |

### Step Type Enum Values

```python
class RAGStepType(str, Enum):
    EMBEDDING = "embedding"              # Query embedding generation
    SEARCH = "search"                    # Qdrant vector search
    CONTEXT_ASSEMBLY = "context_assembly" # Formatting retrieved documents
    LLM_CALL = "llm_call"                # Grok API response generation
```

---

## Entity 3: IngestionLog (Existing - Referenced)

**Purpose**: Track file ingestion operations (already exists, referenced by ReindexService).

### Key Fields (for reference)

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique log identifier |
| user_id | UUID | Admin who uploaded |
| file_name | String | Original filename |
| file_path | String | Temporary file path |
| file_size | Integer | File size in bytes |
| file_type | String | MIME type |
| status | String | pending, processing, completed, failed |
| chunk_count | Integer | Number of chunks indexed |
| qdrant_point_ids | JSON | List of Qdrant point UUIDs |
| created_at | DateTime | When ingestion started |
| completed_at | DateTime | When ingestion completed |

---

## Data Access Patterns

### ReindexJob Queries

**Get Latest Job**:
```python
def get_latest_reindex_job(db: Session) -> Optional[ReindexJob]:
    return db.query(ReindexJob).order_by(ReindexJob.created_at.desc()).first()
```

**Get Job by ID**:
```python
def get_reindex_job(db: Session, job_id: UUID) -> Optional[ReindexJob]:
    return db.query(ReindexJob).filter(ReindexJob.id == job_id).first()
```

**Get Running Jobs** (prevent concurrent re-indexing):
```python
def get_running_jobs(db: Session) -> List[ReindexJob]:
    return db.query(ReindexJob).filter(ReindexJob.status == "running").all()
```

**Update Progress**:
```python
def update_job_progress(
    db: Session, 
    job: ReindexJob, 
    processed: int, 
    current_file: Optional[str] = None
):
    job.processed_files = processed
    if current_file:
        job.current_file = current_file
    db.commit()
```

**Mark Job Complete**:
```python
def complete_job(db: Session, job: ReindexJob, status: str):
    job.status = status
    job.completed_at = datetime.utcnow()
    job.current_file = None
    db.commit()
```

---

## Migration Requirements

**Check Existing Migrations**:
- Verify ReindexJob model has Alembic migration
- If not created, create migration: `alembic revision --autogenerate -m "Create reindex_jobs table"`

**Data Retention** (future consideration):
- Consider archiving old completed jobs (> 30 days)
- Implement cleanup job or manual retention policy

---

## Relationships Diagram

```
┌─────────────┐         ┌──────────────────┐
│   User      │         │  IngestionLog    │
│             │         │                  │
│  id (PK)    │◄────────┤  user_id (FK)    │
│  email      │         │  id (PK)         │
│  ...        │         │  ...             │
└─────────────┘         └──────────────────┘
       │
       │ created_by_user (FK)
       │
       ▼
┌─────────────┐
│ ReindexJob  │
│             │
│ id (PK)     │
│ status      │
│ total_files │
│ ...         │
└─────────────┘
```

---

## Indexes

**ReindexJob**:
- `idx_reindex_jobs_status`: Fast lookup by status (for finding running jobs)
- Primary key (id): Automatic

**PerformanceMetric** (if created):
- `idx_metrics_timestamp`: Time-range queries
- `idx_metrics_endpoint`: Endpoint-specific metrics
- `idx_metrics_step_type`: RAG step filtering

---

## Notes

1. **ReindexJob model already exists** at `backend/models/reindex_job.py` - verify schema matches this spec
2. **PerformanceMetric is optional** - current implementation uses in-memory singleton
3. **IngestionLog is referenced** but not modified - used by ReindexService to get files to re-index
4. All UUIDs use PostgreSQL's native UUID type (not GUID wrapper)
