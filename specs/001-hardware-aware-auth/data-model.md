# Data Model: Hardware-Aware Authentication and Personalization

**Created**: 2026-03-16
**Feature**: 001-hardware-aware-auth
**Purpose**: Define database entities, relationships, and validation rules for student authentication, PDF-specified hardware profiles, and curriculum progress tracking

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────┐       ┌──────────────────┐
│    User     │──1:1──│ StudentProfile│──1:1──│ HardwareConfig   │
└─────────────┘       └──────────────┘       └──────────────────┘
       │                      │
       │1:many                │1:many
       ▼                      ▼
┌──────────────┐       ┌──────────────────┐
│ ChatSession  │       │ CurriculumProgress
└──────────────┘       └──────────────────┘
       │
       │1:many
       ▼
┌──────────────┐
│ ChatMessage  │
└──────────────┘
```

---

## Entity Definitions

### User

**What it represents**: Core authentication entity representing a registered student with credentials (email/password or GitHub OAuth). Managed by Better-Auth.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Not Null | Unique user identifier |
| `email` | String(255) | Unique, Not Null | Student's email address |
| `password_hash` | String(255) | Nullable | Bcrypt hash (null for OAuth-only users) |
| `github_id` | String(100) | Unique, Nullable | GitHub OAuth provider ID |
| `email_verified` | Boolean | Default False | Whether email is verified |
| `created_at` | DateTime | Not Null | Account creation timestamp |
| `updated_at` | DateTime | Not Null | Last update timestamp |
| `last_login_at` | DateTime | Nullable | Most recent login timestamp |

**Relationships**:
- 1:1 with `StudentProfile`
- 1:many with `ChatSession`

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Password must be at least 8 characters (enforced by Better-Auth)
- Either `password_hash` or `github_id` must be present
- Email must be unique across all users

**State Transitions**:
```
[Unverified] --email verification--> [Verified]
[Unverified] --login attempt--> [Verified] (auto-verify on OAuth)
[Active] --account deletion--> [Deleted] (soft delete)
```

---

### StudentProfile

**What it represents**: Extended student information including curriculum progress summary, preferences, and linkage to hardware configuration.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Not Null | Unique profile identifier |
| `user_id` | UUID | Foreign Key, Not Null | Reference to User.id |
| `display_name` | String(100) | Nullable | Student's preferred name |
| `avatar_url` | String(500) | Nullable | Profile picture URL |
| `bio` | Text | Nullable | Student biography |
| `timezone` | String(50) | Default 'UTC' | Student's timezone |
| `total_weeks_completed` | Integer | Default 0 | Cached count of completed weeks |
| `created_at` | DateTime | Not Null | Profile creation timestamp |
| `updated_at` | DateTime | Not Null | Last profile update timestamp |

**Relationships**:
- 1:1 with `User` (cascade delete)
- 1:1 with `HardwareConfig`
- 1:many with `CurriculumProgress`

**Validation Rules**:
- `user_id` must reference an existing User
- `display_name` must be 3-50 characters if provided
- `timezone` must be valid IANA timezone format

---

### HardwareConfig

**What it represents**: Student's hardware specifications from PDF "Hardware Reality" section (Page 5), used for personalizing chatbot responses.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Not Null | Unique hardware config identifier |
| `student_profile_id` | UUID | Foreign Key, Unique, Not Null | Reference to StudentProfile.id |
| `hardware_type` | String(20) | Not Null | Type: "sim_rig" or "edge_kit" |
| `gpu_model` | String(200) | Nullable | GPU model (e.g., "RTX 4070 Ti", "Jetson Orin Nano integrated") |
| `gpu_vram_gb` | Integer | Nullable | GPU VRAM in GB (e.g., 12, 16, 24) |
| `ubuntu_version` | String(20) | Nullable | Ubuntu version (e.g., "22.04", "20.04") |
| `edge_kit_type` | String(100) | Nullable | Edge device: "Jetson Orin Nano", "Jetson Orin NX", "Jetson AGX Orin" |
| `jetpack_version` | String(20) | Nullable | JetPack version (e.g., "5.1", "5.0") |
| `robot_model` | String(50) | Nullable | Robot: "Unitree Go2", "Unitree G1", "Proxy" |
| `sensor_model` | String(100) | Nullable | Sensor: "RealSense D435i", "RealSense D455", "OAK-D" |
| `additional_specs` | JSONB | Default {} | Flexible field for other specs |
| `created_at` | DateTime | Not Null | Config creation timestamp |
| `updated_at` | DateTime | Not Null | Last update timestamp |

**Relationships**:
- 1:1 with `StudentProfile` (cascade delete)

**Validation Rules**:
- `student_profile_id` must reference an existing StudentProfile
- `hardware_type` must be one of: "sim_rig", "edge_kit"
- If `hardware_type` = "sim_rig", then `gpu_vram_gb` >= 12 (PDF Page 5: RTX 4070 Ti+ 12GB minimum)
- If `hardware_type` = "edge_kit", then `edge_kit_type` must be set
- `edge_kit_type` must be one of: "Jetson Orin Nano", "Jetson Orin NX", "Jetson AGX Orin"
- `robot_model` must be one of: "Unitree Go2", "Unitree G1", "Proxy"
- `sensor_model` should include "RealSense D435i" as primary option (PDF-specified)

**PDF Hardware Mapping** (Page 5 "Hardware Reality"):
```
Sim Rig (Workstation):
  - GPU: RTX 4070 Ti+ (12GB VRAM minimum)
  - OS: Ubuntu 22.04
  - Use: Simulation, training, heavy computation

Edge Kit:
  - Device: Jetson Orin Nano / NX / AGX Orin
  - Use: Inference, Sim-to-Real (Page 8)
  - Constraints: Resource-limited, power-efficient

Robots:
  - Quadruped: Unitree Go2
  - Humanoid: Unitree G1
  - Simulation: Proxy

Sensors:
  - Primary: RealSense D435i (depth + IMU)
```

**Example JSONB additional_specs**:
```json
{
  "cpu_model": "Intel i7-13700K",
  "ram_gb": 32,
  "storage_type": "NVMe SSD",
  "monitor_resolution": "1920x1080",
  "internet_speed_mbps": 100,
  "preferred_ide": "VS Code"
}
```

---

### CurriculumProgress

**What it represents**: Record of completed curriculum weeks (Weeks 1-13) for a student, tracking progress through the PDF-defined curriculum.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Not Null | Unique progress record identifier |
| `student_profile_id` | UUID | Foreign Key, Not Null | Reference to StudentProfile.id |
| `week_number` | Integer | Not Null, CHECK 1-13 | Week number (1-13) |
| `module_id` | String(50) | Not Null | Module identifier (e.g., "01-ros-2", "02-gazebo") |
| `completed_at` | DateTime | Not Null | Completion timestamp |
| `score_percentage` | Integer | Nullable, CHECK 0-100 | Assessment score if applicable |
| `notes` | Text | Nullable | Student notes for this week |

**Relationships**:
- 1:many with `StudentProfile` (cascade delete)

**Validation Rules**:
- `student_profile_id` must reference an existing StudentProfile
- `week_number` must be between 1 and 13 (inclusive)
- `module_id` must match valid module pattern (e.g., `^\d{2}-[a-z0-9-]+$`)
- `score_percentage` must be 0-100 if provided
- Unique constraint on (`student_profile_id`, `week_number`, `module_id`) to prevent duplicates

**Indexes**:
- Index on `student_profile_id` for fast lookups
- Index on `week_number` for curriculum analytics
- Composite index on (`student_profile_id`, `completed_at`) for progress timeline

**Weekly Breakdown Structure** (from PDF):
```
Weeks 1-3: ROS 2 Fundamentals
Weeks 4-6: Simulation with Gazebo
Weeks 7-9: NVIDIA Isaac Integration
Weeks 10-13: VLA and Advanced Topics
```

---

### ChatSession

**What it represents**: A conversation session between a student and the chatbot, with hardware context tracking.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Not Null | Unique session identifier |
| `user_id` | UUID | Foreign Key, Not Null | Reference to User.id |
| `title` | String(200) | Nullable | Session title (auto-generated or user-provided) |
| `hardware_context_injected` | Boolean | Default False | Whether hardware profile was injected |
| `hardware_type_at_session` | String(20) | Nullable | Hardware type at time of session: "sim_rig" or "edge_kit" |
| `created_at` | DateTime | Not Null | Session creation timestamp |
| `updated_at` | DateTime | Not Null | Last message timestamp |
| `message_count` | Integer | Default 0 | Cached message count |

**Relationships**:
- 1:many with `User` (cascade delete)
- 1:many with `ChatMessage`

**Validation Rules**:
- `user_id` must reference an existing User
- `title` must be 1-200 characters if provided
- `message_count` must be non-negative

**Indexes**:
- Index on `user_id` for fast user session lookups
- Index on `updated_at` for sorting by recent activity

---

### ChatMessage

**What it represents**: Individual messages within a chat session, including hardware context snapshot.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Not Null | Unique message identifier |
| `chat_session_id` | UUID | Foreign Key, Not Null | Reference to ChatSession.id |
| `role` | String(20) | Not Null | Message role: "user", "assistant", or "system" |
| `content` | Text | Not Null | Message content |
| `selected_text` | Text | Nullable | User-selected text for context |
| `hardware_profile_snapshot` | JSONB | Nullable | Hardware context at time of message |
| `pdf_page_references` | JSONB | Nullable | PDF pages referenced (e.g., [5, 8]) |
| `sources` | JSONB | Nullable | Source attributions (file paths, similarity scores) |
| `confidence_score` | Float | Nullable | RAG confidence (0.0-1.0) |
| `created_at` | DateTime | Not Null | Message timestamp |
| `tokens_used` | Integer | Nullable | Token count for cost tracking |

**Relationships**:
- 1:many with `ChatSession` (cascade delete)

**Validation Rules**:
- `chat_session_id` must reference an existing ChatSession
- `role` must be one of: "user", "assistant", "system"
- `content` must not be empty
- `confidence_score` must be 0.0-1.0 if provided
- `tokens_used` must be non-negative if provided

**Indexes**:
- Index on `chat_session_id` for fast message retrieval
- Index on `created_at` for chronological ordering
- Full-text search index on `content` for chat history search

**Example hardware_profile_snapshot JSONB**:
```json
{
  "hardware_type": "edge_kit",
  "edge_kit_type": "Jetson Orin Nano",
  "gpu_vram_gb": 8,
  "robot_model": "Unitree Go2",
  "pdf_page_5_prioritized": true,
  "pdf_page_8_inference_mode": true
}
```

---

## Database Schema (SQLAlchemy)

```python
# Example SQLAlchemy models (for reference)

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSONB, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    github_id = Column(String(100), unique=True, nullable=True, index=True)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    # Relationships
    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    timezone = Column(String(50), default="UTC")
    total_weeks_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    hardware_config = relationship("HardwareConfig", back_populates="student_profile", uselist=False, cascade="all, delete-orphan")
    curriculum_progress = relationship("CurriculumProgress", back_populates="student_profile", cascade="all, delete-orphan")

class HardwareConfig(Base):
    __tablename__ = "hardware_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_profile_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    hardware_type = Column(String(20), nullable=False)  # "sim_rig" or "edge_kit"
    gpu_model = Column(String(200), nullable=True)
    gpu_vram_gb = Column(Integer, nullable=True)
    ubuntu_version = Column(String(20), nullable=True)
    edge_kit_type = Column(String(100), nullable=True)  # "Jetson Orin Nano", "Jetson Orin NX", "Jetson AGX Orin"
    jetpack_version = Column(String(20), nullable=True)
    robot_model = Column(String(50), nullable=True)  # "Unitree Go2", "Unitree G1", "Proxy"
    sensor_model = Column(String(100), nullable=True)  # "RealSense D435i", etc.
    additional_specs = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student_profile = relationship("StudentProfile", back_populates="hardware_config")
    
    # Constraints (PDF Page 5 "Hardware Reality")
    __table_args__ = (
        CheckConstraint("hardware_type IN ('sim_rig', 'edge_kit')", name="check_hardware_type"),
        CheckConstraint("edge_kit_type IN ('Jetson Orin Nano', 'Jetson Orin NX', 'Jetson AGX Orin', NULL)", name="check_edge_kit_type"),
        CheckConstraint("robot_model IN ('Unitree Go2', 'Unitree G1', 'Proxy', NULL)", name="check_robot_model"),
    )

class CurriculumProgress(Base):
    __tablename__ = "curriculum_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_profile_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    week_number = Column(Integer, nullable=False)
    module_id = Column(String(50), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    score_percentage = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    student_profile = relationship("StudentProfile", back_populates="curriculum_progress")
    
    # Constraints (Weeks 1-13)
    __table_args__ = (
        CheckConstraint("week_number BETWEEN 1 AND 13", name="check_week_number"),
        CheckConstraint("score_percentage BETWEEN 0 AND 100 OR score_percentage IS NULL", name="check_score_percentage"),
        UniqueConstraint('student_profile_id', 'week_number', 'module_id', name='unique_progress_record'),
    )

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=True)
    hardware_context_injected = Column(Boolean, default=False)
    hardware_type_at_session = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    message_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="chat_session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    hardware_profile_snapshot = Column(JSONB, nullable=True)
    pdf_page_references = Column(JSONB, nullable=True)
    sources = Column(JSONB, nullable=True)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    tokens_used = Column(Integer, nullable=True)
    
    # Relationships
    chat_session = relationship("ChatSession", back_populates="messages")
```

---

## Migration Strategy

**Phase 1: Initial Schema**
1. Create `users` table (managed by Better-Auth)
2. Create `student_profiles`, `hardware_configs`, `curriculum_progress` tables
3. Create `chat_sessions`, `chat_messages` tables
4. Add CHECK constraints for PDF-specified values

**Phase 2: Data Migration (if needed)**
- Migrate existing chat data from current storage to new `chat_sessions`/`chat_messages` tables
- Link existing chat data to anonymous session IDs or new user accounts

**Phase 3: Indexes and Optimization**
- Add indexes after data migration
- Analyze query performance
- Add composite indexes as needed

**Rollback Plan**:
- All migrations are reversible
- Maintain backup before each migration phase
- Test rollback procedures in staging environment

---

## Validation Rules Summary

| Entity | Validation Rule | Enforcement Layer |
|--------|----------------|-------------------|
| User | Email format | Better-Auth + Database constraint |
| User | Password length (8+ chars) | Better-Auth |
| User | Unique email | Database unique constraint |
| StudentProfile | Display name length (3-50) | Application layer |
| HardwareConfig | Hardware type enum | Database CHECK constraint |
| HardwareConfig | Edge kit type enum | Database CHECK constraint |
| HardwareConfig | Robot model enum | Database CHECK constraint |
| HardwareConfig | GPU VRAM >= 12GB for sim_rig | Application layer |
| CurriculumProgress | Week number 1-13 | Database CHECK constraint |
| CurriculumProgress | Score 0-100 | Database CHECK constraint |
| ChatMessage | Role enum | Application layer + Database constraint |
| ChatMessage | Confidence score range (0-1) | Application layer |

---

## Data Retention Policy

| Entity | Retention Period | Deletion Policy |
|--------|-----------------|-----------------|
| User | Until account deletion | Soft delete (is_deleted flag), hard delete after 30 days |
| StudentProfile | Same as User | Cascade delete with User |
| HardwareConfig | Same as User | Cascade delete with StudentProfile |
| CurriculumProgress | 2 years after last activity | Archive old records, anonymize after 3 years |
| ChatSession | 1 year after last message | Soft delete, hard delete after 90 days |
| ChatMessage | Same as ChatSession | Cascade delete with ChatSession |
