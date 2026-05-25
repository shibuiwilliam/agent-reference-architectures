---
title: Anti-Patterns
---

# Anti-Patterns

!!! abstract "TL;DR"
    A collection of **counter-examples for the decision layer** — common design mistakes, their symptoms, and countermeasures.

Even if you know the patterns, applying them incorrectly will cause problems in production. Here we organize the "common mistakes" that are repeatedly observed in real projects.

Anti-patterns can be classified into three types: **(a) Degree errors** (dial misconfiguration), **(b) Tradeoff mis-selection** (wrong choice in binary decisions), and **(c) Pattern misuse** (incorrect application of patterns). All tend to occur as a result of ignoring forces `[F#]`.

-> [Tuning Dials Catalog](../decisions/tuning-dials.md) / [Tradeoffs Catalog](../decisions/tradeoffs.md)

---

## Classification

### (a) Degree Errors — Dial Misconfiguration

Problems caused by setting dial values too low or too high.

| # | Anti-Pattern | Causal Dial |
|---|------------|----------------|
| 1 | [Infinite / Excessive Timeout](01-infinite-timeout.md) | Timeout / Budget Cap |
| 2 | [Excessive Guardrails](02-excessive-guardrails.md) | Guardrail Strictness |
| 3 | [Strongest Model Only](03-strongest-model-only.md) | Model Tier Threshold |
| 4 | [Full Observability Deployment](04-full-observability.md) | Trace Sampling Rate / Log Retention Period |
| 5 | [Context Stuffing](05-context-stuffing.md) | Retrieval top-k / Input Volume |
| 6 | [No Rationale for Dial Settings](06-no-rationale.md) | All Dials |

### (b) Tradeoff Mis-selection — Wrong Binary Choices

Problems caused by leaning too far in one direction while ignoring forces.

| # | Anti-Pattern | Relevant Tradeoff |
|---|------------|---------------|
| 7 | [All Sync / All Async](07-all-sync-or-async.md) | Sync vs. Async |
| 8 | [Universal Multi-Agent](08-universal-multi-agent.md) | Single vs. Multi-Agent |
| 9 | [Retry Storm](09-retry-storm.md) | Fail-fast vs. Graceful Degradation |

### (c) Pattern Misuse — Incorrect Application

Problems caused by misapplying the patterns themselves.

| # | Anti-Pattern | Misused Pattern Area |
|---|------------|-------------------|
| 10 | [Prompt as Security Boundary](10-prompt-as-security.md) | Security / Privilege Separation |
| 11 | [Using LLMs as Calculators](11-llm-as-calculator.md) | Tool Delegation / I/O Contract |
