---
title: Driving Variables (Forces)
---

# Driving Variables (Forces) F1--F9

!!! abstract "Summary"
    Nine environmental variables that determine the "degree" and "selection" of patterns. Even for the same pattern, the optimal implementation differs as force values change.

## What Are Forces

Even when told "use this pattern and it will work," you often wonder how far to apply it to your own system. Forces (driving variables) help make that judgment.

Architecture patterns are not fixed recipes; think of them as **functions that take environmental variables as arguments**. These environmental variables -- driving variables (forces) -- quantify or rank the context in which the system operates (e.g., "what happens when it fails," "how long can the user wait"). "To what degree to apply a pattern" ([Degree Dials](../decisions/tuning-dials.md)) and "which one to choose" ([Tradeoff Selection Criteria](../decisions/tradeoffs.md)) are determined by force values.

## Approach

Forces are **inputs** to decision-making, not outputs (patterns or settings). First estimate forces, then determine dial settings and tradeoff directions based on those values -- this is the fundamental approach of this site's decision-making framework.

Force evaluation can be a subjective estimate. A 3-level scale of "high/medium/low" is sufficient. Aligning team understanding is more important than precise quantification. However, recording the rationale for estimates in an [Architecture Decision Record (ADR)](../decisions/adr-template.md) makes future reviews easier.

## Meaning of the 9 Forces

Forces can be grouped into three categories.

**Risk & Value** (what breaks, what to protect)

| ID | Name | Question | Details |
|----|------|----------|---------|
| `[F1]` | **Reversibility** | Can failures be undone? | [Details -->](forces/f1-reversibility.md) |
| `[F2]` | **Failure Cost** | Financial/legal/safety impact | [Details -->](forces/f2-failure-cost.md) |
| `[F3]` | **Request Value** | Contribution to revenue/decision-making | [Details -->](forces/f3-request-value.md) |

**Constraints & Environment** (what is permitted)

| ID | Name | Question | Details |
|----|------|----------|---------|
| `[F4]` | **Latency Budget** | User's tolerance for waiting | [Details -->](forces/f4-latency-budget.md) |
| `[F5]` | **Input Trust** | Likelihood of attack/contamination | [Details -->](forces/f5-input-trust.md) |
| `[F6]` | **Task Variability** | Routine vs. exploratory | [Details -->](forces/f6-task-variability.md) |
| `[F7]` | **Cost Sensitivity & Scale** | QPS and monthly cost cap | [Details -->](forces/f7-cost-sensitivity.md) |

**Governance & External Dependencies** (whom to explain to)

| ID | Name | Question | Details |
|----|------|----------|---------|
| `[F8]` | **Accountability & Regulation** | Audit and compliance requirements | [Details -->](forces/f8-accountability.md) |
| `[F9]` | **Provider Reliability** | External LLM availability | [Details -->](forces/f9-provider-reliability.md) |

## How to Use

1. **Assess current state**: Estimate F1--F9 for your system as "high/medium/low"
2. **Select patterns**: Prioritize patterns that address areas where forces are high
3. **Adjust degrees**: Tune the dials within selected patterns (timeout values, retry counts, etc.) according to force values (--> [Degree Dials](../decisions/tuning-dials.md))
4. **Judge tradeoffs**: Determine binary design choices based on force combinations (--> [Tradeoff Selection Criteria](../decisions/tradeoffs.md))

## Forces Are Not Static

Forces are not fixed values. Even for the same system, force values can change due to feature additions, user base shifts, or regulatory changes. Therefore, periodic reviews and re-adjustment of pattern application levels are required (--> [#53 Agent Change Management](../foundations/forces/f8-accountability.md)).
