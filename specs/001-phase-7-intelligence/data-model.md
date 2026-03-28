# Data Model Design: Phase 7 Final Intelligence

**Created**: 2026-03-26
**Feature**: 001-phase-7-intelligence
**Purpose**: Define complete database schema for personalization and curriculum features

---

## Existing Models (No Changes Required)

### User
**Location**: `backend/models/user.py`

```python
class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    github_id = Column(String(100), unique=True, nullable=True, index=True)
    email_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False, nullable=False, index=True)
    last_login_at = Column(DateTime, nullable=True)
    # skill_level: NOT HERE - belongs in StudentProfile
```

**Changes**: None. Authentication data remains separate from profile data.

---

### StudentProfile
**Location**: `backend/models/student_profile.py`

```python
class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    timezone = Column(String(50), default="UTC")
    total_weeks_completed = Column(Integer, default=0)
    
    # NEW FIELD for Phase 7
    skill_level = Column(String(20), default='beginner', nullable=False)
    # Values: 'beginner', 'intermediate', 'advanced'
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

**Changes**:
- Add `skill_level` column with default value `'beginner'`
- Add CheckConstraint for valid values

**Migration**:
```python
# Alembic migration
def upgrade():
    op.add_column('student_profiles', sa.Column('skill_level', sa.String(20), nullable=False, server_default='beginner'))
    op.create_check_constraint(
        'check_skill_level',
        'student_profiles',
        "skill_level IN ('beginner', 'intermediate', 'advanced')"
    )

def downgrade():
    op.drop_constraint('check_skill_level', 'student_profiles', type_='check')
    op.drop_column('student_profiles', 'skill_level')
```

---

### HardwareConfig
**Location**: `backend/models/student_profile.py`

```python
class HardwareConfig(Base):
    __tablename__ = "hardware_configs"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    student_profile_id = Column(GUID(), ForeignKey("student_profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    hardware_type = Column(String(20), nullable=False)  # "sim_rig" or "edge_kit"
    gpu_model = Column(String(200), nullable=True)
    gpu_vram_gb = Column(Integer, nullable=True)
    ubuntu_version = Column(String(20), nullable=True)
    edge_kit_type = Column(String(100), nullable=True)
    jetpack_version = Column(String(20), nullable=True)
    robot_model = Column(String(50), nullable=True)
    sensor_model = Column(String(100), nullable=True)
    additional_specs = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

**Changes**: None. Already supports required hardware profiles.

**Note**: Consider adding `'unitree'` as a third hardware type for robot-only setups.

---

## New Models

### CurriculumWeek
**Location**: `backend/models/curriculum.py` (new file)

```python
class CurriculumWeek(Base, TimestampMixin):
    """
    Represents one week of the 13-week Physical AI curriculum.
    
    Attributes:
        week_number: Week number (1-13)
        title: Week title (e.g., "Introduction to Physical AI")
        description: Week description and learning objectives
        order: Display order (should match week_number)
        estimated_hours: Expected time commitment
        prerequisites: JSON array of prerequisite week numbers
    """
    
    __tablename__ = "curriculum_weeks"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    week_number = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    estimated_hours = Column(Integer, nullable=True)
    prerequisites = Column(JSON, default=list)  # [1, 2] means weeks 1 and 2 are prerequisites
    
    # Relationships
    chapters = relationship(
        "Chapter",
        back_populates="curriculum_week",
        cascade="all, delete-orphan",
        order_by="Chapter.order",
    )
    
    __table_args__ = (
        CheckConstraint("week_number BETWEEN 1 AND 13", name="check_week_number"),
        CheckConstraint("order >= 1", name="check_order_positive"),
    )
```

---

### Chapter
**Location**: `backend/models/curriculum.py` (new file)

```python
class Chapter(Base, TimestampMixin):
    """
    Represents a single chapter/lesson within a curriculum week.
    
    Attributes:
        title: Chapter title
        content: Full markdown content
        order: Display order within week
        estimated_time: Expected time to complete (e.g., "2 hours")
        tags: JSON array of topic tags
        hardware_relevant: Which hardware profiles this applies to
    """
    
    __tablename__ = "chapters"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    curriculum_week_id = Column(GUID(), ForeignKey("curriculum_weeks.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)  # Full markdown content
    order = Column(Integer, nullable=False)
    estimated_time = Column(String(50), nullable=True)  # e.g., "2 hours"
    tags = Column(JSON, default=list)  # ["ros2", "middleware", "fundamentals"]
    hardware_relevant = Column(JSON, default=lambda: ["sim_rig", "edge_kit"])  # Applies to which hardware
    
    # Relationships
    curriculum_week = relationship("CurriculumWeek", back_populates="chapters")
    summaries = relationship(
        "ChapterSummary",
        back_populates="chapter",
        cascade="all, delete-orphan",
    )
    translations = relationship(
        "Translation",
        back_populates="chapter",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        CheckConstraint("order >= 1", name="check_chapter_order_positive"),
        UniqueConstraint('curriculum_week_id', 'order', name='unique_chapter_order_per_week'),
    )
```

---

### ChapterSummary
**Location**: `backend/models/curriculum.py` (new file)

```python
class ChapterSummary(Base, TimestampMixin):
    """
    Personalized chapter summary based on hardware profile and skill level.
    
    This is the cached output from the PersonalizationService.
    Generated on first request, then reused for same (chapter, hardware, skill) combination.
    
    Attributes:
        summary_content: Personalized markdown summary
        hardware_profile_type: Target hardware (sim_rig, edge_kit, unitree)
        skill_level: Target skill level (beginner, intermediate, advanced)
        generated_by: LLM model used (e.g., "grok-2")
        token_count: Tokens used for generation (for cost tracking)
    """
    
    __tablename__ = "chapter_summaries"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(GUID(), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    summary_content = Column(Text, nullable=False)  # Personalized markdown
    hardware_profile_type = Column(String(20), nullable=False)  # sim_rig, edge_kit, unitree
    skill_level = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    generated_by = Column(String(50), nullable=True)  # LLM model identifier
    token_count = Column(Integer, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="summaries")
    
    __table_args__ = (
        UniqueConstraint(
            'chapter_id', 
            'hardware_profile_type', 
            'skill_level', 
            name='unique_summary_per_combination'
        ),
        CheckConstraint(
            "hardware_profile_type IN ('sim_rig', 'edge_kit', 'unitree')",
            name="check_hardware_profile_type"
        ),
        CheckConstraint(
            "skill_level IN ('beginner', 'intermediate', 'advanced')",
            name="check_skill_level_summary"
        ),
    )
```

---

### Translation
**Location**: `backend/models/curriculum.py` (new file)

```python
class Translation(Base, TimestampMixin):
    """
    Roman Urdu translation of chapter content.
    
    Attributes:
        translated_content: Full translated markdown content
        language_code: IETF language tag (e.g., "ur-Latn" for Roman Urdu)
        status: Translation status (draft, in_review, published)
        translated_by: Source (e.g., "grok-2-ai", "human-admin")
        review_notes: Admin notes for translation quality
    """
    
    __tablename__ = "translations"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(GUID(), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    translated_content = Column(Text, nullable=False)
    language_code = Column(String(20), nullable=False)  # e.g., "ur-Latn"
    status = Column(String(20), default='draft', nullable=False, index=True)  # draft, in_review, published
    translated_by = Column(String(50), nullable=True)  # "grok-2-ai" or user ID
    review_notes = Column(Text, nullable=True)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="translations")
    
    __table_args__ = (
        UniqueConstraint(
            'chapter_id', 
            'language_code', 
            name='unique_translation_per_language'
        ),
        CheckConstraint(
            "status IN ('draft', 'in_review', 'published')",
            name="check_translation_status"
        ),
    )
```

---

## Relationships Diagram

```
User (1) ────── (1) StudentProfile (1) ────── (1) HardwareConfig
    │                                              │
    │                                              └─ hardware_type: sim_rig | edge_kit | unitree
    │                                              └─ skill_level: beginner | intermediate | advanced
    │
    └─ (many) ChatSessions (existing)

CurriculumWeek (1) ────── (many) Chapter
    │                           │
    └─ week_number: 1-13        ├─ (many) ChapterSummary
                                │   └─ (chapter_id, hardware_profile_type, skill_level) unique
                                │
                                └─ (many) Translation
                                    └─ (chapter_id, language_code) unique
```

---

## Indexes

**Performance Optimization**:

```sql
-- Existing indexes (keep)
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_student_profiles_user_id ON student_profiles(user_id);
CREATE INDEX idx_hardware_configs_profile_id ON hardware_configs(student_profile_id);

-- New indexes for Phase 7
CREATE INDEX idx_curriculum_weeks_number ON curriculum_weeks(week_number);
CREATE INDEX idx_chapters_week_id ON chapters(curriculum_week_id);
CREATE INDEX idx_chapter_summaries_chapter_id ON chapter_summaries(chapter_id);
CREATE INDEX idx_chapter_summaries_lookup 
    ON chapter_summaries(chapter_id, hardware_profile_type, skill_level);
CREATE INDEX idx_translations_chapter_id ON translations(chapter_id);
CREATE INDEX idx_translations_status ON translations(status);
```

---

## Validation Rules

### StudentProfile.skill_level
- **Type**: String
- **Allowed Values**: `'beginner'`, `'intermediate'`, `'advanced'`
- **Default**: `'beginner'`
- **Validation**: CheckConstraint in database, Pydantic validator in schemas

### CurriculumWeek.week_number
- **Type**: Integer
- **Range**: 1-13
- **Unique**: Yes
- **Validation**: CheckConstraint

### ChapterSummary.hardware_profile_type
- **Type**: String
- **Allowed Values**: `'sim_rig'`, `'edge_kit'`, `'unitree'`
- **Validation**: CheckConstraint, auto-match unrecognized hardware to closest

### ChapterSummary.skill_level
- **Type**: String
- **Allowed Values**: `'beginner'`, `'intermediate'`, `'advanced'`
- **Validation**: CheckConstraint

### Translation.status
- **Type**: String
- **Allowed Values**: `'draft'`, `'in_review'`, `'published'`
- **Default**: `'draft'`
- **Validation**: CheckConstraint

---

## State Transitions

### Translation Lifecycle

```
[draft] ──(submit for review)──> [in_review] ──(approve)──> [published]
   │                                  │
   └────────────(reject)──────────────┘
```

**Transitions**:
- `draft → in_review`: Admin submits for review
- `in_review → published`: Admin approves
- `in_review → draft`: Admin requests changes
- `published → draft`: Admin unpublishes for updates

---

## Migration Strategy

### Phase 1: Schema Changes
```sql
-- 1. Add skill_level to StudentProfile
ALTER TABLE student_profiles 
ADD COLUMN skill_level VARCHAR(20) DEFAULT 'beginner' NOT NULL;

ALTER TABLE student_profiles 
ADD CONSTRAINT check_skill_level 
CHECK (skill_level IN ('beginner', 'intermediate', 'advanced'));

-- 2. Create new tables
CREATE TABLE curriculum_weeks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    week_number INTEGER NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    "order" INTEGER NOT NULL,
    estimated_hours INTEGER,
    prerequisites JSON DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_week_number CHECK (week_number BETWEEN 1 AND 13),
    CONSTRAINT check_order_positive CHECK ("order" >= 1)
);

CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    curriculum_week_id UUID NOT NULL REFERENCES curriculum_weeks(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    "order" INTEGER NOT NULL,
    estimated_time VARCHAR(50),
    tags JSON DEFAULT '[]',
    hardware_relevant JSON DEFAULT '["sim_rig", "edge_kit"]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_chapter_order_positive CHECK ("order" >= 1),
    CONSTRAINT unique_chapter_order_per_week UNIQUE (curriculum_week_id, "order")
);

CREATE TABLE chapter_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    summary_content TEXT NOT NULL,
    hardware_profile_type VARCHAR(20) NOT NULL,
    skill_level VARCHAR(20) NOT NULL,
    generated_by VARCHAR(50),
    token_count INTEGER,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_summary_per_combination UNIQUE (chapter_id, hardware_profile_type, skill_level),
    CONSTRAINT check_hardware_profile_type CHECK (hardware_profile_type IN ('sim_rig', 'edge_kit', 'unitree')),
    CONSTRAINT check_skill_level_summary CHECK (skill_level IN ('beginner', 'intermediate', 'advanced'))
);

CREATE TABLE translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    translated_content TEXT NOT NULL,
    language_code VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,
    translated_by VARCHAR(50),
    review_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_translation_per_language UNIQUE (chapter_id, language_code),
    CONSTRAINT check_translation_status CHECK (status IN ('draft', 'in_review', 'published'))
);
```

### Phase 2: Data Migration
- No existing data to migrate (new feature)
- Initial curriculum content will be ingested via script

### Phase 3: Backfill
- Generate initial chapter summaries for all (chapter, hardware, skill) combinations
- Estimated: 13 weeks × 5 chapters/week × 3 hardware × 3 skill = ~585 summaries
- Run as background job after deployment

---

## Pydantic Schemas

**Location**: `backend/schemas/`

### user_profile.py
```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class HardwareType(str, Enum):
    SIM_RIG = "sim_rig"
    EDGE_KIT = "edge_kit"
    UNITREE = "unitree"

class StudentProfileUpdate(BaseModel):
    skill_level: Optional[SkillLevel] = None
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)
    timezone: Optional[str] = Field(None, max_length=50)

class HardwareConfigCreate(BaseModel):
    hardware_type: HardwareType
    gpu_model: Optional[str] = None
    gpu_vram_gb: Optional[int] = Field(None, ge=1, le=128)
    ubuntu_version: Optional[str] = None
    edge_kit_type: Optional[str] = None
    jetpack_version: Optional[str] = None
    robot_model: Optional[str] = None
    additional_specs: dict = Field(default_factory=dict)
```

### curriculum.py
```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CurriculumWeekBase(BaseModel):
    week_number: int = Field(ge=1, le=13)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    order: int = Field(ge=1)
    estimated_hours: Optional[int] = None
    prerequisites: List[int] = Field(default_factory=list)

class ChapterBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str
    order: int = Field(ge=1)
    estimated_time: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    hardware_relevant: List[str] = Field(default=["sim_rig", "edge_kit"])

class ChapterSummaryResponse(BaseModel):
    summary_content: str
    hardware_profile_type: str
    skill_level: str
    generated_at: datetime
    
    class Config:
        from_attributes = True

class TranslationResponse(BaseModel):
    translated_content: str
    language_code: str
    status: str
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

---

## Next Steps

1. Create Alembic migrations for new tables
2. Implement Pydantic schemas in `backend/schemas/`
3. Create repository classes for CRUD operations
4. Write unit tests for model validation
5. Proceed to API contract design
