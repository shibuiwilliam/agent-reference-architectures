---
title: "Retry Count (Network)"
tags:
  - "Tuning Dial"
  - "F9 Provider Reliability"
---

# Retry Count (Network)

!!! abstract "TL;DR"
    Control the balance between automatic recovery from transient failures and failure amplification caused by retry storms.

## Overview

You call an LLM API and get a 503. You try again and it succeeds -- such transient failures are an everyday occurrence, but without a retry mechanism, every failure is visible to the user.

This dial determines how many times to automatically retry when LLM API or tool calls fail due to network errors or rate limiting. It must be designed in conjunction with a backoff strategy (exponential, jitter), not just the retry count alone. For agents that depend on external provider availability, this is one of the first items to tune.

## Why Adjustment Is Needed

LLM APIs frequently return 429 (rate limit) or 503 (overload). Without retries, transient failures become user-facing errors directly. However, too many retries cause a "retry storm" during outages, where all clients retry simultaneously and crush a service that was beginning to recover.

## Extremes of the Range

### Too Small

Failures are finalized immediately on transient 503s or network timeouts. LLM provider blips are not uncommon, and with zero retries, the perceived error rate can reach several percent. User trust erodes, and manual retries further increase load.

### Too Large

During prolonged outages, requests pile up, inflating cost (re-consumed tokens) and latency. Multiple executions of the same request risk duplicating side effects for non-idempotent tool calls. Immediate retries without backoff are especially dangerous.

## Determining Forces

- `[F9]` Provider Reliability -- The lower the external LLM's availability, the greater the need for retries, but the higher the storm risk as well

## Guidelines (Starting Point)

- Basic: 2-3 retries (with exponential backoff + jitter)
- Initial backoff: 1-2 seconds, maximum 30-60 seconds
- 429 responses: Respect the `Retry-After` header
- Non-idempotent operations: Insert a state check before retrying, or do not retry

## Practical Adjustment

- Visualize success rate including retries and the additional cost/latency caused by retries on a dashboard
- Combine with a circuit breaker to stop retries when consecutive failures exceed a threshold
- In multi-provider configurations, prioritize fallback switching over retrying the same provider
- Inject failures intentionally during load testing to confirm retry storms do not occur

## Related Patterns

- [#40 Fallback & Graceful Degradation](../../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) -- Provides alternative pathways after retry limits are reached
