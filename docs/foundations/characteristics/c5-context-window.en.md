---
title: "[C5] Finite Context Window"
tags:
  - "Characteristics"
---

# [C5] Finite Context Window

!!! abstract "Summary"
    Input token count has an upper limit, preventing long conversations or large documents from being handled at once -- a capacity constraint on memory and attention.

## Overview

The LLM context window is finite (thousands to millions of tokens). Long dialogue histories, large document sets, and past tool execution results cannot all be packed into the context. While traditional software could scale memory or storage, with LLMs, longer input increases cost and can cause performance degradation where middle portions of information get "lost" (the Lost in the Middle problem).

## Why This Is a Problem

In customer support, after 30 conversation turns, the early context is lost and the agent starts repeating the same questions. When asked to analyze a 100-page document, later content pushes out earlier context, biasing the answers. In multi-agent architectures, when passing one agent's output to the next, context overflow causes critical decision rationale to be dropped. Users lose trust in an agent that does not remember "the conditions I mentioned earlier" and stop using it.

## Comparison with Traditional Software

| Aspect | Traditional Software | AI Agent |
|--------|---------------------|----------|
| State retention | Unlimited retention in DB/memory | Only what fits in the context window |
| Long-term memory | Explicit CRUD operations | Information that overflows the window automatically disappears |
| Information volume and cost | Storage cost (inexpensive) | Token cost (proportional to input volume, expensive) |

## Affected Forces

- `[F4]` Latency Budget -- Longer context increases inference time
- `[F7]` Cost Sensitivity & Scale -- Input token count directly impacts cost, making removal of unnecessary information important
- `[F6]` Task Variability -- Exploratory tasks require more context and are more likely to hit window constraints

## Safeguard Patterns

- [#23 Layered Memory](../../decisions/tradeoffs-catalog/in-context-vs-external.md) -- Organize memory into short-term, long-term, and shared layers, loading only necessary information into context
- [#24 Context Pack / Assembly](../../decisions/tradeoffs-catalog/rag-vs-finetuning.md) -- Selectively assemble relevant information via RAG or summarization to use the window efficiently
- [#26 Forgetting and Expiration](../../decisions/dials/memory-ttl.md) -- Set expiration dates on old information to prevent window pressure

## Related Design Decisions

- [retrieval-top-k](../../decisions/dials/retrieval-top-k.md) -- More search results provide richer information but put pressure on the window
- [summarization-timing](../../decisions/dials/summarization-timing.md) -- When to run summarization determines the balance between information freshness and window efficiency
- [memory-ttl](../../decisions/dials/memory-ttl.md) -- Memory retention period controls the volume of information flowing into the window
- [in-context vs. external](../../decisions/tradeoffs-catalog/in-context-vs-external.md) -- Keep it in context or offload to an external store
