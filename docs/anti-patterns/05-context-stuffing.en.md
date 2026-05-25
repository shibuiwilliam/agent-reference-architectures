---
title: "Context Stuffing"
tags:
  - "Anti-Pattern"
  - "Degree Error"
---

# 5. Context Stuffing

!!! abstract "TL;DR"
    An anti-pattern where all potentially relevant information is crammed into the prompt, overwhelming the context window and degrading both answer quality and cost.

## Common Scenario

A team built a RAG-based internal document search agent. With the rationale that "more information is better than less," they set the retrieval top-k to 20 and injected all retrieved chunks into the prompt. Initial tests showed good answer quality, but problems surfaced as the document corpus grew. Low-relevance chunks became noise, and the agent began citing irrelevant information and generating incorrect answers.

Furthermore, per-request token counts ballooned from an average of 8,000 to 30,000, nearly quadrupling costs. Latency also worsened, with responses taking over 5 seconds.

## Symptoms

- Per-request input token count is 3x or more the expected amount
- RAG search results contain irrelevant information, leading to off-target answers
- Context window limits are frequently hit, causing important information to be truncated
- Latency increases proportionally with context volume
- Costs increase beyond what request count alone would explain (due to increased token volume)

## Root Cause

The underlying expectation is that "if we put more information in the context, the model will appropriately filter it." However, research shows that LLMs tend to overlook middle portions of long contexts (the "Lost in the Middle" problem), and answer quality degrades with more noise.

The design of top-k values and chunk sizes is not tied to `[F7]` cost sensitivity or `[F4]` latency budget. The "retrieve everything you can and stuff it all in" approach merely shifts the information filtering cost onto the LLM.

## Detection Methods

- **Input token distribution**: Monitor per-request input token counts and check for upward trends
- **Retrieval chunk relevance analysis**: Review relevance scores of injected chunks and verify whether low-relevance chunks are included
- **Answer quality vs. input volume correlation**: Compare answer quality across different top-k values and find the quality peak
- **Metrics**: `input_tokens_per_request`, `retrieval_relevance_score`, `answer_quality_vs_topk`

## Countermeasures

### Step 1: Optimize top-k and relevance thresholds

Instead of a fixed top-k, set a relevance score threshold. Only inject chunks that exceed the threshold.

### Step 2: Introduce context assembly logic

Evaluate retrieved chunks by relevance, redundancy, and information value, then select and compress them to fit within a limited context budget.

### Step 3: Implement progressive information retrieval

First attempt to answer with a small amount of context, and only perform additional retrieval if information is insufficient.

```python
# Progressive context assembly example
context_budget = 4000  # Token limit

# Sort by relevance and assemble within budget
chunks = retriever.search(query, top_k=20)
chunks = [c for c in chunks if c.relevance > 0.7]  # Threshold filter
chunks = deduplicate(chunks)

assembled = []
token_count = 0
for chunk in chunks:
    if token_count + chunk.tokens > context_budget:
        break
    assembled.append(chunk)
    token_count += chunk.tokens
```

## Examples

### Before (problematic state)

```python
# Retrieve everything and inject it all
chunks = retriever.search(query, top_k=20)
context = "\n".join([c.text for c in chunks])  # Concatenate all chunks

response = llm.chat(
    system="Answer based on the following context.",
    context=context,  # Average 30,000 tokens
    query=user_query,
)
```

### After (improved)

```python
from context_assembler import ContextPack

chunks = retriever.search(query, top_k=20)
pack = ContextPack(
    budget_tokens=4000,
    relevance_threshold=0.7,
)
context = pack.assemble(chunks)  # Select only the most relevant

response = llm.chat(
    system="Answer based on the following context.",
    context=context,  # Average 4,000 tokens
    query=user_query,
)
# 75% cost reduction, answer quality equal or better
```

## Related Anti-Patterns

- [Strongest Model Only](03-strongest-model-only.md) — Compressing context may enable smaller models to handle the task
- [Infinite / Excessive Timeout](01-infinite-timeout.md) — Increased latency from large contexts compounds with timeout issues

## Related Patterns

- [#24 Context Pack / Assembly](../patterns/05-memory-context/24-context-pack-assembly.md) — Selectively assemble only highly relevant information
- [#23 Layered Memory](../patterns/05-memory-context/23-layered-memory.md) — Layer memory to optimize access patterns
- [#25 Memory Write Gate](../patterns/05-memory-context/25-memory-write-gate.md) — Filter what information to store in the first place
