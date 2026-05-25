---
title: "All Sync / All Async"
tags:
  - "Anti-Pattern"
  - "Tradeoff Mis-selection"
---

# 7. All Sync / All Async

!!! abstract "TL;DR"
    An anti-pattern where sync/async processing is uniformly standardized, sacrificing either the UX of short requests or the reliability of long requests.

## Common Scenario

A team building an agent API chose to process all requests via synchronous HTTP "to keep things simple." Initially, requests completed in a few seconds, but as long-running tasks like document analysis and code generation were added, requests exceeding 30 seconds became common. Load balancer timeouts disconnected connections mid-processing.

Meanwhile, another team learned from this and designed all requests to go through an async job queue. However, even instantly answerable questions like "What's the weather today?" had to travel through job queue -> worker -> polling, adding 2-3 seconds of latency. The chat UI experience degraded significantly.

## Symptoms

- **All sync**: Long-running requests time out, and clients resend, causing duplicate processing
- **All sync**: Worker threads are held by long-running requests, making even short requests wait
- **All async**: Instantly answerable requests incur unnecessary latency
- **All async**: Polling or webhook implementation costs are imposed on all requests
- In either case, the system cannot accommodate diverse processing times, leaving some users dissatisfied

## Root Cause

The processing model is decided uniformly at design time without dynamic per-request decisions. `[F4]` latency budget varies by request type, and ignoring this diversity by making "everything the same" inevitably causes problems at one extreme or the other.

Also, hybrid sync/async architectures are more complex to implement, so the temptation exists that "standardizing on one approach" keeps the architecture simpler and easier to manage.

## Detection Methods

- **Bimodal latency distribution**: A large gap between P50 and P99 indicates a mix of short and long requests
- **Timeout rate**: Check whether timeouts are occurring in synchronous processing
- **Unnecessary wait time**: Check whether instantly answerable request response times are dominated by infrastructure overhead
- **Metrics**: `request_duration_p50` vs `request_duration_p99`, `timeout_rate`, `queue_wait_time`

## Countermeasures

### Step 1: Predict and classify request processing time

Predict processing time from request type and input size, and classify into "short (within seconds)" and "long (tens of seconds or more)."

### Step 2: Introduce a hybrid architecture

Respond immediately for short requests via sync, and promote long requests to async jobs. Provide a mechanism to notify clients of progress.

### Step 3: Tune the promotion threshold

Set the sync-to-async promotion threshold based on `[F4]` latency budget and optimize through monitoring.

```python
# Hybrid processing example
async def handle_request(request):
    estimated_time = estimate_processing_time(request)

    if estimated_time < SYNC_THRESHOLD:  # e.g., 5 seconds
        # Sync processing: immediate response
        return await process_sync(request)
    else:
        # Promote to async: return job ID
        job_id = await enqueue_job(request)
        return {"status": "processing", "job_id": job_id}
```

## Examples

### Before (problematic state)

```python
# Pattern A: All sync — long requests time out
@app.post("/agent")
def handle(request):
    result = agent.run(request.prompt)  # 5 seconds to 5 minutes
    return result  # Load balancer times out at 30 seconds

# Pattern B: All async — short requests are slow
@app.post("/agent")
def handle(request):
    job_id = queue.enqueue(agent.run, request.prompt)
    return {"job_id": job_id}  # Even "What time is it?" takes 2 seconds
```

### After (improved)

```python
@app.post("/agent")
async def handle(request):
    estimated = estimate_duration(request)

    if estimated.seconds < 5:
        # Short request: sync immediate response
        result = await agent.run(request.prompt, timeout=10)
        return {"result": result}
    else:
        # Long request: promote to async
        job = await create_job(request.prompt, budget=estimated)
        return {"job_id": job.id, "poll_url": f"/jobs/{job.id}"}
```

## Related Anti-Patterns

- [Infinite / Excessive Timeout](01-infinite-timeout.md) — Timeout issues compound with all-sync processing
- [Retry Storm](09-retry-storm.md) — Sync timeouts trigger retries

## Related Patterns

- [#58 Sync Facade over Async Core](../patterns/01-execution/58-sync-facade-over-async-core.md) — Sync/async hybrid architecture
- [#1 Request-to-Job Gateway](../patterns/01-execution/01-request-to-job-gateway.md) — Separation of request intake and job management
- [#7 Streaming Progress](../patterns/01-execution/07-streaming-progress.md) — Progress notification for async processing
