# Quickstart Guide: Phase 7 Final Intelligence

**Created**: 2026-03-26
**Feature**: 001-phase-7-intelligence
**Purpose**: Get developers up and running with personalization features quickly

---

## Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL database (Neon or local)
- Git

---

## Backend Setup

### 1. Clone and Navigate

```bash
cd /home/brownie/projects/physical-ai-docusaurus-textbook/backend
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create `.env` file:

```bash
# Database
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/physicalai

# Grok API
GROK_API_KEY=your_grok_api_key
GROK_API_URL=https://api.x.ai/v1

# Qdrant Cloud
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key

# JWT
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
```

### 5. Run Database Migrations

```bash
# Generate migration for new models
alembic revision --autogenerate -m "Add Phase 7 curriculum and personalization models"

# Apply migrations
alembic upgrade head
```

### 6. Verify Migration

```bash
# Check tables created
psql $DATABASE_URL -c "\dt"

# Should see:
# - curriculum_weeks
# - chapters
# - chapter_summaries
# - translations
# - student_profiles (with skill_level column)
```

### 7. Run Tests

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/services/test_personalization_service.py
pytest tests/api/test_translations.py

# Run with coverage
pytest --cov=backend --cov-report=html
```

### 8. Start Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs for Swagger UI

---

## Frontend Setup

### 1. Navigate to Docusaurus

```bash
cd /home/brownie/projects/physical-ai-docusaurus-textbook/docusaurus-textbook
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Environment Variables

Create `.env` file:

```bash
# Backend API URL
REACT_APP_API_URL=http://localhost:8000/api/v1

# Optional: Feature flags
REACT_APP_PERSONALIZATION_ENABLED=true
REACT_APP_TRANSLATION_ENABLED=true
```

### 4. Create Context and Components

Create the following files (see `contracts/frontend-components.tsx` for implementations):

```bash
# Context
mkdir -p src/context
touch src/context/PersonalizationContext.tsx

# Components
mkdir -p src/components/onboarding
mkdir -p src/components/personalization
mkdir -p src/components/translation

touch src/components/onboarding/HardwareProfileForm.tsx
touch src/components/onboarding/SkillLevelSelector.tsx
touch src/components/personalization/PersonalizationToggle.tsx
touch src/components/personalization/HardwareIndicator.tsx
touch src/components/translation/TranslationToggle.tsx
touch src/components/translation/TranslationProgress.tsx

# Pages
touch src/pages/signup.tsx
touch src/pages/profile.tsx
```

### 5. Swizzle Docusaurus Theme

```bash
# Swizzle DocItem to add personalization UI
npx docusaurus swizzle @docusaurus/theme-classic DocItem --typescript --eject

# This creates: src/theme/DocItem/index.tsx
# Edit to include TranslationToggle and PersonalizedSummary
```

### 6. Update CSS Theme

Ensure cyber theme utilities exist in:

```bash
# Should already exist from Phase 3
src/css/custom.css
```

Add translation toggle styles if missing:

```css
.translation-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.translation-in-progress {
  animation: pulse-cyan 2s infinite;
  color: #FFD700;
}
```

### 7. Start Development Server

```bash
npm run start
```

Visit: http://localhost:3000

---

## Curriculum Content Ingestion

### Option 1: Batch Ingestion Script

Create `backend/ingestion/ingest_curriculum.py`:

```python
#!/usr/bin/env python3
"""
Batch ingest curriculum content from markdown files.

Usage:
  python -m ingestion.ingest_curriculum --path ./curriculum-content/weeks
"""

import argparse
import asyncio
from pathlib import Path
from ingestion.curriculum_parser import parse_week_folder
from services.curriculum_service import CurriculumService

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help='Path to curriculum content')
    parser.add_argument('--regenerate-summaries', action='store_true')
    args = parser.parse_args()
    
    service = CurriculumService()
    curriculum_path = Path(args.path)
    
    # Parse all weeks
    for week_folder in sorted(curriculum_path.glob('week-*')):
        print(f"Ingesting {week_folder.name}...")
        week_data = parse_week_folder(week_folder)
        await service.ingest_week(week_data)
    
    # Optionally regenerate summaries
    if args.regenerate_summaries:
        print("Regenerating personalized summaries...")
        await service.regenerate_all_summaries()
    
    print("✅ Ingestion complete!")

if __name__ == '__main__':
    asyncio.run(main())
```

Run ingestion:

```bash
cd backend
source venv/bin/activate
python -m ingestion.ingest_curriculum --path ../curriculum-content/weeks --regenerate-summaries
```

### Option 2: API Endpoint

```bash
# Prepare curriculum content JSON
# See contracts/openapi.yaml: CurriculumIngestRequest schema

# POST to ingestion endpoint
curl -X POST http://localhost:8000/api/v1/curriculum/ingest \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d @curriculum-data.json
```

---

## Testing Personalization

### Test 1: User Profile Creation

```bash
# Create test user (via signup or API)
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "skill_level": "intermediate"
  }'

# Get auth token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}' \
  | jq -r '.access_token')
```

### Test 2: Hardware Profile Update

```bash
curl -X PUT http://localhost:8000/api/v1/user-profile/hardware-config \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hardware_type": "sim_rig",
    "gpu_model": "RTX 4070 Ti",
    "gpu_vram_gb": 16
  }'
```

### Test 3: Get Personalized Summary

```bash
# Get chapter summary for current user's profile
curl -X GET "http://localhost:8000/api/v1/chapters/CHAPTER_ID/summary" \
  -H "Authorization: Bearer $TOKEN"

# Override profile (admin)
curl -X GET "http://localhost:8000/api/v1/chapters/CHAPTER_ID/summary?hardware_profile=edge_kit&skill_level=beginner" \
  -H "Authorization: Bearer $TOKEN"
```

### Test 4: Translation

```bash
# Get Roman Urdu translation
curl -X GET "http://localhost:8000/api/v1/chapters/CHAPTER_ID/translation?lang=ur-Latn" \
  -H "Authorization: Bearer $TOKEN"

# Check translation stats
curl -X GET "http://localhost:8000/api/v1/translations/status" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Debugging

### Backend Logs

```bash
# Enable debug logging
export LOG_LEVEL=debug
uvicorn main:app --reload
```

### Database Inspection

```bash
# Connect to PostgreSQL
psql $DATABASE_URL

# Check chapter summaries
SELECT chapter_id, hardware_profile_type, skill_level, generated_at
FROM chapter_summaries
ORDER BY generated_at DESC
LIMIT 10;

# Check translation coverage
SELECT status, COUNT(*) as count
FROM translations
GROUP BY status;
```

### Frontend Debugging

```bash
# React DevTools
# - Check PersonalizationContext value
# - Verify localStorage keys: 'language', 'hardwareProfile', 'skillLevel'

# Browser Console
localStorage.getItem('language')
localStorage.getItem('skillLevel')
```

---

## Common Issues

### Issue 1: Migration Fails

**Error**: `column "skill_level" of relation "student_profiles" already exists`

**Solution**:
```bash
# Check if column exists
psql $DATABASE_URL -c "\d student_profiles"

# If exists but migration not recorded
alembic stamp head
```

### Issue 2: Personalization Not Loading

**Check**:
1. Backend: Is `PersonalizationService` returning summaries?
2. Frontend: Is `PersonalizationContext` provider wrapping app?
3. Browser: Is localStorage populated?

**Debug**:
```typescript
// In browser console
console.log('Context:', usePersonalization());
console.log('LocalStorage:', localStorage);
```

### Issue 3: Translation Toggle Not Working

**Check**:
1. API: Does translation exist for chapter?
2. Component: Is `translationAvailable` prop set correctly?
3. State: Is language toggle updating context?

**Debug**:
```bash
# Check translation in database
psql $DATABASE_URL -c "SELECT chapter_id, status FROM translations WHERE chapter_id='CHAPTER_ID'"
```

---

## Performance Optimization

### Enable Caching (Optional)

Add Redis for hot summaries:

```bash
# Install redis
pip install redis

# Add to .env
REDIS_URL=redis://localhost:6379/0

# Update PersonalizationService to cache summaries
```

### Database Indexes

Ensure indexes exist:

```sql
CREATE INDEX IF NOT EXISTS idx_chapter_summaries_lookup 
ON chapter_summaries(chapter_id, hardware_profile_type, skill_level);

CREATE INDEX IF NOT EXISTS idx_translations_chapter_lang 
ON translations(chapter_id, language_code);
```

---

## Next Steps

After setup:

1. **Run full test suite**: `pytest && npm test`
2. **Verify API contracts**: Visit http://localhost:8000/docs
3. **Test user flows**: Signup → Hardware Profile → View Chapter → Toggle Translation
4. **Ingest sample content**: Use ingestion script with test curriculum
5. **Proceed to implementation**: Follow `/sp.tasks` breakdown

---

## Support

- **API Documentation**: http://localhost:8000/docs
- **OpenAPI Spec**: `specs/001-phase-7-intelligence/contracts/openapi.yaml`
- **Component Contracts**: `specs/001-phase-7-intelligence/contracts/frontend-components.tsx`
- **Data Model**: `specs/001-phase-7-intelligence/data-model.md`
