---
title: "[F7] Cost Sensitivity & Scale"
tags:
  - "Driving Variables"
---

# [F7] Cost Sensitivity & Scale

!!! abstract "Summary"
    A force that measures request volume and the strictness of cost caps. The higher the sensitivity, the more essential caching, routing, and budget controls become.

## Overview

An agent that worked comfortably in development saw its end-of-month API bill balloon to 10x projections the moment it hit production -- LLM inference costs are orders of magnitude higher than traditional API calls, so traffic increases translate directly into budget overruns.

Cost sensitivity & scale represents the request volume (QPS) processed by the system and the strictness of the monthly LLM API cost cap. Since unlimited calls cause monthly expenses to balloon rapidly, this force is the starting point for all cost-efficiency design decisions.

## Why It Matters

Overlooking cost sensitivity means a system that works fine in development exceeds its budget the moment it receives production traffic. Or you only realize the problem when the end-of-month API invoice arrives. Especially in architectures where agents autonomously call tools in loops, the number of LLM calls per request is hard to predict, and the risk of budget runaway is high.

## Interpreting the Value Range

### When Low

Situations where cost constraints are relaxed. R&D phase, internal tools for small teams, and cases where per-request value is sufficiently high (`[F3]` high). The highest quality models can be used freely, and retries and multi-candidate generation are acceptable. Optimization can be deprioritized in favor of quality and speed.

### When High

Situations with high request volumes and strict cost caps. B2C service LLM responses to all users, large-scale batch processing, and startup runway constraints are typical examples. Cost optimization patterns become essential: dynamic model tier selection (large models only for difficult problems), semantic caching, prompt compression, and budget-capped loops.

## Evaluation Guidelines

- Is the monthly LLM API cost cap explicitly defined?
- What is the peak QPS, and are there seasonal variations or bursts?
- Is the number of LLM calls per request predictable, or does it depend on agent judgment?
- What is the current average cost per request, and is it sustainable?
- Is there a response plan for cost overruns (degradation, rejection, alerts)?

## Influenced Design Decisions

### Related Dials

- [Budget Cap](../../decisions/dials/budget-cap.md) -- Set caps at the per-request and per-session levels
- [Model Tier Routing](../../decisions/dials/model-tier-routing.md) -- Select between lightweight and large models by difficulty
- [Cache Similarity](../../decisions/dials/cache-similarity.md) -- Lower the cache similarity threshold to increase hit rate
- [Retry Count](../../decisions/dials/retry-count.md) -- Limit retry count as cost sensitivity increases
- [Temperature](../../decisions/dials/temperature.md) -- Low temperature stabilizes output and reduces rejection rate, lowering cost

### Related Tradeoffs

- [RAG vs. Fine-Tuning](../../decisions/tradeoffs-catalog/rag-vs-finetuning.md) -- For high volumes of similar requests, fine-tuning may reduce inference costs
- [LLM vs. Tool](../../decisions/tradeoffs-catalog/llm-vs-tool.md) -- Offload LLM-unnecessary processing to rule-based methods for cost savings
- [Fail-Fast vs. Degradation](../../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) -- Fail-fast on budget overrun or handle with degradation
- [Build vs. Buy](../../decisions/tradeoffs-catalog/build-vs-buy.md) -- Compare managed service usage-based pricing with self-hosted fixed costs

## Related Patterns

- [#38 Semantic Result Cache](../../decisions/dials/cache-similarity.md) -- Reuse semantically similar results to reduce API calls
- [#56 Adaptive Effort](../../foundations/forces/f7-cost-sensitivity.md) -- Scale compute effort up or down by difficulty
- [#37 Semantic Gateway & Cost-Aware Router](../../decisions/dials/model-tier-routing.md) -- Dynamically select models with cost awareness
- [#5 Time-Budgeted Agent Loop](../../decisions/dials/budget-cap.md) -- Budget time, iterations, and cost to prevent loop runaway
- [#55 Deadline & Budget Cascade](../../decisions/dials/budget-cap.md) -- Propagate budget caps down the call tree
