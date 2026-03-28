# Technical Research: Hardware-Aware Authentication and Personalization

**Created**: 2026-03-16
**Feature**: 001-hardware-aware-auth
**Purpose**: Resolve technical unknowns and document best practices for Better-Auth integration, PDF-specified hardware profiles, context injection service, and curriculum tracking

---

## Decision 1: Better-Auth Integration with FastAPI

**What was chosen**: Integrate Better-Auth as a standalone authentication service with session-based authentication using secure cookies, compatible with FastAPI backend and React/Docusaurus frontend.

**Why chosen**: 
- Better-Auth provides out-of-the-box support for both email/password and OAuth providers (GitHub)
- Session-based authentication with secure cookies aligns with security best practices
- Built-in JWT support for API authentication
- TypeScript/JavaScript native (works well with Docusaurus/React)
- Actively maintained with good documentation

**Alternatives considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Auth0 | Fully managed, enterprise features | Expensive at scale, external dependency | Overkill for textbook project, adds latency |
| NextAuth.js | Great for Next.js, good OAuth support | Tightly coupled to Next.js ecosystem | Not compatible with Docusaurus architecture |
| FastAPI Users | Python-native, good FastAPI integration | Limited OAuth provider support, less mature | Better-Auth has broader provider support |
| Custom JWT implementation | Full control, no external dependencies | Security risks, maintenance burden | Authentication is security-critical; use battle-tested solution |

**Implementation approach**:
- Run Better-Auth as a Node.js service alongside FastAPI (or embed in Docusaurus frontend)
- Use Better-Auth's session cookies for browser-based authentication
- FastAPI validates sessions via Better-Auth's verification endpoints or shared secret
- Store user data in PostgreSQL/SQLite via SQLAlchemy ORM

**Best practices identified**:
- Use secure cookie flags: `HttpOnly`, `Secure`, `SameSite=Strict`
- Implement CSRF protection for state-changing operations
- Rate limit authentication endpoints to prevent brute force attacks
- Hash passwords with bcrypt or argon2 (Better-Auth handles this)
- Implement session expiration and refresh token rotation

---

## Decision 2: Database Schema for PDF Hardware Profiles

**What was chosen**: SQLAlchemy ORM with SQLite for development and Neon Serverless PostgreSQL for production, using JSONB columns for flexible hardware specifications that map to PDF "Hardware Reality" section (Page 5).

**Why chosen**:
- SQLAlchemy is already familiar in Python ecosystem
- SQLite requires zero configuration for development
- Neon Serverless PostgreSQL provides auto-scaling, free tier available
- JSONB columns allow flexible hardware specs without schema migrations
- Existing backend uses Python; SQLAlchemy integrates naturally
- PDF specifies exact hardware configurations requiring structured storage

**PDF Hardware Mapping** (Page 5 "Hardware Reality"):
```
Workstation (Sim Rig):
  - GPU: RTX 4070 Ti+ with 12GB VRAM minimum
  - OS: Ubuntu 22.04
  - Use Case: Simulation, training, heavy computation

Edge Kit:
  - Device: Jetson Orin Nano or Jetson Orin NX
  - Use Case: Inference, Sim-to-Real deployment (Page 8)
  - Constraints: Resource-limited, power-efficient

Sensors:
  - Camera: RealSense D435i (depth + IMU)
  
Robots:
  - Quadruped: Unitree Go2
  - Humanoid: Unitree G1
  - Alternative: Proxy (simulation placeholder)
```

**Alternatives considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Prisma (Node.js) | Type-safe, great DX | Requires Node.js runtime, separate from Python backend | Backend is Python-based; would add complexity |
| Raw SQL with asyncpg | Maximum performance, full control | No ORM benefits, more boilerplate | SQLAlchemy provides good balance of performance and productivity |
| MongoDB | Flexible schema, good for JSON | Not relational, different query patterns | User data is highly relational; SQL is better fit |
| Supabase | Managed Postgres + auth | External dependency, vendor lock-in | Better-Auth + Neon provides same benefits with more control |

**Schema design patterns**:
- `users` table: Core authentication data (email, password hash, OAuth provider info) - managed by Better-Auth
- `student_profiles` table: Extended profile data (1:1 relationship with users)
- `hardware_configs` table: PDF-specified hardware configurations with JSONB for flexible fields (1:1 with student_profiles)
- `curriculum_progress` table: Completed weeks (Weeks 1-13) with timestamps (1:many with student_profiles)
- `chat_sessions` table: Conversation metadata (1:many with users)
- `chat_messages` table: Individual messages (1:many with chat_sessions)

**Best practices identified**:
- Use UUIDs for primary keys (better for distributed systems)
- Add indexes on foreign keys and frequently queried fields (email, session_id)
- Implement soft deletes for user data (audit trail)
- Use database migrations (Alembic) for schema evolution
- Encrypt sensitive data at rest (hardware specs may contain serial numbers)
- Use CHECK constraints for PDF-specified enums (hardware_type, robot_model)

---

## Decision 3: Context Injection Service Architecture

**What was chosen**: HardwareContextService that fetches the student's hardware profile and prepends a "Hardware Constraint" instruction to the Grok API prompt, with PDF Page 5 and Page 8 logic integration.

**Why chosen**:
- Centralized logic for personalization (single source of truth)
- Separation from RAG pipeline (maintains modularity)
- Allows testing personalization independently
- Respects PDF constraints without modifying core RAG logic

**Implementation pattern**:
```python
class HardwareContextService:
    async def get_hardware_context(self, user_id: str) -> HardwareContext:
        # Fetch hardware profile from database
        # Return context object with PDF-specified fields
    
    def inject_context(self, prompt: str, context: HardwareContext) -> str:
        # Prepend hardware constraint instruction
        # Prioritize PDF Page 5 "Hardware Reality" and Page 8 "Inference/Sim-to-Real"
        # Return augmented prompt
```

**Logic Rule Implementation** (from user instructions):
```
IF user hardware = "Jetson Orin Nano" THEN:
  - Prioritize "Inference" advice from PDF Page 8
  - Prioritize "Sim-to-Real" deployment guidance from PDF Page 8
  - Emphasize resource-constrained optimization
  - Mention Jetson-specific tools (JetPack, TensorRT)

IF user hardware = "Sim Rig" (RTX 4070 Ti) THEN:
  - Provide workstation-optimized commands
  - Assume Ubuntu 22.04 environment
  - Enable full simulation capabilities
  - Reference Gazebo, Isaac Sim without constraints
```

**Prompt injection strategy**:
```
System: You are a Physical AI textbook assistant.

<Hardware Context>
Student Hardware Profile:
- Type: Edge Kit (Jetson Orin Nano)
- GPU VRAM: 8GB
- OS: Ubuntu 22.04 (JetPack)
- Robot: Unitree Go2
- Sensors: RealSense D435i

Hardware Constraints (PDF Page 5):
- Prioritize inference-optimized approaches
- Focus on Sim-to-Real deployment (PDF Page 8)
- Consider resource constraints (memory, power)
</Hardware Context>

User Query: How do I deploy my SLAM algorithm?
```

**Alternatives considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Fine-tune model per hardware type | Highly personalized | Prohibitively expensive, slow | Prompt injection is instant and free |
| Separate RAG indexes per hardware | Hardware-specific retrieval | Index explosion, maintenance nightmare | Single index with context injection is simpler |
| Post-process responses | Can tailor after generation | May miss opportunities during generation | Pre-injection allows LLM to consider context during generation |

**Risk mitigation**:
- **Risk**: Hardware context overrides textbook technical steps
  - **Mitigation**: Place hardware context AFTER system instructions but BEFORE query
  - **Mitigation**: Use explicit delimiters: `<Hardware Context>...</Hardware Context>`
  - **Mitigation**: Include instruction: "Use hardware context to tailor advice, but DO NOT override textbook technical steps"
  - **Mitigation**: Test with adversarial queries to ensure textbook context wins

**Best practices identified**:
- Keep context injections concise (<300 tokens) to avoid prompt bloat
- Use structured format for context (XML-like tags)
- Implement context validation (don't inject malformed data)
- Log context injections for debugging and optimization
- A/B test personalization effectiveness
- Include PDF page references for traceability

---

## Decision 4: FastAPI Authentication Middleware

**What was chosen**: Custom FastAPI dependency injection for authentication that validates Better-Auth sessions and injects user context into request handlers.

**Why chosen**:
- FastAPI's dependency injection is designed for this use case
- Clean separation of concerns (auth logic separate from business logic)
- Automatic OpenAPI documentation for authenticated endpoints
- Reusable across all protected endpoints (/chat, /ingest, /profile)

**Implementation pattern**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    # Validate token/session with Better-Auth
    # Return user object or raise 401
```

**Endpoints requiring protection**:
- `POST /api/chat` - Requires valid session
- `POST /api/ingest` - Requires valid session
- `GET /api/user/profile` - Requires valid session
- `PUT /api/user/hardware-profile` - Requires valid session
- `POST /api/user/curriculum-progress` - Requires valid session

**Alternatives considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Global middleware | Applied automatically, centralized | Harder to test, less flexible | Dependency injection is more testable |
| Decorator-based auth | Simple to apply | Not FastAPI-native, no OpenAPI integration | Dependency injection integrates better |
| OAuth2 with password flow | Standard protocol | Complex for simple use case | Better-Auth sessions are simpler |

**Best practices identified**:
- Return 401 Unauthorized for missing/invalid tokens
- Return 403 Forbidden for insufficient permissions
- Cache user lookups to reduce database queries
- Log authentication failures for security monitoring
- Use HTTPS in production to protect tokens in transit

---

## Decision 5: Curriculum Progress Tracking Schema

**What was chosen**: Relational table mapping PDF "Weekly Breakdown" (Weeks 1-13) with completion tracking per student.

**Why chosen**:
- Simple relational model aligns with existing database structure
- Easy to query for progress summaries
- Supports partial completion and retakes
- Enables analytics on student performance

**Schema design**:
```sql
CREATE TABLE curriculum_progress (
    id UUID PRIMARY KEY,
    student_profile_id UUID REFERENCES student_profiles(id),
    week_number INTEGER CHECK (week_number BETWEEN 1 AND 13),
    module_id VARCHAR(50),  -- e.g., "01-ros-2", "02-gazebo"
    completed_at TIMESTAMP,
    score_percentage INTEGER CHECK (score_percentage BETWEEN 0 AND 100),
    notes TEXT,
    UNIQUE(student_profile_id, week_number, module_id)
);
```

**Alternatives considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| JSON array in profile | Simple, flexible | Hard to query, no validation | Relational provides better integrity |
| Separate progress service | Decoupled, scalable | Adds complexity, overkill | Single database is sufficient |
| Graph database | Great for dependencies | Unnecessary complexity | Curriculum is linear (Weeks 1-13) |

**Best practices identified**:
- Add index on `student_profile_id` for fast lookups
- Add index on `completed_at` for progress timeline queries
- Include `score_percentage` for assessment tracking
- Support retakes (multiple entries per week with different timestamps)
- Validate week numbers (1-13) at database level

---

## Decision 6: Frontend Hardware Setup Form Strategy

**What was chosen**: React-based hardware setup form with PDF-specified dropdown options, integrated into Docusaurus via custom React components.

**Why chosen**:
- Docusaurus supports React components natively
- Dropdowns ensure students select from PDF-specified options
- Form validation prevents invalid hardware configurations
- Provides immediate feedback on hardware selection

**Implementation components**:
- `HardwareProfileForm.jsx`: Main form component with PDF-based options
- `HardwareTypeSelector.jsx`: Sim Rig vs Edge Kit toggle
- `RobotSelector.jsx`: Unitree Go2/G1/Proxy dropdown
- `SensorSelector.jsx`: RealSense D435i and other sensor options
- `useHardwareProfile.js`: Hook for form state management

**Form fields** (mapped to PDF):
```
Hardware Type: [Sim Rig / Edge Kit] (required)

If Sim Rig:
  - GPU Model: [RTX 4070 Ti (12GB), RTX 4080 (16GB), RTX 4090 (24GB), Other]
  - VRAM: [12GB, 16GB, 24GB, Other]
  - OS: [Ubuntu 22.04 (recommended), Ubuntu 20.04, Windows 11 WSL, Other]

If Edge Kit:
  - Device: [Jetson Orin Nano, Jetson Orin NX, Jetson AGX Orin, Other]
  - JetPack Version: [5.1, 5.0, Other]

Robot Model: [Unitree Go2, Unitree G1, Proxy (simulation), Other]

Sensors: [RealSense D435i, RealSense D455, OAK-D, Other]
```

**Alternatives considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Free-text input | Maximum flexibility | Invalid entries, hard to validate | Dropdowns ensure PDF compliance |
| Wizard-style multi-step | Guided experience | More complex, longer setup | Single form is faster |
| Image-based selection | Visual, intuitive | Requires asset creation | Text dropdowns are sufficient |

**Best practices identified**:
- Show PDF page references next to options (e.g., "Page 5")
- Provide tooltips explaining hardware differences
- Auto-save profile on form submission
- Show hardware-aware tips after selection
- Allow profile updates at any time

---

## Decision 7: Token Synchronization Strategy

**What was chosen**: Better-Auth manages sessions via secure HTTP-only cookies; FastAPI validates sessions by calling Better-Auth verification endpoint or using shared JWT secret.

**Why chosen**:
- HTTP-only cookies are more secure than localStorage for tokens
- Better-Auth handles session lifecycle (creation, expiration, refresh)
- FastAPI can validate tokens independently without tight coupling
- Supports both session-based (browser) and JWT (API) authentication

**Synchronization pattern**:
1. Student logs in via Docusaurus → Better-Auth sets session cookie
2. Docusaurus makes API calls to FastAPI with cookie automatically included
3. FastAPI extracts session token from cookie header
4. FastAPI validates token with Better-Auth (RPC call) or verifies JWT signature
5. FastAPI injects user context into request

**Alternatives considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Shared Redis session store | Fast validation, centralized | Adds infrastructure complexity | Better-Auth's verification endpoint is simpler |
| JWT with shared secret | Stateless, fast | Token revocation is hard | Sessions provide better control |
| OAuth2 authorization code flow | Standard, secure | Complex for single-domain app | Simpler session-based auth is sufficient |

**Best practices identified**:
- Use short-lived access tokens (15-30 minutes)
- Implement refresh token rotation for long-lived sessions
- Invalidate sessions on password change
- Use different token scopes for different permission levels
- Monitor for token reuse anomalies

---

## Summary of Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Auth Provider | Better-Auth | Email/password + OAuth, session management, secure by default |
| Database ORM | SQLAlchemy | Python-native, flexible, good performance |
| Database | SQLite (dev) + Neon Postgres (prod) | Zero-config dev, scalable production |
| Password Hashing | bcrypt (via Better-Auth) | Industry standard, secure |
| Token Format | JWT + Session Cookies | Flexible, secure, Better-Auth native |
| Frontend Auth | React hooks + Better-Auth SDK | Reusable, Docusaurus-compatible |
| Personalization | HardwareContextService + prompt injection | Simple, testable, effective |
| Curriculum Tracking | Relational SQL table | Simple, queryable, validated |
| Hardware Forms | React dropdowns with PDF options | Ensures PDF compliance, validated |

---

## Open Questions (Resolved)

1. **Database location**: User data stored in separate tables from RAG data → Use same Neon Postgres instance, different schemas
2. **Session validation**: FastAPI validates via Better-Auth endpoint → Use shared JWT secret for performance
3. **Hardware profile schema**: JSONB column for flexibility → Allows PDF-specified hardware without migrations
4. **Chat history storage**: Separate tables with pagination → Prevents performance degradation as history grows
5. **PDF Page 8 logic**: Inference/Sim-to-Real prioritization → Implemented in HardwareContextService prompt injection
6. **Curriculum weeks**: Fixed 13-week structure → Enforced via CHECK constraint in database

---

## References

- Better-Auth Documentation: https://www.better-auth.com
- SQLAlchemy Core Tutorial: https://docs.sqlalchemy.org
- FastAPI Security Dependencies: https://fastapi.tiangolo.com/tutorial/security/
- Neon Serverless Postgres: https://neon.tech
- Grok API Documentation: https://x.ai/api
- PDF "Hardware Reality" Section: Page 5
- PDF "Inference/Sim-to-Real" Section: Page 8
