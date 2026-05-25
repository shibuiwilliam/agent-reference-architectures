---
title: Pattern Parameterization
---

# Pattern Parameterization

!!! abstract "TL;DR"
    Patterns are not constants — treat them as **functions** that take driving variables as arguments and return optimal settings.

## What Is Parameterization?

The question "should we adopt this pattern or not?" is often too coarse in the first place. Treating architecture patterns as a binary "apply/don't apply" tends to result in either over-application or under-application. In practice, it is more appropriate to think of patterns as **functions that take driving variables `[F#]` as arguments and return concrete design parameters**.

```
Design Parameters = f(F1, F2, …, F9)
```

We call this approach "pattern parameterization."

## Concrete Examples

### Example 1: Checkpoint Frequency for #2 Durable Agent Session

[#2 Durable Agent Session](../patterns/01-execution/02-durable-agent-session.md) is a pattern for persisting state, but "how frequently to take checkpoints" needs to be tuned as a parameter.

- `[F1]` Reversibility is **Low** (many irreversible side effects) → Checkpoint **every step**
- `[F1]` Reversibility is **High** (all steps can be redone) → **Every N minutes** is sufficient
- `[F7]` Cost Sensitivity is **High** → Widen interval to reduce I/O

In other words, `Checkpoint Frequency = f(F1, F7)`: the lower F1, the higher the frequency; the higher F7, the lower the frequency. If both are high, a tradeoff judgment is needed (→ [Criteria for Selecting Between Opposing Mechanisms](tradeoffs.md)).

### Example 2: Sampling Rate for #32 Agent Trace

[#32 Agent Trace](../patterns/07-observability/32-agent-trace.md) is a pattern for logging every step, but recording 100% in production significantly inflates storage costs.

- `[F8]` Accountability is **High** (regulated industry) → Sampling rate **100%** (full recording is mandatory)
- `[F8]` is **Low** + `[F7]` Cost Sensitivity is **High** → Limit to **1–10%**
- Dynamic sampling that raises to 100% only during anomaly detection is also an option

### Example 3: Routing Threshold for #37 Semantic Gateway

[#37 Semantic Gateway](../patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) is a pattern that routes to different models based on difficulty, and "at what threshold to route to the larger model" becomes the parameter.

- `[F7]` Cost Sensitivity is **High** → **Raise** the threshold to reduce large model usage
- `[F3]` Per-Request Value is **High** → **Lower** the threshold to prioritize quality

## The Practice of Parameterization

1. **Identify parameters**: The dials listed in each pattern's "Tuning (Degree)" section are parameter candidates (→ [Degree Dials](tuning-dials.md))
2. **Map driving variables**: Identify which `[F#]` affects each parameter
3. **Set guideline values**: Determine starting points based on "High/Medium/Low" force ratings
4. **Run the measure-and-adjust loop**: Update values based on production metrics
5. **Record the rationale**: Document why each value was chosen in design documents or traces (→ [#32 Agent Trace](../patterns/07-observability/32-agent-trace.md))

## Risks of Not Parameterizing

Setting values based on "gut feeling" without recording the rationale tends to cause the following problems:

- **Inability to tune**: When problems occur, it's unclear what to change
- **Knowledge silos**: The intent behind settings exists only in one person's head
- **Over/under-application**: Settings don't adapt when forces change

This itself is an anti-pattern, corresponding to [Anti-pattern: No Rationale for Dial Settings](../anti-patterns/06-no-rationale.md).

## Summary

When adopting a pattern, it is important to explicitly state three things: "what are this pattern's parameters?", "which forces determine them?", and "what are the current values and their rationale?" Only when these three points are in place does a pattern function as an operationally viable design decision.
