---
title: "Retrieval top-k / Injection Volume"
tags:
  - "Tuning Dial"
  - "F4 Latency Budget"
  - "F7 Cost Sensitivity / Scale"
---

# Retrieval top-k / Injection Volume

!!! abstract "TL;DR"
    Control the number of chunks retrieved in RAG, balancing information coverage against context overflow.

## Overview

A RAG-generated answer was produced, but the key supporting document was not included in the context, resulting in an answer mixed with hallucinations. On the other hand, injecting a large volume of chunks caused the LLM to be swayed by irrelevant information -- the number of retrieved items directly affects RAG quality.

This dial determines the top-k number of chunks retrieved from vector search or hybrid search in Retrieval-Augmented Generation (RAG). A larger k reduces the probability of missing relevant information, but inflates the context fed to the LLM, leading to increased token costs, attention dilution, and latency growth.

## Why Adjustment Is Needed

When k is small, relevant information is missed, causing inaccurate answers or hallucinations. When k is large, the context window is overwhelmed, and the "lost in the middle" problem occurs where the LLM's attention is diffused by irrelevant information. The optimal k varies based on query type, chunk size, and context window size.

## Extremes of the Range

### Too Small

Information needed for the answer is not included in the context, and the LLM answers from its own knowledge only. Grounding is insufficient, and hallucination risk increases. Questions spanning multiple documents cannot be addressed.

### Too Large

Search results occupy most of the context window, reducing the relative influence of instructions and system prompts. Token costs increase linearly and latency worsens. Irrelevant chunks become noise, actually degrading answer quality.

## Determining Forces

- `[F4]` Latency Budget -- Increasing k directly impacts latency through increased prompt length
- `[F7]` Cost Sensitivity / Scale -- The number of injected tokens directly impacts cost

## Guidelines (Starting Point)

- General Q&A: top-k 5-10
- Complex analysis or comparison: top-k 10-20
- With large chunk sizes (1000+ tokens): Use a smaller k
- With a reranker: Retrieve broadly initially (k=50-100), then narrow to 5-10 after reranking

## Practical Adjustment

- Measure Recall@k on an evaluation dataset and find the point where increasing k no longer yields improvement
- Introduce a reranker and consider a two-stage approach: broad initial retrieval, narrowed final injection
- Optimize the combination of chunk size and k (small chunks x many k vs. large chunks x few k)
- Monitor context window utilization and keep search results under 50% of the window

## Related Patterns

- [#24 Context Pack / Assembly](../../glossary.md) -- Pattern for assembling context including search results
