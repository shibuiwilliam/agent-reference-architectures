---
title: "Timeout (Per Request)"
tags:
  - "Tuning Dial"
  - "F4 Latency Budget"
---

# Timeout (Per Request)

!!! abstract "TL;DR"
    Determine the maximum wait time allowed for a single request, balancing between connection occupation and premature termination.

## Overview

One day, an agent's response suddenly stops coming back. Upon investigation, the request was being cut off mid-process by a load balancer timeout -- timeout-related incidents are common in production environments.

This dial controls how much wait time is tolerated for a single request. Since synchronous APIs and asynchronous jobs differ by orders of magnitude, settings must be configured per pathway. Too short, and normal processing gets interrupted; too long, and connection pools or threads get occupied, causing the entire system to stall.

## Why Adjustment Is Needed

Default values (30 seconds for frameworks, 60 seconds for infrastructure) are often too short for agent processing that includes LLM calls. On the other hand, extending timeouts indefinitely exhausts connections behind the load balancer, causing all subsequent requests to fail. In production, unless you set timeouts based on "95th percentile of normal operation + margin," you will end up with either sporadic timeout errors or resource exhaustion.

## Extremes of the Range

### Too Small

Requests are terminated before the LLM inference or tool calls complete. Users receive errors, and tokens partially consumed on the server side go to waste. Cascading retries further increase load, creating a vicious cycle.

### Too Large

A single request occupies a connection for an extended period, reaching the concurrent connection limit. During outages, slow queries accumulate with no backpressure, causing the entire system to hang. On the client side, the UI appears frozen, significantly degrading user experience.

## Determining Forces

- `[F4]` Latency Budget -- The shorter the user's tolerance for waiting, the shorter the timeout must be, but large gaps between the timeout and actual agent processing time reduce success rates

## Guidelines (Starting Point)

- Synchronous API: 5-10 seconds (time to start streaming)
- Asynchronous jobs: 5-30 minutes (depending on task complexity)
- Gateway layer: Client-facing timeout < Backend-facing timeout (maintain margin)
- Single LLM API call: 30-120 seconds (depending on model and prompt length)

## Practical Adjustment

- Measure production latency distribution (p50/p95/p99) and set the initial timeout to p99 + 20%
- If synchronous pathways cannot accommodate, consider async promotion patterns with two-tier timeouts
- Set timeout occurrence rate as an alert target; when the threshold is exceeded, review the value or split the processing
- Align timeouts across load balancer, API Gateway, and application layers to prevent zombie requests from misalignment

## Related Patterns

- [#1 Request-to-Job Gateway](../../glossary.md) -- Entry point for switching requests that exceed synchronous timeouts to asynchronous jobs
- [#5 Time-Budgeted Agent Loop](../../glossary.md) -- Internalizes timeouts as budgets within the agent loop
