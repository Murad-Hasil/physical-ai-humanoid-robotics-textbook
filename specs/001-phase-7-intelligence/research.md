# Research & Discovery: Phase 7 Final Intelligence

**Created**: 2026-03-26
**Feature**: 001-phase-7-intelligence
**Purpose**: Resolve all unknowns from Technical Context before Phase 1 design

---

## Research Task 1: User Model Extension with Better-Auth

**Question**: How to add `skill_level` to existing User model without breaking Better-Auth integration?

**Decision**: Add `skill_level` to the `StudentProfile` model, not the `User` model.

**Rationale**:
- Existing architecture already separates authentication (`User`) from profile data (`StudentProfile`)
- `StudentProfile` has one-to-one relationship with `User` via `user_id` foreign key
- Better-Auth manages the `User` table for authentication; extending `StudentProfile` avoids migration conflicts
- `StudentProfile` already contains user-facing fields (display_name, avatar_url, bio, timezone)
- Skill level is user-facing profile data, not authentication data

**Migration Strategy**:
```sql
-- No changes to User table needed
-- Skill level can be added as column to StudentProfile or kept in existing JSON field
ALTER TABLE student_profiles ADD COLUMN skill_level VARCHAR(20) DEFAULT 'beginner';
-- OR use existing JSON field if flexibility needed
-- ALTER TABLE student_profiles ADD COLUMN extended_profile JSONB DEFAULT '{}';
```

**Alternatives Considered**:
- Add to `User` model: Rejected due to Better-Auth integration complexity
- Create new `UserProfileExtension` table: Over-engineering when `StudentProfile` exists
- Use JSON field in `User` model: Loses type safety and queryability

**Implementation**:
- Add `skill_level` column to `StudentProfile` model in `backend/models/student_profile.py`
- Update Pydantic schemas to include `skill_level` in profile requests/responses
- Create Alembic migration for database schema change
- Default value: `'beginner'` for existing users

---

## Research Task 2: Grok API Prompt Engineering for Personalization

**Question**: Best practices for hardware-aware content rewriting with consistent output format?

**Decision**: Use structured prompt templates with explicit output format markers and context injection.

**Prompt Template Structure**:
```python
PERSONALIZATION_PROMPT = """
You are a technical education assistant specializing in Physical AI curriculum.

CONTEXT:
- User Hardware: {hardware_type} ({gpu_model}, {vram_gb}GB VRAM)
- User Skill Level: {skill_level}
- Original Chapter Summary: {original_summary}

TASK:
Rewrite the chapter summary to be personalized for this user's setup.

GUIDELINES:
1. For Sim Rig (RTX 4070 Ti+): Emphasize desktop GPU optimizations, CUDA cores, high-memory workflows
2. For Edge Kit (Jetson Orin): Focus on power efficiency, TensorRT optimization, memory constraints
3. For Unitree Robots: Highlight real-time processing, sensor integration, embedded deployment

4. For Beginner: Use simple language, explain acronyms, focus on foundational concepts
5. For Intermediate: Include technical details, assume basic knowledge
6. For Advanced: Deep optimization strategies, production considerations, edge cases

OUTPUT FORMAT:
- Preserve all markdown formatting (headers, lists, code blocks)
- Keep technical terms and API names in English
- Output ONLY the rewritten summary, no preamble

PERSONALIZED SUMMARY:
"""
```

**Rationale**:
- Explicit context injection ensures Grok understands user's situation
- Numbered guidelines provide clear transformation rules
- Output format preservation critical for Docusaurus rendering
- Structured approach ensures consistency across 13 weeks of content

**Alternatives Considered**:
- Fine-tune model on personalized content: Overkill, less flexible
- Rule-based template substitution: Too rigid, can't handle nuanced technical content
- Multiple specialized prompts per hardware type: Maintenance burden, single prompt with context is cleaner

**Implementation**:
- Create `backend/llm/prompts/personalization.py` with prompt templates
- Reuse existing `grok_client.py` for API calls
- Add response validation to ensure markdown structure preserved
- Implement retry logic for malformed responses

---

## Research Task 3: Roman Urdu Translation for Technical Content

**Question**: Approach for technical content translation (preserve code/terms while translating prose)?

**Decision**: Use translation prompts with explicit preservation rules and technical term glossary.

**Translation Prompt Structure**:
```python
TRANSLATION_PROMPT = """
You are a technical translator specializing in AI/robotics education.

TASK:
Translate the following technical content from English to Roman Urdu.

PRESERVATION RULES (CRITICAL):
1. DO NOT translate: Code blocks, function names, class names, API endpoints, file paths
2. DO NOT translate: Technical acronyms (CUDA, ROS, AI, RAG, GPU, VRAM, etc.)
3. DO NOT translate: Library/framework names (PyTorch, TensorFlow, FastAPI, React, etc.)
4. DO NOT translate: Commands and terminal instructions
5. Translate ONLY: Explanatory prose, descriptions, examples (where not code)

STYLE GUIDELINES:
- Use conversational Roman Urdu (as spoken in Pakistan/India)
- Keep sentences clear and concise
- Maintain technical accuracy
- Preserve all markdown formatting (headers, lists, bold, italics)
- Keep code blocks exactly as-is with language tags

CONTENT TO TRANSLATE:
{chapter_content}

ROMAN URDU TRANSLATION:
"""
```

**Technical Term Glossary** (to be preserved):
- Hardware: GPU, CPU, VRAM, RAM, SSD, CUDA cores, Tensor cores, Jetson, Orin, RTX
- Software: Python, C++, ROS, Docker, Kubernetes, FastAPI, React, Docusaurus
- AI/ML: TensorFlow, PyTorch, RAG, embeddings, vector database, Qdrant, LLM, Grok
- Robotics: SLAM, navigation, perception, planning, control, sensors, LiDAR, IMU

**Rationale**:
- Explicit preservation rules prevent over-translation of technical content
- Glossary ensures consistency across all translations
- Markdown preservation critical for Docusaurus rendering
- Conversational Roman Urdu improves accessibility for target audience

**Partial Translation Handling**:
- Add `status` field to Translation model: `draft`, `published`, `in_progress`
- Show "AI Translation in progress" indicator for `draft` or `in_progress` status
- Fallback to English content if translation unavailable (per spec FR-017)

**Alternatives Considered**:
- Human translation only: Too slow, expensive for 13 weeks of content
- Google Translate API: Poor quality for technical Urdu, doesn't preserve terms
- Hybrid (AI + human review): Good approach, start with AI, allow manual edits later

**Implementation**:
- Create `backend/services/translation_service.py`
- Build glossary of technical terms (expandable)
- Add translation status tracking to database model
- Create admin endpoint for manual translation updates

---

## Research Task 4: Curriculum Content Structure

**Question**: How to organize 13 weeks of markdown files for efficient personalization?

**Decision**: Use hierarchical folder structure with metadata files for efficient retrieval.

**Folder Structure**:
```text
curriculum-content/
├── weeks/
│   ├── week-01/
│   │   ├── _category_.json          # Week metadata (title, description)
│   │   ├── 01-introduction.md        # Chapter content
│   │   ├── 02-ros2-basics.md
│   │   └── 03-simulation.md
│   ├── week-02/
│   │   ├── _category_.json
│   │   └── ...
│   └── ... (weeks 1-13)
└── metadata/
    ├── curriculum.yaml               # Overall curriculum metadata
    └── hardware-profiles.yaml        # Hardware profile definitions
```

**Week Metadata** (`_category_.json`):
```json
{
  "week_number": 1,
  "title": "Introduction to Physical AI",
  "description": "Foundational concepts and setup",
  "estimated_hours": 10,
  "prerequisites": []
}
```

**Chapter Frontmatter** (in markdown files):
```markdown
---
title: "Introduction to ROS 2"
order: 2
estimated_time: "2 hours"
tags: ["ros2", "middleware", "fundamentals"]
hardware_relevant: ["sim_rig", "edge_kit"]  # Which hardware profiles this applies to
---

Chapter content here...
```

**Rationale**:
- Docusaurus-native structure (uses `_category_.json` convention)
- Frontmatter enables filtering and personalization logic
- Hierarchical organization matches 13-week curriculum structure
- Metadata enables batch ingestion and efficient queries

**Alternatives Considered**:
- Database-only storage: Loses git versioning, harder to review content changes
- Single markdown file per week: Too large, hard to personalize at chapter level
- Flat structure: Loses week/chapter hierarchy, harder to navigate

**Implementation**:
- Create `backend/services/curriculum_service.py` for content retrieval
- Build batch ingestion script: `backend/ingestion/ingest_curriculum.py`
- Create database models: `CurriculumWeek`, `Chapter`
- Add admin endpoint for content updates

---

## Research Task 5: Docusaurus Theme Customization

**Question**: How to manage translation toggle state across Docusaurus pages?

**Decision**: Use React Context for global state + localStorage for persistence.

**Architecture**:
```typescript
// src/context/PersonalizationContext.tsx
interface PersonalizationContext {
  hardwareProfile: HardwareProfile | null;
  skillLevel: SkillLevel;
  language: 'en' | 'ur-Latn';
  personalizationEnabled: boolean;
  setLanguage: (lang: 'en' | 'ur-Latn') => void;
  setPersonalizationEnabled: (enabled: boolean) => void;
}

// src/theme/DocItem/index.tsx (custom wrapper)
export default function DocItem(props) {
  const { language, personalizationEnabled, hardwareProfile } = usePersonalization();
  
  return (
    <OriginalDocItem
      {...props}
      translationToggle={
        <TranslationToggle 
          currentLang={language}
          chapterId={props.content.metadata.id}
        />
      }
      personalizedSummary={
        personalizationEnabled 
          ? <PersonalizedSummary chapterId={props.content.metadata.id} />
          : null
      }
    />
  );
}
```

**State Persistence**:
- Initial load: Read from localStorage
- Authenticated users: Sync with backend user profile
- Unauthenticated users: localStorage only
- Language preference: Persist across sessions

**Component Placement**:
- Translation toggle: Top-right of chapter content (above main text)
- Personalization indicator: Below title, shows current hardware profile
- Hardware profile editor: Link in user menu or profile page

**Rationale**:
- React Context provides clean global state management
- localStorage ensures persistence without backend roundtrip
- Docusaurus theme swizzling allows deep customization
- Separation of concerns (context, components, backend API)

**Alternatives Considered**:
- Redux/Zustand: Overkill for simple state (language + toggle)
- URL query params: Clutters URLs, requires parsing on every page
- Backend-only state: Slow, requires auth for every preference change

**Implementation**:
- Create `PersonalizationContext.tsx` with provider
- Swizzle Docusaurus DocItem component: `npm swizzle @docusaurus/theme-classic DocItem`
- Build TranslationToggle, PersonalizationToggle components
- Add localStorage sync logic in context provider

---

## Research Task 6: Caching Strategy

**Question**: Whether to cache personalized summaries or generate on-demand?

**Decision**: Use hybrid caching with database storage + optional Redis for high-traffic scenarios.

**Caching Layers**:

**Layer 1: Database Storage (Primary)**:
- Store generated summaries in `ChapterSummary` table
- Key: `(chapter_id, hardware_profile_type, skill_level)`
- Regenerate on: content update, user requests refresh
- TTL: None (persist until content changes)

**Layer 2: In-Memory Cache (Optional, Phase 2)**:
- Use Redis or FastAPI `lru_cache` for hot summaries
- TTL: 1 hour
- Invalidate on: database update, manual admin refresh

**Cache Invalidation**:
- Content update: Invalidate all summaries for that chapter
- Hardware profile update: Invalidate summaries for affected profile type
- Admin action: Manual cache clear endpoint

**Rationale**:
- Database storage provides persistence across restarts
- Unique constraint prevents duplicate generation
- Fast lookup by (chapter_id, hardware_profile, skill_level)
- Redis can be added later if performance requires

**Performance Estimates**:
- Grok API call: ~500-1000ms per summary generation
- Database lookup: ~10-50ms
- Cache hit ratio target: 90%+ (most users share hardware profiles)

**Alternatives Considered**:
- Generate on-demand every time: Too slow, redundant API calls
- Cache everything in Redis: Loses persistence, harder to debug
- Pre-generate all combinations: 13 weeks × ~10 chapters × 3 hardware × 3 skill = ~1,170 summaries (feasible but inflexible)

**Implementation**:
- Create `ChapterSummary` model with unique constraint
- Add `generated_at` timestamp for cache freshness tracking
- Implement service method: `get_or_generate_summary(chapter_id, profile, skill)`
- Add admin endpoint: `POST /api/v1/personalization/cache/clear`

---

## Summary of Decisions

| Unknown | Decision | Impact |
|---------|----------|--------|
| User model extension | Add `skill_level` to `StudentProfile` | No Better-Auth conflicts, clean separation |
| Grok prompt engineering | Structured templates with context injection | Consistent output, preserves markdown |
| Roman Urdu translation | Preservation rules + technical glossary | Accurate technical content, readable Urdu |
| Curriculum structure | Hierarchical folders + frontmatter | Docusaurus-native, git-versioned |
| Frontend state management | React Context + localStorage | Simple, persistent, no backend dependency |
| Caching strategy | Database storage + optional Redis | Persistent, fast lookup, scalable |

---

## Next Steps

1. **Create data-model.md**: Define complete schema for new models
2. **Create API contracts**: Write OpenAPI specification
3. **Create quickstart.md**: Setup instructions for developers
4. **Update agent context**: Add new technologies to Qwen agent file
5. **Proceed to /sp.tasks**: Break implementation into testable tasks
