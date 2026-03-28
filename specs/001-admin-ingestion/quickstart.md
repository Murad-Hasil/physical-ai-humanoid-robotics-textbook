# Quickstart: Admin Ingestion Dashboard

**Feature**: 001-admin-ingestion  
**Date**: 2026-03-17  
**Audience**: Developers implementing the feature

## Prerequisites

- Node.js 20.x (frontend)
- Python 3.12 (backend)
- PostgreSQL database (Neon)
- Qdrant Cloud instance
- Existing authentication system (Better-Auth)

## Setup Steps

### 1. Install Dependencies

**Backend**:
```bash
cd backend
pip install react-dropzone  # Not needed - frontend only
pip install python-multipart  # For file uploads
```

**Frontend**:
```bash
cd docusaurus-textbook
npm install react-dropzone
```

### 2. Database Migrations

Run Alembic migrations to add admin columns and tables:

```bash
cd backend
alembic revision -m "Add admin ingestion tables"
```

Apply the migration:
```bash
alembic upgrade head
```

Verify tables created:
```bash
psql $DATABASE_URL -c "\dt ingestion_logs"
psql $DATABASE_URL -c "\dt reindex_jobs"
psql $DATABASE_URL -c "SELECT is_admin FROM users LIMIT 1;"
```

### 3. Promote First Admin

Manually set `is_admin = true` for the first admin user:

```bash
psql $DATABASE_URL -c "UPDATE users SET is_admin = true WHERE email = 'your-admin-email@example.com';"
```

### 4. Backend Implementation

#### 4.1 Create Models

Create `backend/models/ingestion_log.py`:
```python
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from db.session import Base
from models.base import GUID

class IngestionLog(Base):
    __tablename__ = "ingestion_logs"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="pending", index=True)
    chunk_count = Column(Integer, nullable=True)
    error_message = Column(String, nullable=True)
    qdrant_point_ids = Column(ARRAY(GUID), nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="ingestion_logs")
```

Update `backend/models/user.py` to add relationship:
```python
# Add to User model
ingestion_logs = relationship(
    "IngestionLog",
    back_populates="user",
    cascade="all, delete-orphan"
)
```

Create `backend/models/reindex_job.py`:
```python
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.session import Base
from models.base import GUID

class ReindexJob(Base):
    __tablename__ = "reindex_jobs"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    status = Column(String(50), nullable=False, default="queued", index=True)
    total_files = Column(Integer, nullable=False)
    processed_files = Column(Integer, nullable=False, default=0)
    failed_files = Column(Integer, nullable=False, default=0)
    current_file = Column(String(500), nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by_user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    created_by_user = relationship("User")
```

#### 4.2 Create Services

Create `backend/services/ingestion_service.py`:
```python
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
import tempfile
import os

class IngestionService:
    def __init__(self, db: Session, qdrant_client: QdrantClient):
        self.db = db
        self.qdrant = qdrant_client
    
    async def process_upload(self, file: UploadFile, user_id: str) -> IngestionLog:
        # Validate file
        await self._validate_file(file)
        
        # Create ingestion log
        log = IngestionLog(
            user_id=user_id,
            file_name=file.filename,
            file_path="",
            file_size=0,
            file_type=file.content_type,
            status="processing"
        )
        self.db.add(log)
        self.db.commit()
        
        # Process in background
        # ... implementation
        
        return log
```

Create `backend/services/performance_monitor.py`:
```python
from collections import deque
from datetime import datetime

class PerformanceMonitor:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.latencies = deque(maxlen=1000)
        return cls._instance
    
    def record_latency(self, endpoint: str, latency_ms: float, status_code: int):
        self.latencies.append({
            "endpoint": endpoint,
            "latency_ms": latency_ms,
            "status_code": status_code,
            "timestamp": datetime.utcnow()
        })
    
    def get_metrics(self) -> dict:
        # Calculate avg, p95, p99
        # ... implementation
```

#### 4.3 Create API Routes

Create `backend/api/admin.py`:
```python
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from auth.dependencies import get_current_admin_user
from models.user import User
from services.ingestion_service import IngestionService
from services.performance_monitor import PerformanceMonitor

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/ingest/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Upload single file for indexing."""
    service = IngestionService(db, get_qdrant_client())
    return await service.process_upload(file, current_user.id)

@router.get("/ingest/files")
async def list_indexed_files(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """List all indexed files."""
    # ... implementation

@router.post("/ingest/reindex")
async def trigger_reindex(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Trigger background re-indexing."""
    # ... implementation

@router.get("/metrics")
async def get_metrics(current_user: User = Depends(get_current_admin_user)):
    """Get performance metrics."""
    monitor = PerformanceMonitor()
    return monitor.get_metrics()

@router.get("/grok/status")
async def check_grok_status(current_user: User = Depends(get_current_admin_user)):
    """Check Grok API health."""
    # ... implementation
```

Update `backend/main.py` to include admin router:
```python
from api.admin import router as admin_router

app.include_router(admin_router)
```

#### 4.4 Add Admin Dependency

Create `backend/auth/dependencies.py`:
```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from models.user import User
from auth.jwt_handler import get_current_user  # Existing

async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Verify user has admin privileges."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "forbidden", "message": "Admin access required"}
        )
    return current_user
```

### 5. Frontend Implementation

#### 5.1 Update Auth Hook

Update `docusaurus-textbook/src/hooks/useAuth.tsx`:
```typescript
interface User {
  id: string;
  email: string;
  email_verified: boolean;
  is_admin: boolean;  // Add this field
}
```

#### 5.2 Create Admin Guard Component

Create `docusaurus-textbook/src/components/AdminGuard.jsx`:
```jsx
import React from 'react';
import { useAuth } from '@site/src/hooks/useAuth';
import { Navigate } from '@docusaurus/router';

export default function AdminGuard({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (!user.is_admin) {
    return <Navigate to="/" />;
  }

  return children;
}
```

#### 5.3 Create File Upload Component

Create `docusaurus-textbook/src/components/FileUploader.jsx`:
```jsx
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useAuth } from '@site/src/hooks/useAuth';

export default function FileUploader({ onUploadComplete }) {
  const { user } = useAuth();
  const [progress, setProgress] = useState({});

  const onDrop = useCallback(async (acceptedFiles, rejectedFiles) => {
    // Handle upload with progress tracking
    // ... implementation
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'text/markdown': ['.md'],
    },
    maxFiles: 10,
    maxSize: 10 * 1024 * 1024,
    onDrop
  });

  return (
    <div {...getRootProps()} className="dropzone">
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop files here...</p>
      ) : (
        <p>Drag & drop PDF or Markdown files here (max 10 files, 10MB each)</p>
      )}
    </div>
  );
}
```

#### 5.4 Create Admin Ingestion Page

Create `docusaurus-textbook/src/pages/admin/ingest.tsx`:
```tsx
import React from 'react';
import Layout from '@theme/Layout';
import AdminGuard from '@site/src/components/AdminGuard';
import FileUploader from '@site/src/components/FileUploader';
import IndexedFilesTable from '@site/src/components/IndexedFilesTable';
import PerformanceMetrics from '@site/src/components/PerformanceMetrics';

export default function AdminIngestPage() {
  return (
    <Layout title="Admin - Knowledge Base" description="Manage RAG knowledge base">
      <AdminGuard>
        <div className="container margin-vert--lg">
          <h1>Admin Ingestion Dashboard</h1>
          
          <section>
            <h2>Upload Files</h2>
            <FileUploader onUploadComplete={() => {}} />
          </section>
          
          <section>
            <h2>Indexed Files</h2>
            <IndexedFilesTable />
          </section>
          
          <section>
            <h2>Performance</h2>
            <PerformanceMetrics />
          </section>
        </div>
      </AdminGuard>
    </Layout>
  );
}
```

### 6. Test the Implementation

#### Backend Tests:
```bash
cd backend
pytest tests/contract/test_admin_api.py -v
pytest tests/integration/test_ingestion_pipeline.py -v
```

#### Frontend Tests:
```bash
cd docusaurus-textbook
npm test -- AdminIngestPage.test.tsx
```

### 7. Run Locally

**Backend**:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend**:
```bash
cd docusaurus-textbook
npm start
```

Navigate to `http://localhost:3000/admin/ingest` (must be logged in as admin).

## Next Steps

- Implement TDD tests before each feature
- Add comprehensive error handling
- Set up monitoring and alerting
- Document API in Swagger UI (`/docs`)
- Create admin user management interface

## Troubleshooting

**Issue**: 403 Forbidden on admin endpoints  
**Solution**: Verify `is_admin = true` in database for your user

**Issue**: File upload fails with 413  
**Solution**: Check file size is under 10MB limit

**Issue**: React-dropzone not working  
**Solution**: Verify npm install completed, check browser console for errors

**Issue**: Qdrant connection fails  
**Solution**: Verify QDRANT_URL and QDRANT_API_KEY in backend/.env
