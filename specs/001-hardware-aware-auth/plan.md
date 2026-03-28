# Implementation Plan: Hardware-Aware Authentication and Personalization

**Branch**: `001-hardware-aware-auth` | **Date**: 2026-03-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-hardware-aware-auth/spec.md`

## Summary

Implement student authentication using Better-Auth with email/password and GitHub OAuth providers, create user profile schemas for PDF-specified hardware configurations (RTX 4070 Ti, Jetson Orin, Unitree robots), protect FastAPI endpoints with authentication middleware, build a context injection service that prepends hardware constraints to Grok API prompts based on PDF "Hardware Reality" (Page 5) and Page 8 "Inference/Sim-to-Real" logic, track 13-week curriculum progress, and provide Docusaurus frontend components for auth state management and hardware setup forms.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript ES2022/TypeScript (frontend)
**Primary Dependencies**: FastAPI, Better-Auth, SQLAlchemy, Grok API (xAI), React 18+
**Storage**: SQLite (development), PostgreSQL (production via Neon Serverless)
**Testing**: pytest (backend), React Testing Library (frontend)
**Target Platform**: Linux server (backend), Web browser (Docusaurus frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Authentication <2s p95, chat response <3s with personalization, chat history retrieval <2s for 100 conversations, hardware context injection <100ms overhead
**Constraints**: Secure password hashing (bcrypt/argon2), JWT/session tokens with secure cookies, hardware context must not override textbook technical steps, PDF Page 5 "Hardware Reality" and Page 8 "Inference/Sim-to-Real" must be prioritized in prompts
**Scale/Scope**: 10k concurrent students, auth system supporting email/password + GitHub OAuth, hardware profiles with JSON fields for PDF-specified configurations, 13-week curriculum tracking

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Justification |
|------|--------|---------------|
| **Sequential Phase Execution** | ✅ PASS | This is Phase 3 work, Phase 1 (Docusaurus) and Phase 2 (RAG backend) are complete |
| **Workflow Integrity** | ✅ PASS | Following sequence: spec (completed) → plan (current) → tasks → implement |
| **Contract Adherence** | ✅ PASS | Plan stays within spec boundaries: auth, PDF hardware profiles, hardware-aware responses, curriculum tracking, no scope expansion |
| **Tooling Constraints** | ✅ PASS | No modifications to `.specify/`, `.claude/`, or `.qwen/` internal files |
| **Phase Completion Gates** | ✅ PASS | Will deliver working auth system with PDF-based hardware personalization as standalone milestone |

## Project Structure

### Documentation (this feature)

```text
specs/001-hardware-aware-auth/
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
├── auth/
│   ├── __init__.py
│   ├── better_auth_config.py      # Better-Auth configuration
│   ├── session_validator.py       # Session validation logic
│   └── middleware.py              # FastAPI auth middleware
├── models/
│   ├── __init__.py
│   ├── user.py                    # User model (extends Better-Auth)
│   ├── student_profile.py         # StudentProfile model
│   ├── hardware_config.py         # HardwareConfig model (PDF-specified)
│   └── curriculum_progress.py     # CurriculumProgress model (Weeks 1-13)
├── services/
│   ├── __init__.py
│   ├── hardware_context_service.py # Context injection service
│   ├── rag_pipeline.py            # RAG pipeline (existing, modified)
│   └── grok_client.py             # Grok API client (existing, modified)
├── api/
│   ├── __init__.py
│   ├── auth.py                    # Auth endpoints (login, register, logout)
│   ├── user.py                    # User profile endpoints
│   ├── hardware.py                # Hardware profile endpoints
│   ├── curriculum.py              # Curriculum progress endpoints
│   └── chat.py                    # Chat endpoint (modified with personalization)
├── utils/
│   ├── __init__.py
│   └── pdf_hardware_constants.py  # PDF Page 5 hardware constants
└── tests/
    ├── unit/
    │   ├── test_auth.py
    │   ├── test_hardware_context_service.py
    │   └── test_curriculum_progress.py
    └── integration/
        ├── test_chat_personalization.py
        └── test_protected_endpoints.py

docusaurus-textbook/
├── src/
│   ├── components/
│   │   ├── LoginButton.jsx        # Auth button component
│   │   ├── HardwareProfileForm.jsx # Hardware setup form
│   │   ├── CurriculumProgress.jsx  # Progress tracker component
│   │   └── ChatHistory.jsx         # Chat history viewer
│   ├── hooks/
│   │   ├── useAuth.js             # Auth state hook
│   │   └── useHardwareProfile.js  # Hardware profile hook
│   └── pages/
│       ├── profile.jsx            # User profile page
│       └── progress.jsx           # Curriculum progress page
└── src/theme/
    └── Root.js                    # Auth provider wrapper
```

**Structure Decision**: Web application structure with backend (FastAPI + Better-Auth) and frontend (Docusaurus + React). All auth-specific logic isolated in `/backend/auth` directory. Hardware-aware personalization logic in `/backend/services/hardware_context_service.py`. Frontend components for hardware setup and curriculum tracking in Docusaurus `src/components/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitution gates passed.

## Constitution Check (Post-Design Re-evaluation)

*Re-evaluated after Phase 1 design completion.*

| Gate | Status | Justification |
|------|--------|---------------|
| **Sequential Phase Execution** | ✅ PASS | Design documents (research.md, data-model.md, contracts, quickstart.md) completed before implementation |
| **Workflow Integrity** | ✅ PASS | Following sequence: spec → plan (current) → tasks → implement. All artifacts generated. |
| **Contract Adherence** | ✅ PASS | Design stays within spec boundaries: Better-Auth, PDF hardware profiles, hardware-aware RAG, curriculum tracking (Weeks 1-13). No scope expansion. |
| **Tooling Constraints** | ✅ PASS | No modifications to `.specify/`, `.claude/`, or `.qwen/` internal files. QWEN.md updated only to add Active Technologies section. |
| **Phase Completion Gates** | ✅ PASS | Design delivers working auth system with PDF-based hardware personalization. All Phase 1 artifacts complete: research.md, data-model.md, contracts/api-contracts.yaml, quickstart.md. |
