# Data Model: Admin Ingestion Dashboard

**Feature**: 001-admin-ingestion  
**Date**: 2026-03-17  
**Source**: Derived from spec.md functional requirements

## Entity 1: User (Extended)

**Purpose**: Extend existing User model with admin capability

### Fields
- `id` (GUID, primary key): Unique user identifier
- `email` (String 255, unique, indexed): User email address
- `password_hash` (String 255, nullable): Bcrypt hashed password
- `github_id` (String 100, unique, nullable): GitHub OAuth provider ID
- `email_verified` (Boolean, default false): Whether email is verified
- `is_admin` (Boolean, default false, indexed): **NEW** Admin privilege flag
- `last_login_at` (DateTime, nullable): Most recent login timestamp
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Relationships
- `profile` → StudentProfile (one-to-one, cascade delete)
- `chat_sessions` → ChatSession (one-to-many, cascade delete)

### Validation Rules
- Email must be unique and valid format
- Password required unless GitHub OAuth user
- `is_admin` defaults to false for all new users
- Only existing admins can promote other users (enforced at service layer)

### State Transitions
```
New User → is_admin=false (default)
         → is_admin=true (admin promotion via database migration or admin action)
```

---

## Entity 2: IngestionLog

**Purpose**: Track file upload and indexing operations for audit and monitoring

### Fields
- `id` (GUID, primary key): Unique log identifier
- `user_id` (GUID, foreign key → User.id): Admin who initiated upload
- `file_name` (String 500): Original filename
- `file_path` (String 1000): Temporary storage path during processing
- `file_size` (Integer): File size in bytes
- `file_type` (String 50): MIME type or extension (pdf, markdown)
- `status` (String 50, indexed): Processing status
  - `pending`: Uploaded, waiting processing
  - `processing`: Currently being indexed
  - `completed`: Successfully indexed to Qdrant
  - `failed`: Processing failed (error logged)
- `chunk_count` (Integer, nullable): Number of chunks indexed to Qdrant
- `error_message` (Text, nullable): Error details if failed
- `qdrant_point_ids` (Array of GUID, nullable): IDs of indexed chunks in Qdrant
- `started_at` (DateTime): Processing start timestamp
- `completed_at` (DateTime): Processing end timestamp
- `created_at` (DateTime): Upload timestamp
- `updated_at` (DateTime): Last update timestamp

### Relationships
- `user` → User (many-to-one, required)

### Validation Rules
- File size must not exceed 10MB (10,485,760 bytes)
- File type must be: `application/pdf`, `text/markdown`, `text/plain`
- Status transitions must follow valid paths (see below)
- `chunk_count` required when status = `completed`
- `error_message` required when status = `failed`

### State Transitions
```
pending → processing → completed
                      → failed
```

### Indexes
- `user_id` (for filtering by admin)
- `status` (for finding pending/failed jobs)
- `created_at` (for sorting by upload date)
- Composite: `(user_id, status)` for admin dashboard queries

---

## Entity 3: PerformanceMetric (In-Memory, Not Persisted)

**Purpose**: Track API performance for monitoring dashboard

### Fields
- `timestamp` (DateTime): When request occurred
- `endpoint` (String 200): API endpoint path
- `method` (String 10): HTTP method (GET, POST, etc.)
- `latency_ms` (Float): Request duration in milliseconds
- `status_code` (Integer): HTTP response status code
- `user_id` (GUID, nullable): User who made request (if authenticated)

### Storage Strategy
- In-memory deque (max 1000 samples)
- Automatically evicts oldest entries
- Not persisted to database (transient metrics only)
- Aggregated statistics computed on-demand

### Aggregations (Computed)
- `avg_latency_ms`: Average latency over sample window
- `p95_latency_ms`: 95th percentile latency
- `p99_latency_ms`: 99th percentile latency
- `request_count`: Total requests in sample window
- `error_rate`: Percentage of 4xx/5xx responses

---

## Entity 4: ReindexJob

**Purpose**: Track background re-indexing operations

### Fields
- `id` (GUID, primary key): Unique job identifier
- `status` (String 50, indexed): Job status
  - `queued`: Waiting to start
  - `running`: Currently processing
  - `completed`: All files re-indexed
  - `cancelled`: Manually stopped
  - `failed`: Error occurred
- `total_files` (Integer): Total files to re-index
- `processed_files` (Integer): Files completed so far
- `failed_files` (Integer): Files that failed
- `current_file` (String 500, nullable): Currently processing file name
- `started_at` (DateTime): Job start timestamp
- `completed_at` (DateTime): Job end timestamp
- `created_at` (DateTime): Job creation timestamp
- `created_by_user_id` (GUID, foreign key → User.id): Admin who triggered

### Relationships
- `created_by_user` → User (many-to-one)

### Validation Rules
- Only one reindex job can run at a time (enforced at service layer)
- `processed_files` + `failed_files` ≤ `total_files`
- `completed_at` required when status = `completed` or `failed`

### State Transitions
```
queued → running → completed
               → failed
               → cancelled
```

---

## Validation Rules Summary

### File Upload Validation
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {
    'application/pdf': '.pdf',
    'text/markdown': '.md',
    'text/plain': '.txt'
}
ALLOWED_EXTENSIONS = {'.pdf', '.md', '.txt'}

def validate_file(file: UploadFile) -> ValidationResult:
    # Check size
    file_size = len(await file.read())
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File exceeds 10MB limit: {file_size} bytes")
    
    # Check extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")
    
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Invalid MIME type: {file.content_type}")
    
    # Verify magic bytes for PDF
    if ext == '.pdf':
        magic = await file.read(4)
        if not magic.startswith(b'%PDF'):
            raise ValueError("Invalid PDF file (magic bytes mismatch)")
    
    return ValidationResult(valid=True)
```

### Admin Authorization Validation
```python
async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to verify admin access."""
    if not current_user.is_admin:
        log_security_event(
            "UNAUTHORIZED_ADMIN_ACCESS",
            user_id=str(current_user.id),
            email=current_user.email,
            path=request.url.path
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "forbidden",
                "message": "Admin access required"
            }
        )
    return current_user
```

---

## Database Schema (PostgreSQL)

```sql
-- Extension for GUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Add is_admin to users table
ALTER TABLE users 
ADD COLUMN is_admin BOOLEAN DEFAULT FALSE NOT NULL;
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- Create ingestion_logs table
CREATE TABLE ingestion_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(500) NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    chunk_count INTEGER,
    error_message TEXT,
    qdrant_point_ids UUID[],
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ingestion_logs_user_id ON ingestion_logs(user_id);
CREATE INDEX idx_ingestion_logs_status ON ingestion_logs(status);
CREATE INDEX idx_ingestion_logs_created_at ON ingestion_logs(created_at);
CREATE INDEX idx_ingestion_logs_user_status ON ingestion_logs(user_id, status);

-- Create reindex_jobs table
CREATE TABLE reindex_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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
CREATE INDEX idx_reindex_jobs_created_at ON reindex_jobs(created_at);
```

---

## Qdrant Schema

### Collection: `knowledge_base`

**Purpose**: Store indexed content chunks for RAG retrieval

### Vector Configuration
- Vector size: 384 (sentence-transformers/all-MiniLM-L6-v2)
- Distance: Cosine similarity

### Payload Schema
```json
{
  "file_id": "UUID",
  "file_name": "String",
  "chunk_index": "Integer",
  "content": "String",
  "metadata": {
    "uploaded_by": "UUID",
    "uploaded_at": "ISO8601 timestamp",
    "file_type": "String (pdf|markdown)",
    "file_size": "Integer (bytes)"
  }
}
```

### Indexing Strategy
- Payload index on `file_id` for filtering
- Payload index on `file_name` for display
- No payload index on `content` (full-text search not required)

---

## Relationships Diagram

```
┌─────────────┐
│    User     │
│  (extended) │
└──────┬──────┘
       │
       ├──────────────┐
       │              │
       ▼              ▼
┌──────────────┐  ┌─────────────┐
│IngestionLog  │  │ ReindexJob  │
│  (NEW)       │  │   (NEW)     │
└──────────────┘  └─────────────┘
       │
       │ (logical, not persisted)
       ▼
┌─────────────┐
│   Qdrant    │
│  Collection │
└─────────────┘
```

---

## Migration Strategy

### Phase 1: Add is_admin to Users
```python
# Alembic migration
def upgrade():
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))
    op.create_index('idx_users_is_admin', 'users', ['is_admin'])

def downgrade():
    op.drop_index('idx_users_is_admin', table_name='users')
    op.drop_column('users', 'is_admin')
```

### Phase 2: Create IngestionLog Table
```python
def upgrade():
    op.create_table('ingestion_logs',
        sa.Column('id', GUID(), nullable=False),
        sa.Column('user_id', GUID(), nullable=False),
        sa.Column('file_name', sa.String(length=500), nullable=False),
        sa.Column('file_path', sa.String(length=1000), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('chunk_count', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('qdrant_point_ids', sa.ARRAY(GUID()), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ingestion_logs_user_id', 'ingestion_logs', ['user_id'])
    op.create_index('idx_ingestion_logs_status', 'ingestion_logs', ['status'])
    op.create_index('idx_ingestion_logs_created_at', 'ingestion_logs', ['created_at'])
    op.create_index('idx_ingestion_logs_user_status', 'ingestion_logs', ['user_id', 'status'])
```

### Phase 3: Create ReindexJob Table
```python
def upgrade():
    op.create_table('reindex_jobs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='queued'),
        sa.Column('total_files', sa.Integer(), nullable=False),
        sa.Column('processed_files', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('failed_files', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('current_file', sa.String(length=500), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('created_by_user_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_reindex_jobs_status', 'reindex_jobs', ['status'])
    op.create_index('idx_reindex_jobs_created_at', 'reindex_jobs', ['created_at'])
```
