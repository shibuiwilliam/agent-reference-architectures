---
title: Degree (Tuning) Dials
---

# Degree (Tuning) Dials

!!! abstract "TL;DR"
    Patterns are not ON/OFF — they come with **dials**. The value range of each dial is determined by driving variables `[F#]`.

## What Are Dials?

After adopting a pattern, have you ever wondered "what should the timeout be?" or "how many retries should we allow?" Many patterns have parameters that determine "to what degree" they are applied. Since setting these too low or too high both cause problems, the optimal point must be determined based on the system's context — that is, the value ranges of the [Driving Variables (Forces)](../foundations/forces.md).

## Approach

Dial guideline values are merely **starting points**, with the assumption that they will be validated and adjusted using production data. Operate using these 3 steps:

1. **Determine the starting point from forces** — Check the "determining factor" force for each dial and set the guideline value
2. **Validate with production metrics** — Observe actual error rates, costs, and latency to judge whether the values are appropriate
3. **Review periodically** — Re-adjust as forces change (scale increases, regulatory tightening, etc.)

## Dial Classification and Meaning

The 20 dials can be classified into 5 categories by the domain they control.

### Execution Control

Dials related to agent execution time, retries, and cost. Directly impacts system stability and responsiveness.

| Dial | Determining Factor | Guideline | Details |
|---------|-------|------|------|
| **Timeout** | `[F4]` | Sync 5–10s, Async 5–30min | [→](dials/timeout.md) |
| **Retry Count** | `[F9]` | 2–3 times (exponential backoff) | [→](dials/retry-count.md) |
| **Self-Correction Loop Count** | `[F7]` `[F3]` | 1–3 times | [→](dials/self-correction-loops.md) |
| **Checkpoint Frequency** | `[F1]` | Per step or every N minutes | [→](dials/checkpoint-frequency.md) |
| **Budget Cap** | `[F7]` `[F3]` | 10–30% of request value | [→](dials/budget-cap.md) |

### Autonomy & Safety Control

Dials that determine how much to delegate to the agent and where humans intervene.

| Dial | Determining Factor | Guideline | Details |
|---------|-------|------|------|
| **Autonomy Level** | `[F2]` `[F1]` | Start low for new agents → promote with track record | [→](dials/autonomy-level.md) |
| **HITL Frequency** | `[F2]` | High-risk operations only | [→](dials/hitl-frequency.md) |
| **Guardrail Strictness** | `[F5]` `[F2]` | Threshold 0.7–0.9 | [→](dials/guardrail-strictness.md) |

### Model & Generation Control

Dials that determine how LLMs are used and how costs are allocated.

| Dial | Determining Factor | Guideline | Details |
|---------|-------|------|------|
| **Model Tier** | `[F7]` `[F3]` | Use smaller model when confidence ≥ 0.8 | [→](dials/model-tier-routing.md) |
| **Best-of-N** | `[F2]` `[F3]` | 1 (low risk), 3–5 (high risk) | [→](dials/best-of-n.md) |
| **Temperature** | `[F6]` | 0.0–0.3 (routine), 0.5–0.8 (exploratory) | [→](dials/temperature.md) |

### Memory & Context Control

Dials that determine the volume of information the agent references and accumulates.

| Dial | Determining Factor | Guideline | Details |
|---------|-------|------|------|
| **Cache Similarity Threshold** | `[F7]` | Cosine similarity 0.92–0.97 | [→](dials/cache-similarity.md) |
| **Retrieval top-k** | `[F4]` `[F7]` | 5–20, ≤50% of total | [→](dials/retrieval-top-k.md) |
| **Memory TTL** | `[F8]` | Session 1 hour, long-term 30–90 days | [→](dials/memory-ttl.md) |
| **Memory Write Eagerness** | `[F8]` | Automatic based on confidence threshold | [→](dials/memory-write-eagerness.md) |
| **Summarization Timing** | `[F4]` | When token usage reaches 70% of window | [→](dials/summarization-timing.md) |
| **Exposed Tool Count** | `[F6]` | 5–15 per session | [→](dials/exposed-tool-count.md) |

### Observation & Recording Control

Dials related to logging, tracing, and prompt management. Balances audit/debugging granularity with cost.

| Dial | Determining Factor | Guideline | Details |
|---------|-------|------|------|
| **Trace Sampling Rate** | `[F8]` `[F7]` | Dev 100%, Prod 1–10% | [→](dials/trace-sampling-rate.md) |
| **Prompt Storage Destination & Granularity** | `[F8]` | Git-managed, with version tags | [→](dials/prompt-storage.md) |
| **Log Retention Period** | `[F8]` `[F7]` | Hot 7–30 days, Cold 1–7 years | [→](dials/log-retention.md) |

## How to Use

1. Check the dials listed in the "Tuning (Degree)" section of the pattern you are adopting
2. Rate your system's [Driving Variables](../foundations/forces.md) as "High/Medium/Low"
3. Cross-reference with the "Determining Factor" column in the tables above and set the guideline value as a starting point
4. Continuously adjust based on production metrics (error rate, cost, latency)

Dial values are not "set once and forget." It is important to review them periodically following the process in [#53 Agent Change Management](../foundations/forces/f8-accountability.md).
