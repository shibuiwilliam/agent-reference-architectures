---
title: "[C8] Cost Proportional to Input/Output Volume"
tags:
  - "Characteristics"
---

# [C8] Cost Proportional to Input/Output Volume

!!! abstract "Summary"
    Token-based pricing causes costs to vary by orders of magnitude depending on usage -- traditional compute resource management assumptions do not apply.

## Overview

In traditional software, infrastructure costs were primarily determined by CPU, memory, and storage, and per-request costs were nearly uniform. In AI agents, per-token usage-based pricing dominates, and request costs vary by factors of tens to hundreds depending on input length, number of reasoning steps, and output volume. Stuffing large document sets into context via RAG, resending prompts on retries, running self-correction loops -- all of these drive up costs.

## Why This Is a Problem

Costs that were 10,000 yen per month during development jump to 1,000,000 yen per month with production traffic. Simply changing RAG pipeline top-k from 10 to 50 increases input tokens by 5x and the bill by 5x. When guardrail self-correction loops run 3 times, the cost of a single request quadruples. In multi-tenant SaaS, one tenant's heavy requests consume the shared cost cap. Budget overruns are only noticed when the end-of-month invoice arrives, by which time it is too late. Lack of cost monitoring is not technical debt -- it is a business risk.

## Comparison with Traditional Software

| Aspect | Traditional Software | AI Agent |
|--------|---------------------|----------|
| Per-request cost | Nearly uniform (CPU-time based) | Varies by orders of magnitude based on I/O token volume |
| Cost prediction | Estimable by QPS x fixed unit cost | Varies significantly by task difficulty and context length |
| Scaling cost | Linear with instance count | Non-linear variation based on token consumption patterns |
| Cost optimization | Cache, CDN, DB optimization | Prompt design, model selection, caching |

## Affected Forces

- `[F7]` Cost Sensitivity & Scale -- The tighter the monthly cost cap, the higher the priority of cost control patterns
- `[F3]` Request Value -- When per-request value is low, using expensive models does not pay off
- `[F4]` Latency Budget -- Using smaller models to reduce cost may impact quality or latency

## Safeguard Patterns

- [#38 Semantic Result Cache](../../glossary.md) -- Reuse semantically similar past results to reduce LLM calls altogether
- [#39 Prompt Cache Optimized Context](../../glossary.md) -- Reduce input token cost through common prefix caching
- [#56 Adaptive Effort](../../glossary.md) -- Scale compute effort up or down by task difficulty to optimize cost efficiency

## Related Design Decisions

- [budget-cap](../../decisions/dials/budget-cap.md) -- Where to set cost caps at the request, tenant, and monthly levels
- [model-tier-routing](../../decisions/dials/model-tier-routing.md) -- Use cheaper models for easy tasks to reduce costs
- [cache-similarity](../../decisions/dials/cache-similarity.md) -- Balance between cache hit rate and cost reduction
- [retrieval-top-k](../../decisions/dials/retrieval-top-k.md) -- Number of search results directly impacts input token volume
