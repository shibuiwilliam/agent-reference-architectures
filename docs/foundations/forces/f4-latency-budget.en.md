---
title: "[F4] Latency Budget"
tags:
  - "Driving Variables"
---

# [F4] Latency Budget

!!! abstract "Summary"
    A force that measures how long the user can wait. The smaller the budget, the more synchronous processing, caching, and lightweight models are required; the larger it is, the more you can invest in quality.

## Overview

If you need to show autocomplete suggestions as a user types each character, you must respond within 100ms. But for a weekly research report, having it ready by the next morning is sufficient. This range of "how long can they wait" fundamentally determines the available architecture choices.

Latency budget represents the length of time a user will tolerate from request issuance to result receipt.

## Why It Matters

Misjudging the latency budget means either users abandon while waiting for results, or the system unnecessarily sacrifices quality. LLM calls take hundreds of milliseconds to tens of seconds, so many cases do not fit within synchronous HTTP boundaries. Budget overruns lead directly to HTTP timeouts, connection drops, and user experience collapse.

## Interpreting the Value Range

### When Low

Situations requiring immediate response (100ms to a few seconds). Examples include search suggestions, single-turn chat responses, and real-time classification/filtering. Raw LLM calls often cannot meet the timeline, requiring caching, lightweight models, streaming output, or fallback to non-LLM traditional methods.

### When High

Situations tolerating waits of minutes to hours. Typical examples include research report generation, codebase-wide refactoring, and large-scale data analysis. These can be accepted as asynchronous jobs, with progress notifications sent while processing runs in the background. Budget can be allocated to multi-step reasoning and ensembles for quality improvement.

## Evaluation Guidelines

- Does the user wait for results in a UI, or receive a completion notification in the background?
- What response time is currently tolerated for similar features?
- Can streaming intermediate results during processing reduce perceived wait time?
- What are the timeout settings on the load balancer or API gateway?
- Are response time upper limits defined in SLAs or SLOs?

## Influenced Design Decisions

### Related Dials

- [Timeout](../../decisions/dials/timeout.md) -- Set per-request timeout according to the latency budget
- [Model Tier Routing](../../decisions/dials/model-tier-routing.md) -- Route to lightweight, fast models when the budget is small
- [Cache Similarity](../../decisions/dials/cache-similarity.md) -- Increase cache hit rate for faster response when the budget is small
- [Retry Count](../../decisions/dials/retry-count.md) -- Set retry count upper limits that fit within the budget

### Related Tradeoffs

- [Sync vs. Async](../../decisions/tradeoffs-catalog/sync-vs-async.md) -- Async is essential when the budget exceeds LLM processing time
- [Fail-Fast vs. Degradation](../../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) -- When the budget cannot be met, fail immediately or return degraded-quality results
- [Push vs. Pull](../../decisions/tradeoffs-catalog/push-vs-pull.md) -- Choose the progress notification method for async processing based on budget and connection environment

## Related Patterns

- [#1 Request-to-Job Gateway](../../decisions/tradeoffs-catalog/sync-vs-async.md) -- Accept requests that exceed the budget as asynchronous jobs
- [#7 Streaming Progress](../../decisions/tradeoffs-catalog/push-vs-pull.md) -- Stream progress during processing to reduce perceived wait time
- [#58 Sync Facade over Async Core](../../decisions/tradeoffs-catalog/sync-vs-async.md) -- Respond synchronously if fast enough, promote to async otherwise
- [#38 Semantic Result Cache](../../decisions/dials/cache-similarity.md) -- Reuse semantically similar past results to reduce latency
- [#39 Prompt Cache Optimized Context](../../foundations/forces/f7-cost-sensitivity.md) -- Leverage prompt cache via common prefixes
