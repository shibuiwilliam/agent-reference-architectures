---
title: "[C6] Dependency on External LLMs"
tags:
  - "Characteristics"
---

# [C6] Dependency on External LLMs

!!! abstract "Summary"
    The inference engine is an external service, and latency, availability, pricing, and behavior are outside your control.

## Overview

In traditional software, computation logic was confined to your own code and infrastructure. The "brain" of an AI agent -- the LLM -- depends on external APIs. Provider outages, rate limits, pricing changes, and model deprecations directly impact your production service. The situation where service quality changes without changing a single line of your own code can occur routinely.

## Why This Is a Problem

On a Friday night, the LLM provider has an outage and all agents stop. However, your monitoring only watches your own API returning HTTP 200, and you are slow to notice that "the LLM API is returning 504." When rate limits are hit, concentrated retries cause a cascade of timeouts. The provider updates the default model version without notice, and quality fluctuates. At month's end, token unit prices are revised, and costs far exceed projections. In multi-tenant SaaS, one tenant's heavy request volume exhausts the shared rate limit, affecting others.

## Comparison with Traditional Software

| Aspect | Traditional Software | AI Agent |
|--------|---------------------|----------|
| Location of computation logic | Own code, own infrastructure | External API (vendor-dependent) |
| Outage control | Redundancy/failover decided internally | Must wait for provider recovery |
| Price volatility | Infrastructure costs change gradually | Token unit price revisions cause sudden spikes |
| Version management | You control deployment timing | Affected by provider-side updates |

## Affected Forces

- `[F9]` Provider Reliability -- The less reliable the provider, the more essential fallback and multi-provider strategies become
- `[F7]` Cost Sensitivity & Scale -- When tolerance for price volatility is low, cost caps and routing controls are important
- `[F4]` Latency Budget -- Provider response time variability directly impacts SLAs

## Safeguard Patterns

- [#37 Semantic Gateway & Cost-Aware Router](../../decisions/dials/model-tier-routing.md) -- Dynamically select models by difficulty to optimize cost and quality
- [#40 Fallback & Graceful Degradation](../../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) -- Switch to alternative models or degraded mode during provider outages
- [#45 Agent Runtime Abstraction](../../decisions/tradeoffs-catalog/build-vs-buy.md) -- Abstract the execution platform to make providers swappable

## Related Design Decisions

- [retry-count](../../decisions/dials/retry-count.md) -- Too many retries can worsen rate limiting
- [model-tier-routing](../../decisions/dials/model-tier-routing.md) -- Which difficulty level of requests to route to which model
- [single vs. multi-provider](../../decisions/tradeoffs-catalog/single-vs-multi-provider.md) -- Single-provider simplicity vs. multi-provider fault tolerance
- [fail-fast vs. degradation](../../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) -- Fail immediately on outage or continue with degraded operation
