---
title: "Evidence-First Answer"
tags:
  - "Reliability, Verification, Guardrails & Autonomy"
  - "F8 Accountability & Regulation"
---

# #27 Evidence-First Answer

!!! abstract "TL;DR"
    Retrieve evidence **before** generating an answer, then present the response with citations.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #27 Evidence-First Answer</summary>

| Field | Value |
|------|-----|
| **ID** | 27 |
| **Category** | 06-reliability — Reliability, Verification, Guardrails & Autonomy |
| **Forces** | `[F8]` |
| **Dials** | — |
| **Tradeoffs** | rag-vs-finetuning |
| **Related Patterns** | #24, #28, #14 |
| **When to Use** | Legal/medical/financial Q&A, internal knowledge search, support requiring audit trails |
| **When Not to Use** | Creative/brainstorming (no correct source); evidence sources don't exist |
| **Element Technologies** | RAG pipeline, web search API, internal document API, confidence evaluation, citation metadata |

</details>
<!-- END:GEN:meta -->

## Overview

LLMs can "confidently get things wrong." Even with high confidence, if not grounded in facts, this can cause serious problems in legal, medical, and financial domains. Evidence-First Answer addresses this by separating the answer generation workflow into two stages: "first gather evidence, then compose the answer based on it." When no evidence is found, it explicitly returns "I don't know." Answers include citations (source document, chunk, URL) so users and auditors can verify.

!!! info "Position in Decision Framework"
    - **Driving Forces**: `[F8]` Accountability & Regulation
    - **Related Decisions**: [Tradeoffs](../../decisions/tradeoffs.md) — RAG ↔ FT ↔ Long Context
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

```mermaid
flowchart LR
    Q[Question] --> Search[Evidence Retrieval]
    Search --> Judge{Evidence<br/>sufficient?}
    Judge -->|sufficient| Gen[Answer Generation<br/>with citations]
    Judge -->|insufficient| Decline[Reply "unknown"<br/>or ask follow-up]
    Gen --> Out[Cited Answer]
```

The retrieval phase uses the same mechanisms as [#24 Context Pack / Assembly](../05-memory-context/24-context-pack-assembly.md), but adds an "answerability" assessment step. Citation format — inline footnotes (`[1]`) or metadata blocks — is chosen based on downstream use.

## Problem Solved

The most dangerous form of hallucination is "plausible but baseless answers." In `[F8]` regulated domains (legal, medical, financial), baseless advice can lead to legal liability. Evidence-First structurally eliminates the "answering without evidence" path by making answer generation dependent on evidence retrieval.

## When to Use / When Not to Use

- **When to Use**: Suitable for legal, medical, and financial Q&A, internal knowledge search, and customer support requiring audit compliance.
- **When Not to Use**: Not suited for creative or brainstorming tasks with no correct answers, or exploratory conversations where evidence sources don't exist.

## Element Technologies

- Evidence Retrieval: RAG pipeline, web search API, internal document API
- Sufficiency Assessment: LLM self-evaluation (confidence score), search score threshold
- Citation Attachment: Embed chunk ID and URL as metadata in the answer
- Display: Frontend footnote rendering, source links

## Related Patterns

- [#24 Context Pack / Assembly](../05-memory-context/24-context-pack-assembly.md) — The implementation foundation for evidence retrieval
- [#28 Verifier Agent / Critic](28-verifier-agent-critic.md) — A complementary pattern adding independent verification after generation
- [#14 Structured Output Contract](../03-io-contract/14-structured-output-contract.md) — Contractualizes citation metadata with schemas

## References

- Gao et al., "RARR: Researching and Revising What Language Models Say" (2023)
