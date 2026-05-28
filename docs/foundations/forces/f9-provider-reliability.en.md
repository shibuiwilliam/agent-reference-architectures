---
title: "[F9] Provider Reliability"
tags:
  - "Driving Variables"
---

# [F9] Provider Reliability

!!! abstract "Summary"
    A force that measures concerns about external LLM provider availability and vendor lock-in. The lower the reliability, the more fallback, abstraction, and multi-provider strategies are needed.

## Overview

Late at night, the LLM provider had an outage, and the production service that fully depended on it was completely down for hours -- single-provider dependency means a provider outage becomes a system-wide outage.

Provider reliability represents the degree of trust in the availability, stability, and continuity of the external LLM providers the system depends on. When risks such as outages, pricing changes, API specification changes, and service discontinuation must be addressed, designs differ significantly.

## Why It Matters

LLM providers experience outages more frequently than traditional cloud services, and rate limits, model deprecations, and API specification changes also occur frequently. Designs tightly coupled to a single provider mean provider outages translate directly into full system downtime. Furthermore, tight coupling to a specific provider's SDK or prompt format makes migration to better or cheaper providers prohibitively expensive.

## Interpreting the Value Range

### When Low (Reliability is High = Risk is Low)

Situations where a single provider is judged sufficient. Internal tools, PoCs, and low-traffic systems where some downtime is acceptable. You can use the provider's SDK directly and take full advantage of model-specific features (structured output, tool call format, etc.). Development speed is prioritized by avoiding abstraction layer overhead.

### When High (Reliability is Low = Risk is High)

Situations where availability and vendor lock-in are major concerns. Mission-critical B2C services, multi-region deployments, and systems intended for long-term operation are typical examples. Fallback paths for provider outages, compatibility layers to absorb model differences, and provider-agnostic runtime abstraction are needed. Operating multiple provider contracts and routing logic incurs costs, but availability and negotiating leverage are secured.

## Evaluation Guidelines

- What is the outage frequency and recovery time of the LLM provider used over the past six months?
- Does the system come to a complete halt during a provider outage, or can it operate in a degraded mode?
- Do current prompts and tool call formats depend on provider-specific APIs?
- Have you estimated migration costs if the provider changes prices or deprecates models?
- Are there contractual clauses restricting the use of providers other than the current one?

## Influenced Design Decisions

### Related Dials

- [Model Tier Routing](../../decisions/dials/model-tier-routing.md) -- Define routing strategies across multiple providers
- [Retry Count](../../decisions/dials/retry-count.md) -- Retry count during provider outages and the threshold for switching to fallback
- [Timeout](../../decisions/dials/timeout.md) -- The threshold for switching to fallback when the provider's response is delayed

### Related Tradeoffs

- [Single vs. Multi-Provider](../../decisions/tradeoffs-catalog/single-vs-multi-provider.md) -- Choose multi-provider when reliability is low
- [Fail-Fast vs. Degradation](../../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) -- Fail immediately on provider outage, or continue with degraded operation via another provider
- [Build vs. Buy](../../decisions/tradeoffs-catalog/build-vs-buy.md) -- Build the provider abstraction layer in-house or use an OSS framework

## Related Patterns

- [#40 Fallback & Graceful Degradation](../../glossary.md) -- Continue with staged degradation on failure
- [#45 Agent Runtime Abstraction](../../glossary.md) -- Abstract the execution platform to be provider-agnostic
- [#46 Model Behavior Compatibility Layer](../../glossary.md) -- A compatibility layer that absorbs behavioral differences between models
- [#36 Shadow / Canary Deployment](../../glossary.md) -- Gradually verify switching to new providers/models
- [#53 Agent Change Management](../../glossary.md) -- Change management processes including provider changes
