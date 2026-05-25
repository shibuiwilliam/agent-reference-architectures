---
title: "[C2] Long and Variable Duration Execution"
tags:
  - "Characteristics"
---

# [C2] Long and Variable Duration Execution

!!! abstract "Summary"
    Processing time swings from seconds to tens of minutes and cannot be predicted in advance -- assumptions about HTTP timeouts and resource allocation break down.

## Overview

Traditional APIs have nearly constant processing times, allowing fixed timeout values. AI agents have execution times that vary by orders of magnitude depending on the number of reasoning steps and chains of tool calls. "Simple questions take 2 seconds, research tasks take 15 minutes" can happen on the same endpoint.

## Why This Is a Problem

Long-running tasks get cut off by load balancer or API Gateway timeouts (typically 30--60 seconds). The client receives no result, yet the agent continues running on the server side consuming resources. In multi-tenant environments, one tenant's long-running task monopolizes the worker pool, degrading response times for other tenants. Auto-scalers misjudge scaling decisions when processing time variance is large, swinging between over-provisioning and resource exhaustion. Users are left waiting with no progress visibility and reload the browser, triggering duplicate executions.

## Comparison with Traditional Software

| Aspect | Traditional Software | AI Agent |
|--------|---------------------|----------|
| Processing time | Nearly constant (P99 also predictable) | Seconds to tens of minutes (varies by orders of magnitude) |
| Timeout design | Fixed values are sufficient | Fixed values are either too short or too long |
| Resource planning | Estimated by QPS x average processing time | Worker occupancy time is unpredictable due to variable step counts |
| User experience | Loading indicator is sufficient | Progress streaming is required |

## Affected Forces

- `[F4]` Latency Budget -- The lower the user's tolerance for waiting, the more important async processing and progress notifications become
- `[F7]` Cost Sensitivity & Scale -- Worker occupancy time variability directly impacts infrastructure costs
- `[F1]` Reversibility -- When long-running execution fails mid-way, recovery from intermediate state is needed

## Safeguard Patterns

- [#1 Request-to-Job Gateway](../../patterns/01-execution/01-request-to-job-gateway.md) -- Decouple from synchronous HTTP and execute as an asynchronous job
- [#5 Time-Budgeted Agent Loop](../../patterns/01-execution/05-time-budgeted-agent-loop.md) -- Set budgets for time, iterations, and cost to prevent runaway execution
- [#6 Interruptible Agent](../../patterns/01-execution/06-interruptible-agent.md) -- Structure the agent so it can be stopped mid-execution and course-corrected

## Related Design Decisions

- [timeout](../../decisions/dials/timeout.md) -- Where to set the timeout value. Too short and legitimate tasks fail
- [budget-cap](../../decisions/dials/budget-cap.md) -- Where to draw the time/cost budget ceiling
- [sync vs. async](../../decisions/tradeoffs-catalog/sync-vs-async.md) -- Respond synchronously or switch to an asynchronous job
