# Implementation Plan: Phase 7 Final Intelligence

**Branch**: `001-phase-7-intelligence` | **Date**: 2026-03-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-7-intelligence/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement adaptive content personalization and multi-language support for the Physical AI curriculum. The system will collect user hardware profiles (RTX/Jetson/Unitree) and skill levels during onboarding, then dynamically rewrite chapter summaries using the existing Grok/RAG pipeline. Roman Urdu translation toggle will be added for accessibility. All 13 weeks of curriculum content will be ingested and organized for personalized delivery.

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript 5.6 + React 19 (frontend)
**Primary Dependencies**: FastAPI 0.109+, Docusaurus 3.9+, SQLAlchemy 2.0+, Better-Auth (existing), Grok API, Qdrant Cloud
**Storage**: PostgreSQL (Neon) for user data and curriculum content, Qdrant Cloud for vector embeddings, local filesystem for uploads
**Testing**: pytest (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web application (Linux server backend, browser frontend)
**Project Type**: Full-stack web application with existing backend (FastAPI) and frontend (Docusaurus)
**Performance Goals**: Personalized summaries load within 2 seconds (p90), support 1,000 concurrent users, translation toggle responds within 500ms
**Constraints**: Backend logic must use existing Grok/RAG pipeline, UI must maintain "Robotic SaaS" glassmorphism theme, data persistence uses existing PostgreSQL `users` and `student_profiles` tables
**Scale/Scope**: 13-week curriculum with multiple chapters per week, ~100-200 total content items for personalization, hardware profiles for 3 device categories (Sim Rig, Edge Kit, Unitree robots)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Status**: Constitution file exists but contains only template placeholders. No active principles to validate against.

**Gates**:
- [ ] Test-First: Not enforced (constitution template not filled)
- [ ] CLI Interface: Not applicable (web application)
- [ ] Library-First: Not applicable (feature-specific implementation)
- [ ] Integration Testing: Required for API contracts and personalization services
- [ ] Observability: Structured logging required for personalization and translation services

**Note**: Constitution should be updated with project-specific principles. For now, proceeding with standard best practices for FastAPI + React applications.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-7-intelligence/
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
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── user_profiles.py    # User profile and hardware config endpoints
│   │   │   ├── personalization.py  # Content personalization endpoints
│   │   │   └── translations.py     # Translation service endpoints
│   │   └── deps.py                 # Dependencies (auth, user context)
│   └── deps.py
├── services/
│   ├── personalization_service.py  # Hardware-aware content rewriting
│   ├── translation_service.py      # Roman Urdu translation
│   └── curriculum_service.py       # 13-week content management
├── models/
│   ├── user.py                     # Existing User model (extend with skill_level)
│   ├── student_profile.py          # Existing StudentProfile + HardwareConfig
│   └── curriculum.py               # New models for curriculum content
├── schemas/
│   ├── user_profile.py             # Pydantic schemas for profile requests
│   ├── personalization.py          # Schemas for personalization requests
│   └── translation.py              # Schemas for translation requests
├── llm/
│   ├── prompts/
│   │   ├── personalization.py      # Prompt templates for hardware-aware rewriting
│   │   └── translation.py          # Prompt templates for Roman Urdu translation
│   └── grok_client.py              # Existing Grok API client (reuse)
└── tests/
    ├── api/
    │   ├── test_user_profiles.py
    │   ├── test_personalization.py
    │   └── test_translations.py
    └── services/
        ├── test_personalization_service.py
        ├── test_translation_service.py
        └── test_curriculum_service.py

docusaurus-textbook/
├── src/
│   ├── components/
│   │   ├── onboarding/
│   │   │   ├── HardwareProfileForm.tsx    # Hardware + skill level collection
│   │   │   └── SkillLevelSelector.tsx
│   │   ├── personalization/
│   │   │   ├── PersonalizationToggle.tsx  # Enable/disable personalization
│   │   │   └── HardwareIndicator.tsx      # Show current hardware profile
│   │   └── translation/
│   │       ├── TranslationToggle.tsx      # English ↔ Roman Urdu toggle
│   │       └── TranslationProgress.tsx    # "AI Translation in progress" indicator
│   └── pages/
│       ├── signup.tsx                     # Enhanced signup with hardware profile
│       └── profile.tsx                    # Profile page with hardware editing
└── docs/
    ├── week-01/
    │   ├── _category_.json
    │   ├── 01-introduction.md
    │   └── ...
    ├── week-02/
    └── ... (weeks 1-13)
```

**Structure Decision**: Using existing backend/frontend separation. Backend follows FastAPI layered architecture (api → services → models). Frontend uses Docusaurus with custom React components for personalization and translation UI.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New services layer (personalization, translation) | Core feature requires dynamic content rewriting based on user context | Direct API calls would scatter logic; services provide testable, reusable abstraction |
| LLM prompt engineering for personalization | Hardware-aware content adaptation requires contextual understanding | Rule-based templates would be too rigid and not scale across 13 weeks of content |
| Separate translation service | Roman Urdu translation is distinct from personalization with different prompts and caching needs | Combining would create monolithic service violating single responsibility |

---

## Phase 0: Research & Discovery

### Unknowns from Technical Context

1. **User Model Extension**: How to add `skill_level` to existing User model without breaking Better-Auth integration
2. **Grok API Prompt Patterns**: Best practices for hardware-aware content rewriting with consistent output format
3. **Roman Urdu Translation**: Approach for technical content translation (preserve code/terms while translating prose)
4. **Curriculum Content Structure**: How to organize 13 weeks of markdown files for efficient personalization
5. **Frontend State Management**: How to manage translation toggle state across Docusaurus pages
6. **Caching Strategy**: Whether to cache personalized summaries or generate on-demand

### Research Tasks

**Task 1**: Research user model extension patterns with Better-Auth
- Investigate existing `StudentProfile` and `HardwareConfig` models
- Determine if `skill_level` belongs on `User` or `StudentProfile`
- Document migration strategy for existing users

**Task 2**: Research Grok API prompt engineering for content personalization
- Review existing `llm/grok_client.py` implementation
- Design prompt templates that accept hardware profile + skill level as context
- Ensure output format preserves markdown structure

**Task 3**: Research Roman Urdu translation patterns for technical content
- Identify technical terms that should remain in English (code, APIs, frameworks)
- Design translation prompts that preserve code blocks and technical terminology
- Plan for partial translation coverage ("AI Translation in progress" indicator)

**Task 4**: Research curriculum content ingestion patterns
- Review existing `ingestion/` directory for PDF processing patterns
- Design folder structure for 13 weeks of markdown content
- Plan batch ingestion script for initial content population

**Task 5**: Research Docusaurus theme customization for translation toggle
- Investigate Docusaurus theme components (DocItem, DocPage)
- Design component wrapper for translation toggle placement
- Plan state persistence (localStorage vs user preference API)

---

## Phase 1: Design & Contracts

### Data Model Design

**Entities from Spec**:

1. **User** (existing, extend):
   - Add `skill_level` field: `beginner`, `intermediate`, `advanced`
   - Migration: ALTER TABLE users ADD COLUMN skill_level VARCHAR(20) DEFAULT 'beginner'

2. **StudentProfile** (existing):
   - Already has relationship to `HardwareConfig`
   - No changes needed

3. **HardwareConfig** (existing):
   - Already supports `sim_rig`, `edge_kit` types
   - Already has GPU model, VRAM, JetPack version fields
   - No changes needed

4. **CurriculumWeek** (new):
   - Fields: `week_number` (1-13), `title`, `description`, `order`
   - Relationship: has many `Chapter`

5. **Chapter** (new):
   - Fields: `title`, `content`, `week_id`, `order`
   - Relationships: belongs to `CurriculumWeek`, has many `ChapterSummary`

6. **ChapterSummary** (new):
   - Fields: `chapter_id`, `hardware_profile_type`, `skill_level`, `summary_content`
   - Unique constraint: (chapter_id, hardware_profile_type, skill_level)
   - Relationship: belongs to `Chapter`

7. **Translation** (new):
   - Fields: `chapter_id`, `language_code` (e.g., "ur-Latn"), `translated_content`, `status` (draft, published)
   - Unique constraint: (chapter_id, language_code)
   - Relationship: belongs to `Chapter`

See `data-model.md` for complete schema definitions.

### API Contracts

**Endpoint Design** (RESTful):

1. **User Profiles**:
   - `POST /api/v1/user-profile/skill-level` - Set skill level
   - `GET /api/v1/user-profile` - Get complete profile with hardware config
   - `PUT /api/v1/user-profile/hardware-config` - Update hardware configuration

2. **Personalization**:
   - `GET /api/v1/chapters/{id}/summary?hardware_profile={type}&skill_level={level}` - Get personalized summary
   - `POST /api/v1/personalization/regenerate` - Regenerate all summaries for user (admin)

3. **Translations**:
   - `GET /api/v1/chapters/{id}/translation?lang=ur-Latn` - Get Roman Urdu translation
   - `PUT /api/v1/chapters/{id}/translation` - Update translation (admin)
   - `GET /api/v1/translations/status` - Get translation coverage stats

4. **Curriculum**:
   - `GET /api/v1/curriculum/weeks` - List all weeks
   - `GET /api/v1/curriculum/weeks/{week_number}` - Get week with chapters
   - `POST /api/v1/curriculum/ingest` - Batch ingest curriculum content (admin)

See `contracts/openapi.yaml` for complete OpenAPI 3.0 specification.

### Frontend Component Contracts

**React Components**:

1. **HardwareProfileForm**:
   - Props: `onSubmit`, `initialValues` (optional)
   - Emits: `profileSaved` event with hardware config

2. **SkillLevelSelector**:
   - Props: `value`, `onChange`, `disabled`
   - Emits: `change` event with skill level

3. **TranslationToggle**:
   - Props: `chapterId`, `currentLang`, `onToggle`
   - Emits: `languageChanged` event with new language code

4. **PersonalizationToggle**:
   - Props: `enabled`, `onToggle`
   - Emits: `personalizationToggled` event

See `contracts/frontend-components.tsx` for TypeScript interface definitions.

### Quickstart Guide

**Backend Setup**:
```bash
cd backend
source venv/bin/activate
alembic upgrade head  # Run migrations
pytest  # Run tests
uvicorn main:app --reload  # Start dev server
```

**Frontend Setup**:
```bash
cd docusaurus-textbook
npm install
npm run start  # Start dev server
```

**Content Ingestion**:
```bash
cd backend
python -m ingestion.ingest_curriculum --path ./curriculum-content/weeks
```

See `quickstart.md` for detailed setup instructions.

---

## Phase 2: Implementation Planning

**Note**: Phase 2 tasks will be created by `/sp.tasks` command.

### Implementation Phases

**Phase 2.1 - Data Collection (Goal 3)**:
- Extend User model with `skill_level` field
- Create API endpoints for profile updates
- Build HardwareProfileForm component for signup flow
- Build Profile page for hardware config editing

**Phase 2.2 - Intelligence Hooks (Goal 1 & 2)**:
- Implement PersonalizationService with Grok API integration
- Implement TranslationService for Roman Urdu
- Design prompt templates for hardware-aware rewriting
- Create caching layer for generated summaries

**Phase 2.3 - Frontend Integration**:
- Wrap Docusaurus DocItem with personalization components
- Add TranslationToggle to chapter pages
- Implement state management for language preference
- Add HardwareIndicator to show current profile

**Phase 2.4 - Content Strategy (Goal 4)**:
- Create curriculum folder structure (weeks 1-13)
- Build batch ingestion script for markdown files
- Implement curriculum service for content retrieval
- Add progress tracking integration

---

## Constitution Check (Post-Design)

*Re-evaluate after Phase 1 design complete*

**Gates**:
- [ ] Test-First: All new services will have test files created before implementation
- [ ] Integration Testing: API contract tests required for personalization and translation endpoints
- [ ] Observability: Structured logging added to all services (personalization, translation, curriculum)

**Status**: Design aligns with constitution principles. Proceeding to `/sp.tasks`.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
