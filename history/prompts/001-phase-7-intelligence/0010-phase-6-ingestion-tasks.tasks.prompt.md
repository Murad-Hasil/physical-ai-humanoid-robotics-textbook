---
id: 0010
title: phase-6-ingestion-tasks
stage: tasks
date: 2026-03-26
surface: agent
model: qwen-coder-plus
feature: 001-phase-7-intelligence
branch: 001-phase-7-intelligence
user: brownie
command: /sp.tasks Target: /phase-6-content-ingestion - File Preparation, Ingestion Execution, Vector Sync, Verification
labels: ["tasks","phase-7","content-ingestion","qdrant","vector-sync","curriculum","rag"]
links:
  spec: specs/001-phase-7-intelligence/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase-7-intelligence/tasks-phase6-ingestion.md
tests:
  - Task format validation (checkbox, ID, story labels, file paths)
  - User story independence verification
  - Ingestion workflow completeness check
tests_run:
  - Service layer dependency mapping
  - Qdrant integration verification
---

## Prompt

/sp.tasks
Target: /phase-6-content-ingestion

Instructions:
1. **File Preparation**:
   - [ ] Ensure `docs/week-1-foundations.md` exists with the provided technical content.
2. **Ingestion Execution**:
   - [ ] Run the `backend/services/ingestion_service.py` logic to parse the new Markdown file.
   - [ ] Extract metadata: `chapter_id='week-1'`, `title='Foundations of Physical AI'`.
3. **Vector Sync**:
   - [ ] Use `QdrantService` to generate embeddings for the chapter chunks.
   - [ ] Upsert the vectors into the `physical-ai-knowledge-base` collection.
4. **Verification**:
   - [ ] Verify that the `IngestionLog` table in PostgreSQL records a successful sync.
   - [ ] Test a sample query: "What is the Chebychev-Grübler-Kutzbach criterion?" via the backend.

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Response snapshot

Generated comprehensive tasks-phase6-ingestion.md with 21 tasks organized by User Story 4:

**Phase 6 (US4 - Content Ingestion)**: 17 tasks
- File preparation: Create week-1 markdown content with frontmatter, category JSON
- CurriculumService implementation: ingest_chapter(), metadata extraction, content chunking
- QdrantService implementation: ingest_chapter(), embedding generation, collection verification
- Ingestion logging: IngestionLog table integration, verification script
- Testing: Query testing with known questions, Docusaurus rendering verification
- Batch ingestion: Script for all 13 weeks, folder structure creation
- Frontend integration: Sidebar updates, curriculum overview page

**Phase 7 (Polish)**: 4 tasks
- Admin monitoring dashboard
- Re-ingestion endpoint
- Performance optimization
- Documentation updates

**Key Features**:
- 13 tasks marked [P] for parallel execution
- User Story 4 independently testable
- MVP scope defined (Week 1 ingestion = 8 tasks)
- Parallel execution opportunities identified
- Content chunking for optimal embedding (512 tokens)
- Batch processing for efficiency (batch_size=32)
- Verification script for quality assurance

**Technical Details**:
- Embedding model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- Qdrant collection: physical-ai-knowledge-base
- Distance metric: COSINE
- Chunk overlap for context continuity
- IngestionLog tracking for audit trail

## Outcome

- ✅ Impact: Actionable task list for content ingestion with clear file paths and dependencies
- 🧪 Tests: Task format validated, ingestion workflow verified for completeness
- 📁 Files: tasks-phase6-ingestion.md (21 tasks across 2 phases)
- 🔁 Next prompts: /sp.implement to begin Phase 6 ingestion
- 🧠 Reflection: Content ingestion critical for RAG functionality; vector sync ensures accurate query results

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated successfully with all design artifacts available
- Graders run and results (PASS/FAIL): PASS - task format validation confirmed all 21 tasks follow checklist format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with /sp.implement starting from file preparation (T029-T030)
