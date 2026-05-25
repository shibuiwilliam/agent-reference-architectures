---
title: Architecture Decision Record (ADR) Template
---

# Architecture Decision Record (ADR) Template

!!! abstract "TL;DR"
    Preserve the "why" behind design decisions in a reproducible format. Capture force evaluations, either-or selections, and dial settings with their rationale — all on one page.

## What Is an ADR?

"Why did we set the timeout to 5 seconds?" "Why did we choose async?" — Can you answer these questions immediately six months later? An Architecture Decision Record (ADR) is a document that records design decisions and their rationale. In AI agent architectures, it is particularly important to record not just pattern selection, but also **degree (dial) settings** and **tradeoff (either-or) selection rationale**. Without documented rationale, tuning becomes impossible when problems arise, leading to knowledge silos.

## Template

Copy and use the following. Each item corresponds to a step in the [Decision-Making Process](decision-flow.md).

```markdown
# ADR-NNN: [Title]

- **Date**: YYYY-MM-DD
- **Status**: Proposed / Accepted / Rejected / Deprecated
- **Stakeholders**: [Decision makers, reviewers]

## Context

[What system/feature needed a decision, and what was the question. 1–3 sentences.]

## Force Evaluation (F1–F9)

| Force | Rating | Rationale |
|---------|------|------|
| F1 Reversibility | High/Med/Low | [Why this rating] |
| F2 Failure Cost | High/Med/Low | |
| F3 Per-Request Value | High/Med/Low | |
| F4 Latency Budget | High/Med/Low | |
| F5 Input Trustworthiness | High/Med/Low | |
| F6 Task Variability | High/Med/Low | |
| F7 Cost Sensitivity | High/Med/Low | |
| F8 Accountability | High/Med/Low | |
| F9 Provider Reliability | High/Med/Low | |

## Either-Or Decisions Considered

| Either-Or | Selection | Decisive Force | Rationale |
|---------|------|--------------|------|
| [e.g., Sync vs. Async] | [Async] | F4 | [Processing takes over 30 seconds] |

→ For either-or details, see the [Tradeoff Catalog](tradeoffs.md).

## Dials Configured

| Dial | Setting | Decisive Force | Rationale |
|---------|--------|--------------|------|
| [e.g., Timeout] | [5 min] | F4 | [Measured max processing time + margin] |

→ For dial details, see the [Degree Catalog](tuning-dials.md).

## Decision

[The adopted pattern composition and the rationale for the combination.]

## Rejected Alternatives

[Alternatives considered but not adopted, and why.]

## Re-evaluation Conditions

[Under what force changes should this decision be revisited.]
```

## Tips for Use

- **You don't need to fill in all forces.** It is sufficient to document rationale only for the decisive forces. However, explicitly noting "Low" for non-decisive forces is helpful during re-evaluation.
- **ADR corresponds to step (5) of the Decision-Making Process.** Record the results of tracing steps (1)–(4) of the [Decision-Making Process](decision-flow.md) here.
- **Re-evaluation conditions are the most important part.** Since forces fluctuate, specify conditions concretely, such as "when F7 becomes High" or "when monthly QPS exceeds 10x."
- The granularity standard for records is "can the same decision be reproduced later?" It is sufficient if a new team member can read this ADR and understand why this configuration was chosen.

## Worked Example

Concrete ADR examples are appended to each system in the [Worked Examples](worked-examples.md).

## Related Pages

- [Decision-Making Process](decision-flow.md) — The overall workflow that ADR corresponds to
- [Driving Variables (Forces)](../foundations/forces.md) — Force evaluation definitions
- [Tradeoff Catalog](tradeoffs.md) — Selection criteria for either-or decisions
- [Degree Catalog](tuning-dials.md) — Guideline values for dials
