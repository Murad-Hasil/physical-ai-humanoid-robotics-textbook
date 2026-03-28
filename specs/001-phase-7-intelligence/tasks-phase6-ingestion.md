# Tasks: Phase 7 - Content Ingestion & Vector Sync (Phase 6)

**Input**: Design documents from `/specs/001-phase-7-intelligence/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)
**Previous Work**: Phases 1-5 complete (Setup, Foundational, Onboarding, Personalization, Translation)

**Tests**: Tests are OPTIONAL for this feature. Not included in this task list. Add manually if TDD approach is desired.

**Organization**: Tasks are grouped by User Story 4 (Curriculum Content Access).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **Frontend**: `docusaurus-textbook/` at repository root
- **Docs**: `docusaurus-textbook/docs/` for curriculum content
- Paths shown below are absolute from repository root

---

## Phase 1-5: Setup Through Translation (Already Complete ✓)

**Status**: All previous phases complete

---

## Phase 6: User Story 4 - Complete Curriculum Content Access (Priority: P4) 🎯

**Goal**: Ingest 13-week curriculum content into database and Qdrant vector store for RAG-powered access

**Independent Test**: Run ingestion script on week-1 markdown file, verify chapter appears in database, vectors in Qdrant, and query returns relevant results

### File Preparation

- [ ] T029 [P] [US4] Create `docusaurus-textbook/docs/week-01-foundations.md` with technical content:
  - Title: "Week 1: Foundations of Physical AI"
  - Include sections: Introduction, Chebychev-Grübler-Kutzbach criterion, DOF calculations
  - Add frontmatter: `week_number: 1`, `chapter_id: 'week-1'`, `tags: ['foundations', 'kinematics']`
  - Ensure markdown formatting is clean for Docusaurus rendering
  - Include code examples and diagrams where appropriate

- [ ] T030 [P] [US4] Create `docusaurus-textbook/docs/_category_.json` for week 1:
  - Set `label: "Week 1: Foundations"`
  - Set `position: 1`
  - Set `link: type: 'generated-index'`
  - Configure sidebar display options

### Ingestion Service Implementation

- [ ] T031 [P] [US4] Implement `CurriculumService.ingest_chapter()` in `backend/services/curriculum_service.py`:
  - Accept markdown file path and metadata
  - Parse frontmatter to extract chapter_id, title, tags
  - Create or update Chapter record in PostgreSQL
  - Return chapter_id for vector sync
  - Add error handling for duplicate chapters

- [ ] T032 [P] [US4] Implement metadata extraction in `backend/services/curriculum_service.py`:
  - Extract `chapter_id` from frontmatter or filename
  - Extract `title` from frontmatter or first H1 header
  - Extract `tags` array from frontmatter
  - Extract `estimated_time` if provided
  - Default `hardware_relevant` to ['sim_rig', 'edge_kit']

- [ ] T033 [P] [US4] Add content chunking logic in `backend/services/ingestion_service.py`:
  - Split markdown into logical chunks by H2/H3 headers
  - Preserve context from parent sections
  - Limit chunk size to 512 tokens for embedding
  - Add overlap between chunks for context continuity
  - Return list of chunks with metadata

### Vector Sync with Qdrant

- [ ] T034 [P] [US4] Implement `QdrantService.ingest_chapter()` in `backend/retrieval/qdrant_service.py`:
  - Accept chapter content and metadata
  - Generate embeddings using Sentence Transformers
  - Upsert vectors into `physical-ai-knowledge-base` collection
  - Store metadata: chapter_id, week_number, tags, hardware_relevant
  - Return number of vectors ingested

- [ ] T035 [P] [US4] Add embedding generation in `backend/retrieval/qdrant_service.py`:
  - Use `sentence-transformers/all-MiniLM-L6-v2` model
  - Generate embeddings for each content chunk
  - Batch embeddings for efficient upsert (batch_size=32)
  - Handle rate limiting with retry logic
  - Log embedding statistics

- [ ] T036 [P] [US4] Implement Qdrant collection verification in `backend/retrieval/qdrant_service.py`:
  - Check if `physical-ai-knowledge-base` collection exists
  - Create collection if not exists with correct schema
  - Configure vector size (384 for MiniLM)
  - Set distance metric (COSINE)
  - Add metadata indexes

### Ingestion Logging & Verification

- [ ] T037 [P] [US4] Log ingestion to `IngestionLog` table in `backend/services/ingestion_service.py`:
  - Record chapter_id, status ('success' or 'failed')
  - Log number of chunks ingested
  - Log number of vectors upserted to Qdrant
  - Record ingestion timestamp
  - Add error messages if failed

- [ ] T038 [P] [US4] Create ingestion verification script `backend/scripts/verify_ingestion.py`:
  - Query IngestionLog for recent ingestions
  - Verify chapter exists in database
  - Verify vectors exist in Qdrant (query by chapter_id)
  - Display ingestion statistics
  - Return exit code 0 if successful, 1 if failed

### Testing & Validation

- [ ] T039 [US4] Test sample query via backend in `backend/tests/ingestion/test_query.py`:
  - Query: "What is the Chebychev-Grübler-Kutzbach criterion?"
  - Verify relevant chapter chunks are returned
  - Verify RAG context includes correct metadata
  - Test with different hardware profiles
  - Log query results for review

- [ ] T040 [US4] Test Docusaurus rendering in `docusaurus-textbook/docs/week-01-foundations.md`:
  - Start Docusaurus dev server: `npm run start`
  - Navigate to week-1 chapter
  - Verify markdown renders correctly
  - Verify code blocks are syntax-highlighted
  - Verify images/diagrams display
  - Verify sidebar navigation works

### Batch Ingestion for All Weeks

- [ ] T041 [P] [US4] Create batch ingestion script `backend/scripts/ingest_all_weeks.py`:
  - Iterate through `docusaurus-textbook/docs/week-*.md` files
  - Call CurriculumService.ingest_chapter() for each
  - Call QdrantService.ingest_chapter() for vector sync
  - Log progress with chapter count
  - Handle errors gracefully (continue on failure)
  - Display summary: X chapters ingested, Y vectors upserted

- [ ] T042 [P] [US4] Create curriculum folder structure for weeks 2-13:
  - Create `docusaurus-textbook/docs/week-02-*.md` through `week-13-*.md`
  - Create `_category_.json` for each week
  - Add placeholder content with frontmatter
  - Configure sidebar ordering

- [ ] T043 [US4] Run full ingestion for all 13 weeks:
  - Execute: `python backend/scripts/ingest_all_weeks.py`
  - Monitor logs for errors
  - Verify all chapters in database
  - Verify all vectors in Qdrant
  - Run sample queries for each week
  - Document any failures and retry

### Frontend Integration

- [ ] T044 [US4] Update Docusaurus sidebar in `docusaurus-textbook/sidebars.ts`:
  - Add curriculum section with all 13 weeks
  - Configure category links for each week
  - Set proper ordering (week 1 through week 13)
  - Test sidebar navigation
  - Verify mobile responsiveness

- [ ] T045 [US4] Add curriculum overview page in `docusaurus-textbook/docs/curriculum-overview.md`:
  - List all 13 weeks with descriptions
  - Add learning objectives for each week
  - Include prerequisites and dependencies
  - Link to individual week pages
  - Add estimated completion time

**Checkpoint**: User Story 4 complete - all 13 weeks ingested, vectors synced, queries return relevant results, curriculum accessible in Docusaurus

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final polish and validation

- [ ] T046 [P] Add ingestion monitoring dashboard in `backend/api/admin.py`:
  - GET endpoint for ingestion statistics
  - Display total chapters, vectors, last ingestion time
  - Show failures and retry options
  - Admin-only access

- [ ] T047 [P] Add re-ingestion endpoint in `backend/api/v1/endpoints/curriculum.py`:
  - POST `/chapters/{chapter_id}/reingest` (admin-only)
  - Re-run ingestion for specific chapter
  - Invalidate old vectors in Qdrant
  - Log re-ingestion attempt

- [ ] T048 [P] Performance optimization in `backend/retrieval/qdrant_service.py`:
  - Add batch processing for large chapters
  - Implement parallel embedding generation
  - Add progress callbacks for long-running ingestions
  - Optimize Qdrant upsert operations

- [ ] T049 [P] Documentation updates in `docs/ingestion/`:
  - Document ingestion process
  - Add troubleshooting guide
  - Document Qdrant collection schema
  - Add query examples

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phases 1-5**: ✅ Already complete
- **Phase 6 (US4)**: Can start immediately - depends on Curriculum and Translation tables existing
- **Phase 7 (Polish)**: Depends on Phase 6 completion

### Within Phase 6

- File preparation (T029-T030) before ingestion
- Service implementation (T031-T033) before vector sync
- Vector sync (T034-T036) before verification
- Verification (T037-T038) before testing
- Testing (T039-T040) before batch ingestion
- Batch ingestion (T041-T043) before frontend integration

### Parallel Opportunities

**File Preparation**:
- T029 (week-1 content), T030 (category JSON) can run in parallel

**Service Implementation**:
- T031 (ingest_chapter), T032 (metadata extraction), T033 (chunking) can run in parallel

**Vector Sync**:
- T034 (Qdrant ingest), T035 (embeddings), T036 (collection verification) can run in parallel

**Testing**:
- T039 (query test) and T040 (Docusaurus rendering) can run in parallel

---

## Parallel Example: Phase 6 (User Story 4)

```bash
# Launch all file preparation tasks together:
Task: "T029 [P] [US4] Create week-1 markdown content"
Task: "T030 [P] [US4] Create category JSON"

# Launch all service tasks together:
Task: "T031 [P] [US4] Implement CurriculumService.ingest_chapter()"
Task: "T032 [P] [US4] Implement metadata extraction"
Task: "T033 [P] [US4] Implement content chunking"

# Launch all vector sync tasks together:
Task: "T034 [P] [US4] Implement QdrantService.ingest_chapter()"
Task: "T035 [P] [US4] Implement embedding generation"
Task: "T036 [P] [US4] Implement collection verification"
```

---

## Implementation Strategy

### MVP First (Week 1 Only)

1. Complete T029-T030: Create week-1 content files
2. Complete T031-T033: Implement ingestion service
3. Complete T034-T036: Sync vectors to Qdrant
4. Complete T037-T038: Verify ingestion
5. **STOP and VALIDATE**: Test query "What is the Chebychev-Grübler-Kutzbach criterion?"
6. Deploy/demo if ready

### Incremental Delivery

1. Ingest Week 1 → Test query → Deploy
2. Ingest Weeks 2-5 → Test navigation → Deploy
3. Ingest Weeks 6-10 → Test personalization → Deploy
4. Ingest Weeks 11-13 → Test full curriculum → Deploy
5. Each increment adds value without breaking previous work

---

## Task Summary

**Total Tasks**: 21 tasks (Phase 6-7 only)

**By Phase**:
- Phase 6 (US4 - Content Ingestion): 17 tasks
- Phase 7 (Polish): 4 tasks

**Parallelizable Tasks**: 13 tasks marked with [P]

**MVP Scope** (Week 1 ingestion only): 8 tasks (T029-T036)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- User Story 4 is independently completable and testable
- Commit after each task or logical group of 2-3 tasks
- Stop at checkpoints to validate ingestion independently
- Verify Qdrant collection exists before upserting vectors
- Log all ingestion attempts for debugging
- Test queries with known answers to verify RAG accuracy
