---
title: "Prompt Cache Optimized Context"
tags:
  - "Cost, Performance & Scaling"
  - "F7 Cost Sensitivity & Scale"
  - "F4 Latency Budget"
---

# #39 Prompt Cache Optimized Context

!!! abstract "TL;DR"
    **Fix common prefixes (system prompts, few-shot examples) at the beginning** of the prompt to maximize LLM provider prompt caching.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #39 Prompt Cache Optimized Context</summary>

| Field | Value |
|------|-----|
| **ID** | 39 |
| **Category** | 08-cost-scaling — Cost, Performance & Scaling |
| **Forces** | `[F7]`, `[F4]` |
| **Dials** | — |
| **Tradeoffs** | — |
| **Related Patterns** | #38, #24, #37 |
| **When to Use** | Long system prompts/few-shot examples, batch requests of same category, large RAG context |
| **When Not to Use** | Prompt structure varies significantly per request; provider does not support caching; prefix too short |
| **Element Technologies** | Anthropic Prompt Caching, OpenAI Automatic, Google Context Caching |

</details>
<!-- END:GEN:meta -->

## Overview

When including large amounts of RAG context in prompts, input token counts can balloon to thousands or tens of thousands, worsening cost and latency. However, the bulk of this is often content shared across requests, such as system prompts and few-shot examples.

Many LLM providers apply caching when the prefix portion of prompts matches, reducing input token costs and Time to First Token (TTFT). This pattern stably places system prompts, few-shot examples, and common context at the beginning of the prompt, with per-request variable content (user input, dynamic context) at the end. By maintaining a prefix length above a certain threshold, cache hit rates are maximized.

!!! info "Position in decision-making"
    - **Driving force**: `[F7]` Cost Sensitivity & Scale, `[F4]` Latency Budget
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

The prompt is structured in three layers. Layer 1 is the system prompt + behavioral guidelines (shared across all requests, low change frequency). Layer 2 is few-shot examples and domain knowledge (shared across task categories). Layer 3 is user input and session-specific context (per-request). Layers 1 and 2 form the common prefix that becomes the caching target. The ordering within Layer 2 is also stabilized (e.g., via hashing) to prevent cache invalidation from order variations.

## Problems Solved

Including large amounts of RAG context in prompts inflates input token counts, worsening cost `[F7]` and latency `[F4]`. When prompt caching is effective, input costs for the common prefix are reduced by 50-90%, and TTFT is also shortened. However, if the prefix is unstable, cache hit rates drop and the expected benefits are not realized.

## When to Use / When Not to Use

- **When to Use**: Agents with long system prompts or few-shot examples, workloads with consecutive requests in the same category, configurations with large RAG context.
- **When Not to Use**: When prompt structure changes significantly per request, or when the provider does not offer prompt caching. Also ineffective for short prompts that do not meet the minimum prefix length for cache eligibility.

## Element Technologies

- Provider caching: Anthropic Prompt Caching, OpenAI Automatic Prompt Caching, Google Context Caching
- Context assembly: Used in combination with [#24 Context Pack / Assembly](../05-memory-context/24-context-pack-assembly.md)
- Order stabilization: Hash-based sorting of context chunks

## Tuning (Dials)

- **Prefix length** — Too short falls below the provider's minimum cache threshold vs. too long narrows the context window for dynamic content / Deciding factor `[F7]` / Guideline: Meet the provider's minimum prefix requirement (e.g., 1024+ tokens) while leaving sufficient room for dynamic content. → [Tuning Dials](../../decisions/tuning-dials.md)

## Related Patterns

- [#38 Semantic Result Cache](38-semantic-result-cache.md) — Result-level caching (complementary to prompt caching)
- [#24 Context Pack / Assembly](../05-memory-context/24-context-pack-assembly.md) — How context is assembled directly affects cache efficiency
- [#37 Semantic Gateway](37-semantic-gateway-cost-aware-router.md) — Combine model selection with caching strategies for cost optimization

## References

- Anthropic Prompt Caching Documentation
- OpenAI Prompt Caching Guide
