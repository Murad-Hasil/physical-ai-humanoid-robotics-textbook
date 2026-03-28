# Quickstart: Phase 4-5 Stability Layer

**Created**: 2026-03-18
**Feature**: Performance Monitoring Dashboard + Stability Layer
**Branch**: 001-performance-monitoring

---

## Overview

This guide helps developers quickly set up and test the stability layer features including re-indexing, performance monitoring, and health checks.

---

## Prerequisites

- Python 3.12
- PostgreSQL database (or SQLite for development)
- Qdrant Cloud or local Qdrant instance
- Backend dependencies installed

---

## 1. Setup Database

### Option A: Using PostgreSQL (Recommended)

```bash
# Create database
createdb physical_ai_db

# Create user (if not exists)
createuser physical_ai_user

# Set password
psql -c "ALTER USER physical_ai_user WITH PASSWORD 'your_secure_password';"

# Update .env file
cd backend
echo "DATABASE_URL=postgresql://physical_ai_user:your_secure_password@localhost:5432/physical_ai_db" >> .env

# Run migrations
alembic upgrade head
```

### Option B: Using SQLite (Development Only)

```bash
cd backend
# SQLite is default if DATABASE_URL not set
# Tables will be created automatically on startup
```

---

## 2. Configure Environment

Update `backend/.env` with required settings:

```env
# Database
DATABASE_URL=postgresql://physical_ai_user:your_secure_password@localhost:5432/physical_ai_db

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key  # If using Qdrant Cloud

# Grok API
GROK_API_KEY=gsk_your_api_key_here
GROK_MODEL=grok-beta

# Authentication
JWT_SECRET=your_jwt_secret_change_in_production
JWT_EXPIRY_HOURS=24

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 4. Start Backend Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server should start at: `http://localhost:8000`

---

## 5. Verify Setup

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.2.0",
  "timestamp": "2026-03-18T11:30:00Z"
}
```

### API Documentation

Open in browser: `http://localhost:8000/docs`

---

## 6. Create Admin User (for testing)

```bash
cd backend
python -c "
from db.session import SessionLocal
from models.user import User
from passlib.hash import bcrypt

db = SessionLocal()

# Check if admin exists
admin = db.query(User).filter(User.email == 'admin@example.com').first()
if not admin:
    admin = User(
        email='admin@example.com',
        hashed_password=bcrypt.hash('admin_password'),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    print('Admin user created')
else:
    print('Admin user already exists')

db.close()
"
```

---

## 7. Get Admin Token

```bash
# Login to get JWT token
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin_password"}')

# Extract token (using jq)
ADMIN_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

# Or manually copy from response
echo "Token: $ADMIN_TOKEN"
```

---

## 8. Test Endpoints

### Test Health Endpoint

```bash
curl http://localhost:8000/api/admin/health \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq
```

Expected response shows status of PostgreSQL, Qdrant, and Grok API.

### Test Stats Endpoint

```bash
curl "http://localhost:8000/api/admin/stats?time_range=1h" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq
```

Expected response shows latency metrics and usage analytics.

### Test Re-index Endpoint

```bash
# Trigger re-indexing
curl -X POST http://localhost:8000/api/admin/reindex \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" | jq

# Check status
curl http://localhost:8000/api/admin/reindex/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq
```

Expected response shows job_id and status.

---

## 9. Run Tests

### Unit Tests

```bash
cd backend
pytest tests/unit/test_reindex_service.py -v
pytest tests/unit/test_performance_monitor.py -v
```

### Integration Tests

```bash
cd backend
pytest tests/integration/test_admin_endpoints.py -v
pytest tests/integration/test_reindex_flow.py -v
```

### All Tests

```bash
cd backend
pytest tests/ -v --cov=services --cov=api
```

---

## 10. Common Issues

### Issue: Database connection error

**Symptom**: `could not connect to server`

**Solution**:
```bash
# Check PostgreSQL is running
pg_isready

# Restart PostgreSQL (Linux)
sudo systemctl restart postgresql

# Verify DATABASE_URL in .env
cat backend/.env | grep DATABASE_URL
```

### Issue: Qdrant connection error

**Symptom**: `Connection refused` or `Connection timeout`

**Solution**:
```bash
# Check Qdrant is running
curl http://localhost:6333/cluster

# Or check Qdrant Cloud URL and API key
cat backend/.env | grep QDRANT
```

### Issue: JWT token expired

**Symptom**: `401 Unauthorized`

**Solution**:
```bash
# Get new token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin_password"}'
```

### Issue: Rate limit exceeded

**Symptom**: `429 Too Many Requests`

**Solution**:
```bash
# Wait 60 seconds before retrying
# Or increase rate limit in middleware/rate_limiter.py
```

### Issue: Tables don't exist

**Symptom**: `relation "reindex_jobs" does not exist`

**Solution**:
```bash
cd backend
alembic upgrade head
```

---

## 11. Development Workflow

### Making Changes

1. Create feature branch from `001-performance-monitoring`
2. Make changes to services or API
3. Write tests
4. Run tests
5. Commit and push

### Testing Re-indexing

```bash
# 1. Upload some test files first
curl -X POST http://localhost:8000/api/admin/ingest/upload \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -F "file=@test_document.pdf"

# 2. Trigger re-indexing
curl -X POST http://localhost:8000/api/admin/reindex \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# 3. Monitor progress
watch -n 2 'curl -s http://localhost:8000/api/admin/reindex/status \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq'
```

### Monitoring Performance

```bash
# Watch metrics in real-time
watch -n 5 'curl -s http://localhost:8000/api/admin/stats \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .rag_latency'
```

---

## 12. Next Steps

After setup:

1. **Read API Contracts**: See `contracts/admin-api.md` for detailed endpoint specs
2. **Review Data Model**: See `data-model.md` for entity relationships
3. **Start Implementation**: Run `/sp.tasks` to get implementation tasks
4. **Frontend Setup**: See Docusaurus frontend documentation for UI development

---

## 13. Useful Commands

```bash
# View logs
tail -f backend/logs/app.log

# Check database
psql physical_ai_db -c "SELECT * FROM reindex_jobs ORDER BY created_at DESC LIMIT 5;"

# Clear all metrics
curl -X DELETE http://localhost:8000/api/admin/metrics/clear \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Check running jobs
psql physical_ai_db -c "SELECT * FROM reindex_jobs WHERE status = 'running';"
```

---

## Support

For issues or questions:
- Check existing issues in repository
- Review specification: `spec.md`
- Review research: `research.md`
- Contact development team
