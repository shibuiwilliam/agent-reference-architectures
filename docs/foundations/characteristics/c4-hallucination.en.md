---
title: "[C4] Hallucination"
tags:
  - "Characteristics"
---

# [C4] Hallucination

!!! abstract "Summary"
    Confidently generates information that contradicts facts -- the system cannot trivially guarantee the correctness of its output.

## Overview

LLMs predict the next token based on learned data patterns and lack an internal mechanism to verify the "factual accuracy" of their output. Non-existent URL citations, fabricated legal precedents, and numerical errors are generated in a tone indistinguishable from accurate information. Unlike traditional software that "crashes" clearly as a bug, hallucinations silently infiltrate as normal-looking output.

## Why This Is a Problem

A legal agent cites a non-existent precedent and produces contract review comments based on it. A customer support agent recommends a non-existent return policy, leading to complaints when customers do not receive the expected treatment. A medical information agent responds with incorrect dosage amounts, creating a safety incident. The most troublesome aspect is that these do not appear as "errors" in logs and go undetected unless a human scrutinizes the content. By the time they are discovered, customer interactions or decisions have already been affected.

## Comparison with Traditional Software

| Aspect | Traditional Software | AI Agent |
|--------|---------------------|----------|
| Incorrect output | Manifested explicitly as exceptions or error codes | Silently mixed in as normal responses |
| Detection method | Detected by unit tests | Requires semantic verification or human review |
| Basis for trust | Correctness of code logic | Requires cross-referencing with evidence sources |
| Occurrence frequency | Converges as bugs are fixed | Fluctuates with model updates; complete elimination is impossible |

## Affected Forces

- `[F2]` Failure Cost -- When high, a single hallucination can cause critical damage
- `[F8]` Accountability & Regulation -- In regulated industries, answers without evidence can incur legal liability
- `[F3]` Request Value -- Higher-value answers demand stronger accuracy guarantees

## Safeguard Patterns

- [#27 Evidence-First Answer](../../decisions/tradeoffs-catalog/rag-vs-finetuning.md) -- Retrieve and cite evidence before answering to suppress groundless generation
- [#29 Guardrail Sidecar + Self-Correction](../../decisions/tradeoffs-catalog/inline-vs-post-verification.md) -- Inspect output and self-correct or block when factual accuracy is in doubt

## Related Design Decisions

- [guardrail-strictness](../../decisions/dials/guardrail-strictness.md) -- Higher guardrail strictness reduces hallucination pass-through rate but may also block legitimate answers
- [self-correction-loops](../../decisions/dials/self-correction-loops.md) -- More correction loops improve quality but increase cost and latency
- [inline vs. post verification](../../decisions/tradeoffs-catalog/inline-vs-post-verification.md) -- Verify immediately at output time, or batch-verify downstream
