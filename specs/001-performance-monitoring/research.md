# Research & Discovery: Phase 4-5 Stability Layer

**Created**: 2026-03-18
**Feature**: Performance Monitoring Dashboard + Stability Layer
**Branch**: 001-performance-monitoring

---

## 1. Long-Running Job Tracking in FastAPI

### Decision: Use ReindexJob Model in PostgreSQL with Background Tasks

**What was chosen**: 
- Persist job state in PostgreSQL using existing ReindexJob model
- Use FastAPI's `BackgroundTasks` for async job execution
- Poll-based progress tracking (client polls status endpoint)

**Why chosen**:
- ✅ Persists across application restarts
- ✅ Leverages existing database infrastructure (no new dependencies)
- ✅ ReindexJob model already exists with proper schema
- ✅ Simple to implement and test
- ✅ Compatible with existing auth and admin patterns

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Redis for job state | Fast, built-in expiry | New dependency, infrastructure | Overkill for MVP, adds complexity |
| In-memory tracking | Simple, no dependencies | Lost on restart, no persistence | Unreliable for long operations |
| Celery task queue | Robust, distributed | Heavy dependency, over-engineering | Unnecessary for single-server deployment |
| WebSockets for push | Real-time updates | Complex connection management | Polling sufficient for admin dashboard |

**Implementation Pattern**:
```python
# In ReindexService
async def start_reindex(self, user: User) -> ReindexJob:
    job = ReindexJob(
        status="queued",
        total_files=await self.count_files(),
        created_by_user_id=user.id
    )
    self.db.add(job)
    self.db.commit()
    
    # Run in background
    background_tasks.add_task(self._run_reindex, job.id)
    return job
```

---

## 2. RAG Pipeline Instrumentation

### Decision: Service-Level Timing with Context Managers

**What was chosen**:
- Add timing instrumentation directly in RAG pipeline service
- Use context managers for clean timing blocks
- Log each step with structured logging (step name, duration, metadata)
- Store metrics in PerformanceMonitor singleton

**Why chosen**:
- ✅ Minimal code changes to existing pipeline
- ✅ Precise control over what gets timed
- ✅ No middleware complexity
- ✅ Easy to extend with new steps
- ✅ Compatible with existing PerformanceMonitor service

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Middleware timing | Automatic, all endpoints | Can't distinguish RAG steps | Too coarse-grained |
| Decorator-based | Reusable, clean | Requires refactoring all methods | More invasive |
| AOP/aspect-oriented | Separation of concerns | Complex setup, new dependencies | Over-engineering |
| OpenTelemetry | Industry standard, tracing | Heavy, requires OTel setup | Overkill for MVP |

**Implementation Pattern**:
```python
# In RAG pipeline
async def generate_response(self, query: str, user_id: str) -> str:
    # Time embedding step
    with self.timing_context("embedding"):
        query_embedding = await self.embedder.embed(query)
    
    # Time search step
    with self.timing_context("search"):
        results = await self.qdrant.search(query_embedding)
    
    # Time context assembly
    with self.timing_context("context_assembly"):
        context = self.assemble_context(results)
    
    # Time LLM call
    with self.timing_context("llm_call"):
        response = await self.grok_client.chat(query, context)
    
    return response

@contextmanager
def timing_context(self, step_name: str):
    start = time.time()
    try:
        yield
    finally:
        duration_ms = (time.time() - start) * 1000
        self.monitor.record_step_latency(step_name, duration_ms)
```

**RAG Steps to Track**:
1. **Embedding**: Time to generate query embedding (fastembed model)
2. **Search**: Time for Qdrant vector search
3. **Context Assembly**: Time to format retrieved documents
4. **LLM Call**: Time for Grok API response (includes network latency)

---

## 3. Health Check Patterns

### Decision: On-Demand Health Checks with Client-Side Caching

**What was chosen**:
- Health checks run on-demand when status endpoint is called
- Each service (PostgreSQL, Qdrant, Grok API) checked independently
- Response includes status (healthy/unhealthy) and response time
- Frontend caches results for 30 seconds to reduce load

**Why chosen**:
- ✅ Simple to implement and test
- ✅ Always returns current state
- ✅ No background processes needed
- ✅ Frontend controls refresh frequency
- ✅ Clear failure isolation (each service independent)

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Background polling | Always fresh data | Wastes resources when no one viewing | Inefficient for admin-only feature |
| Hybrid (background + on-demand) | Best of both | More complex state management | Unnecessary for MVP |
| Event-driven health checks | Reactive | Complex event system | Over-engineering |

**Health Check Implementation**:
```python
# PostgreSQL health
async def check_postgresql_health() -> HealthStatus:
    start = time.time()
    try:
        await db.execute("SELECT 1")
        response_time = (time.time() - start) * 1000
        return HealthStatus(status="healthy", response_time_ms=response_time)
    except Exception as e:
        return HealthStatus(status="unhealthy", error=str(e))

# Qdrant health
async def check_qdrant_health() -> HealthStatus:
    start = time.time()
    try:
        await qdrant_client.get_collection(collection_name)
        response_time = (time.time() - start) * 1000
        return HealthStatus(status="healthy", response_time_ms=response_time)
    except Exception as e:
        return HealthStatus(status="unhealthy", error=str(e))

# Grok API health
async def check_grok_health() -> HealthStatus:
    start = time.time()
    try:
        # Lightweight API call (not actual chat, just auth check)
        await grok_client.list_models()
        response_time = (time.time() - start) * 1000
        return HealthStatus(status="healthy", response_time_ms=response_time)
    except Exception as e:
        return HealthStatus(status="unhealthy", error=str(e))
```

**Frontend Caching Strategy**:
```typescript
// In frontend service
const HEALTH_CACHE_TTL = 30000; // 30 seconds

let healthCache: { data: HealthData; timestamp: number } | null = null;

async function getHealthStatus(): Promise<HealthData> {
  if (healthCache && Date.now() - healthCache.timestamp < HEALTH_CACHE_TTL) {
    return healthCache.data;
  }
  
  const response = await fetch('/api/admin/health');
  const data = await response.json();
  healthCache = { data, timestamp: Date.now() };
  return data;
}
```

---

## 4. Rate Limiting for Heavy Operations

### Decision: Per-User Rate Limiting with Sliding Window

**What was chosen**:
- Rate limit re-indexing to 10 operations per minute per admin user
- Use existing `upload_limiter` pattern from IngestionService
- Return 429 Too Many Requests with retry-after header
- Log rate limit violations for security monitoring

**Why chosen**:
- ✅ Consistent with existing rate limiting patterns
- ✅ Per-user prevents single user from monopolizing resources
- ✅ Sliding window is fair and predictable
- ✅ Easy to adjust limits based on monitoring
- ✅ No new dependencies (uses existing middleware)

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Global rate limit | Simpler | One user can starve others | Unfair in multi-admin scenarios |
| IP-based limiting | Network-level | Doesn't work with NAT/proxies | Less precise than user-based |
| Token bucket | Smooths bursts | More complex state | Sliding window sufficient |
| No rate limiting | Simplest | Risk of server overload | Unacceptable for heavy operation |

**Rate Limiter Implementation**:
```python
# In middleware/rate_limiter.py
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = {}
    
    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        
        if user_id not in self.requests:
            self.requests[user_id] = deque()
        
        # Remove old requests outside window
        while self.requests[user_id] and self.requests[user_id][0] < window_start:
            self.requests[user_id].popleft()
        
        # Check if under limit
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        
        return False
    
    def get_remaining(self, user_id: str) -> int:
        # Return remaining requests in current window
        ...

# Usage in admin endpoint
reindex_limiter = RateLimiter(max_requests=10, window_seconds=60)

@router.post("/reindex")
async def trigger_reindex(
    request: Request,
    current_user: User = Depends(get_current_admin_user)
):
    if not reindex_limiter.is_allowed(current_user.id):
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": "Too many re-index operations",
                "retry_after_seconds": 60
            }
        )
    # Proceed with re-indexing
```

**Security Considerations**:
- Log all rate limit violations with user ID and timestamp
- Consider alerting on repeated violations (potential abuse)
- Document rate limits in API documentation
- Consider different limits for different admin roles (super-admin vs regular admin)

---

## Summary of Decisions

| Unknown | Decision | Key Rationale |
|---------|----------|---------------|
| Job Tracking | PostgreSQL + BackgroundTasks | Uses existing infra, persistent, simple |
| RAG Timing | Service-level context managers | Precise, minimal changes, extensible |
| Health Checks | On-demand with 30s cache | Simple, current data, no background processes |
| Rate Limiting | Per-user sliding window | Fair, consistent with existing, no new deps |

---

## Next Steps

1. **Create data-model.md**: Document ReindexJob model and any new entities
2. **Create API contracts**: Write OpenAPI specs for new endpoints
3. **Create quickstart.md**: Developer setup guide
4. **Update agent context**: Add new technologies to agent-specific context file

**All NEEDS CLARIFICATION items resolved** ✅
