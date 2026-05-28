---
title: Dial x Tradeoff Interactions
---

# Dial x Tradeoff Interactions

!!! abstract "TL;DR"
    Dials and tradeoffs are not independent — they are **interlinked**. A choice in one changes the value range of the other.

## Why Be Aware of Interactions?

"Choosing async increased timeout flexibility, but now checkpoint design became necessary" — situations where one decision changes the premises of another occur frequently in practice.

[Degree (Dials)](tuning-dials.md) and [Tradeoffs (Either-Or)](tradeoffs.md) are organized in separate catalogs, but in actual design they are **interlinked**. Resolving one either-or changes the value ranges of related dials, and further alters the premises of other either-or decisions. Without awareness of this chain, designs that appear individually rational may become contradictory as a whole.

## Key Interactions

### What Sync vs. Async Changes

| Either-Or Selection | Affected Dials/Tradeoffs | Effect |
|---|---|---|
| **Choose Async** | Timeout ceiling | Can extend to minutes or tens of minutes |
| | Checkpoint frequency | Design required assuming long-running execution |
| | Push vs. Pull | Progress notification design becomes mandatory |
| **Choose Sync** | Timeout ceiling | Constrained to 5–10 seconds |
| | Self-correction loop count | 1 or fewer (latency constraint) |

→ [#1 Request-to-Job Gateway](../glossary.md), [#58 Sync Facade](../glossary.md)

### What Multi-Agent Changes

| Either-Or Selection | Affected Dials/Tradeoffs | Effect |
|---|---|---|
| **Choose Multi-Agent** | Budget cap | Grows to agent count x per-agent budget |
| | Trace sampling rate | Observation cost multiplied by N; layer separation required |
| | Exposed tool count | Need to limit per agent |
| | Orchestration vs. Choreography | A new either-or decision arises |

→ [#9 Supervisor & Specialist](../glossary.md), [#55 Deadline & Budget Cascade](../glossary.md)

### What Inline Verification Changes

| Either-Or Selection | Affected Dials/Tradeoffs | Effect |
|---|---|---|
| **Choose Inline Verification** | Self-correction loop count | Competes with latency budget `[F4]` |
| | Guardrail strictness | False positives directly increase latency |
| | Same vs. Different-Model Verification | Different model doubles latency and cost |
| **Choose Post-hoc Verification** | Log retention period | Need to retain data for verification |
| | Retry count | Retry strategy changes on verification failure |

→ [#28 Verifier Agent](../glossary.md), [#29 Guardrail Sidecar](../glossary.md)

### What Plan-First Changes

| Either-Or Selection | Affected Dials/Tradeoffs | Effect |
|---|---|---|
| **Choose Plan-First** | HITL frequency | Enables human review at the planning stage (reduces runtime HITL) |
| | Autonomy level | Can increase runtime autonomy when plan is approved |
| | Workflow vs. Agent | Execution following a plan leans toward workflow |
| **Choose ReAct** | Self-correction loop count | Correction needed at each step; count increases |
| | Timeout | Exploratory nature makes prediction difficult; add margin |

→ [#8 Planner-Executor-Reviewer](../glossary.md), [#50 Editable Plan](../glossary.md)

### What Cost Optimization Choices Cascade

| Either-Or Selection | Affected Dials/Tradeoffs | Effect |
|---|---|---|
| **Introduce Model Routing** | Best-of-N | N=1 is sufficient for requests routed to smaller models |
| | Cache similarity threshold | Dual optimization of routing and caching becomes possible |
| | Temperature | Lower temperature for smaller models (stability-focused) |
| **Introduce Caching** | Memory TTL | Need alignment between cache TTL and long-term memory TTL |

→ [#37 Semantic Gateway](../glossary.md), [#38 Semantic Result Cache](../glossary.md)

## How to Handle Interactions

1. **Resolve either-or decisions first**: Since either-or selections determine dial value ranges, consult the [Tradeoff Catalog](tradeoffs.md) first
2. **Trace the chain**: Check the tables above for downstream effects and reconsider guideline values for related dials
3. **Detect contradictions**: Verify there are no mutually contradictory requirements such as "inline verification + low latency + multi-step self-correction"
4. **Record tradeoffs**: Document which interaction led to which priority in an [ADR](adr-template.md)

## Related Pages

- [Decision-Making Process](decision-flow.md) — Decision flow that accounts for interactions
- [Degree (Dial) Catalog](tuning-dials.md) — Guideline values for individual dials
- [Tradeoff (Either-Or) Catalog](tradeoffs.md) — Selection criteria for individual either-or decisions
- [Worked Examples](worked-examples.md) — Examples including interactions
