---
title: "Cache Similarity Threshold"
tags:
  - "Tuning Dial"
  - "F7 Cost Sensitivity / Scale"
---

# Cache Similarity Threshold

!!! abstract "TL;DR"
    Control the hit threshold for semantic caching, weighing cache efficiency against answer accuracy.

## Overview

You ask "What's today's exchange rate?" and get yesterday's cached rate in return -- semantic caching is a powerful cost-reduction strategy, but misjudging similarity can destroy user trust in an instant.

This dial controls the similarity threshold that determines whether to return a cached result for semantically similar queries. Measured by cosine similarity or other distance metrics, results above the threshold are reused from the cache. A lower threshold increases hit rate but raises mismatch risk; a higher threshold is more accurate but diminishes the benefits of caching.

## Why Adjustment Is Needed

LLM calls carry significant cost and latency, making caching highly effective. However, natural language queries have large variation in expression, and determining "same intent" is difficult. An improper threshold causes stale answers to be returned for subtly different questions, eroding user trust. Conversely, if the threshold is too strict, the hit rate drops to single-digit percentages and only the cost of the caching infrastructure remains.

## Extremes of the Range

### Too Small

Only near-exact-match queries hit the cache, resulting in extremely low hit rates. The cost of the caching infrastructure (vector DB, embedding computation) does not deliver proportional benefits. Natural language expression variations cannot be absorbed.

### Too Large

Stale results are returned for queries with subtly different meanings. Users expecting "today's information" or "different context" receive cached results instead. This is especially problematic for time-dependent information or queries requiring personalization.

## Determining Forces

- `[F7]` Cost Sensitivity / Scale -- Higher cost pressure drives the desire to increase cache hit rates, but quality tradeoffs arise

## Guidelines (Starting Point)

- Cosine similarity: 0.92-0.97
- Factual retrieval (FAQ, document search): Around 0.95
- Creative or personalized queries: Disable caching entirely, or set threshold at 0.98+
- Time-dependent information: Ensure freshness through combination with TTL
- Threshold recalibration is mandatory when switching embedding models

## Practical Adjustment

- Measure hit rate and mismatch rate (proportion of users who re-asked) on a weekly basis
- Compare user satisfaction between cache hits and misses to evaluate threshold appropriateness
- Set separate thresholds per domain rather than using a uniform setting
- Periodically recalibrate thresholds in response to embedding model updates or query distribution changes

## Related Patterns

- [#38 Semantic Result Cache](../../glossary.md) -- Implementation pattern for semantic-similarity-based caching
