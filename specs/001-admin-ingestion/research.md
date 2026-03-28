# Research: Admin Ingestion Dashboard

**Feature**: 001-admin-ingestion  
**Date**: 2026-03-17  
**Purpose**: Resolve technical unknowns and establish implementation patterns

## Technical Decisions

### 1. Admin Role Management

**Decision**: Add `is_admin` boolean column to existing `User` model  
**Rationale**: 
- Simplest approach for binary admin/non-admin distinction
- Aligns with existing User model pattern (email_verified boolean)
- No need for complex RBAC system when only two roles exist
- Database migration is straightforward with Alembic

**Alternatives Considered**:
- Separate roles table with many-to-many relationship: Over-engineered for current scope
- Enum-based role system: Unnecessary complexity when only admin/non-admin needed
- Better-Auth built-in roles: Not yet integrated; custom solution faster

**Implementation Pattern**:
```python
# models/user.py
is_admin = Column(Boolean, default=False, nullable=False, index=True)

# api/admin.py dependency
async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

---

### 2. File Upload Component

**Decision**: Use `react-dropzone` for drag-and-drop file uploads  
**Rationale**:
- Lightweight (13.5KB gzipped)
- No external dependencies beyond React
- Excellent accessibility support
- Widely adopted (2M+ weekly downloads)
- Simple API with extensive customization

**Alternatives Considered**:
- `react-dropzone-uploader`: More features but heavier, less maintained
- Custom HTML5 drag-and-drop: Reinventing the wheel, accessibility challenges
- `uppy`: Feature-rich but overkill for simple use case (100KB+)

**Implementation Pattern**:
```tsx
import { useDropzone } from 'react-dropzone';

function FileUploader({ onFilesSelected, maxFiles = 10, maxSize = 10 * 1024 * 1024 }) {
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'text/markdown': ['.md'],
      'text/plain': ['.txt']
    },
    maxFiles,
    maxSize,
    onDrop: onFilesSelected
  });
  
  // Render dropzone with visual feedback
}
```

---

### 3. Upload Progress Feedback

**Decision**: Use XMLHttpRequest with progress events + React state  
**Rationale**:
- Native browser API with fine-grained progress tracking
- No additional dependencies
- Works seamlessly with FastAPI backend
- Better control than fetch API for upload progress

**Alternatives Considered**:
- `axios` with onUploadProgress: Good but adds dependency (already have axios)
- WebSocket for real-time updates: Over-engineered for file upload
- Server-Sent Events: One-way communication not suitable for upload progress

**Implementation Pattern**:
```tsx
function uploadFile(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('file', file);
    
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percentComplete = (e.loaded / e.total) * 100;
        onProgress(percentComplete);
      }
    });
    
    xhr.addEventListener('load', () => {
      if (xhr.status === 200) resolve(JSON.parse(xhr.responseText));
      else reject(new Error(xhr.statusText));
    });
    
    xhr.addEventListener('error', () => reject(new Error('Upload failed')));
    
    xhr.open('POST', `${API_BASE_URL}/api/admin/ingest/upload`);
    xhr.setRequestHeader('Authorization', `Bearer ${token}`);
    xhr.send(formData);
  });
}
```

---

### 4. Indexed Files Data Source

**Decision**: Query Qdrant Cloud for indexed files metadata  
**Rationale**:
- Single source of truth for RAG knowledge base
- Already integrated in backend (qdrant-client in requirements.txt)
- Provides real-time view of indexed content
- Can extract file name, chunk count, indexing timestamp

**Alternatives Considered**:
- PostgreSQL tracking table: Duplicate storage, sync challenges
- Filesystem scanning: Doesn't reflect actual indexed state
- Hybrid approach: Unnecessary complexity for MVP

**Implementation Pattern**:
```python
# services/ingestion_service.py
from qdrant_client import QdrantClient

class IngestionService:
    def __init__(self, qdrant_client: QdrantClient):
        self.client = qdrant_client
    
    def get_indexed_files(self) -> List[IndexedFile]:
        """Retrieve metadata for all indexed files from Qdrant."""
        collections = self.client.get_collections().collections
        # Extract file metadata from collection points
        # Return list with: file_name, indexed_at, chunk_count, status
```

---

### 5. Re-index Operation

**Decision**: Background task with status polling  
**Rationale**:
- Re-indexing can take minutes for large knowledge bases
- HTTP request would timeout
- FastAPI `BackgroundTasks` perfect for fire-and-forget
- Frontend polls status endpoint every 5 seconds (per SC-003)

**Alternatives Considered**:
- Celery worker: Over-engineered, adds Redis dependency
- WebSocket push notifications: Complex, requires connection management
- Server-Sent Events: Good but less widely supported than polling

**Implementation Pattern**:
```python
# api/admin.py
from fastapi import BackgroundTasks

@router.post("/ingest/reindex")
async def trigger_reindex(background_tasks: BackgroundTasks):
    """Trigger background re-indexing of all files."""
    background_tasks.add_task(ingestion_service.reindex_all)
    return {"status": "started", "message": "Re-indexing initiated"}

@router.get("/ingest/reindex/status")
async def get_reindex_status():
    """Check current re-indexing progress."""
    status = ingestion_service.get_reindex_progress()
    return status  # {progress: 0-100, current_file, total_files, status}
```

---

### 6. Performance Metrics Collection

**Decision**: Middleware-based latency tracking + Grok API health endpoint  
**Rationale**:
- Middleware captures all request latencies automatically
- Grok API health check on-demand (not continuous polling)
- Store recent metrics in memory (last 100 requests)
- Expose via `/api/admin/metrics` endpoint

**Alternatives Considered**:
- Prometheus + Grafana: Over-engineered for admin dashboard
- Database logging: Unnecessary write load for transient metrics
- External APM service: Cost, complexity not justified

**Implementation Pattern**:
```python
# services/performance_monitor.py
from collections import deque
from datetime import datetime
import time

class PerformanceMonitor:
    def __init__(self, max_samples=100):
        self.latencies = deque(maxlen=max_samples)
    
    def record_latency(self, latency_ms: float, endpoint: str):
        self.latencies.append({
            "latency_ms": latency_ms,
            "endpoint": endpoint,
            "timestamp": datetime.utcnow()
        })
    
    def get_metrics(self) -> dict:
        if not self.latencies:
            return {"avg_latency_ms": 0, "p95_latency_ms": 0, "request_count": 0}
        
        latencies = [m["latency_ms"] for m in self.latencies]
        return {
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            "request_count": len(latencies)
        }

# api/admin.py
@router.get("/metrics")
async def get_performance_metrics():
    return performance_monitor.get_metrics()

@router.get("/grok/status")
async def check_grok_health():
    """Ping Grok API to verify connectivity."""
    try:
        await grok_client.health_check()
        return {"status": "healthy", "response_time_ms": response_time}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

### 7. File Storage Strategy

**Decision**: Temporary local storage during processing, then discard  
**Rationale**:
- Files are processed immediately upon upload
- No need to store raw files long-term (content extracted to Qdrant)
- Simpler than S3/cloud storage for MVP
- Cleanup after successful indexing

**Alternatives Considered**:
- AWS S3: Unnecessary for temporary storage
- Database BLOB storage: Poor performance, not needed
- Permanent local storage: Wasted space, no benefit

**Implementation Pattern**:
```python
# services/ingestion_service.py
import tempfile
import os

async def process_upload(self, file: UploadFile) -> ProcessingResult:
    """Process uploaded file and index to Qdrant."""
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Process and index
        chunks = await self.extract_content(tmp_path)
        await self.index_to_qdrant(chunks, metadata={"filename": file.filename})
        return ProcessingResult(success=True, chunks=len(chunks))
    finally:
        # Cleanup
        os.unlink(tmp_path)
```

---

## Best Practices

### Security

1. **Admin Route Protection**: All `/api/admin/*` endpoints require valid JWT with `is_admin=True`
2. **File Validation**: Validate MIME type, file extension, and magic bytes before processing
3. **Size Limits**: Enforce 10MB limit at nginx/Fastapi level + application level
4. **Rate Limiting**: Limit upload requests to prevent DoS (e.g., 10 uploads/minute)
5. **Audit Logging**: Log all admin actions with user ID, timestamp, action type

### Error Handling

1. **Graceful Degradation**: If one file fails in multi-upload, continue with others
2. **User-Friendly Messages**: Translate technical errors to actionable user feedback
3. **Retry Logic**: Automatic retry for transient failures (Qdrant timeout, network issues)
4. **Rollback**: If indexing fails mid-process, clean up partial data

### Performance

1. **Streaming Uploads**: Process file chunks as they arrive (don't wait for full upload)
2. **Parallel Processing**: Index multiple files concurrently (configurable batch size)
3. **Connection Pooling**: Reuse Qdrant connections across requests
4. **Caching**: Cache indexed files list for 30 seconds to reduce Qdrant queries

---

## Integration Patterns

### REST API Design

```
POST   /api/admin/ingest/upload      - Upload single file
POST   /api/admin/ingest/upload-batch - Upload multiple files
GET    /api/admin/ingest/files       - List indexed files
POST   /api/admin/ingest/reindex     - Trigger re-index
GET    /api/admin/ingest/reindex/status - Check re-index progress
DELETE /api/admin/ingest/files/{id}  - Remove indexed file
GET    /api/admin/metrics            - Get performance metrics
GET    /api/admin/grok/status        - Check Grok API health
```

### Frontend State Management

```tsx
// Use React Context for global admin state
const AdminContext = createContext();

function AdminProvider({ children }) {
  const [indexedFiles, setIndexedFiles] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [uploadProgress, setUploadProgress] = useState({});
  
  // Fetch data on mount, poll for updates during operations
  // Provide upload, reindex, delete functions
  
  return (
    <AdminContext.Provider value={{...}}>
      {children}
    </AdminContext.Provider>
  );
}
```

---

## Resolved Clarifications

All technical unknowns from the spec have been resolved through this research phase.
