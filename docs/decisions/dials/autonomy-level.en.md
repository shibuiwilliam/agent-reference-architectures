---
title: "Autonomy Level"
tags:
  - "Tuning Dial"
  - "F2 Failure Cost"
  - "F1 Reversibility"
---

# Autonomy Level

!!! abstract "TL;DR"
    Progressively control how far an agent can act without human approval.

## Overview

"We let the agent handle it, and it deleted records from the production database on its own" -- stories of excessive autonomy going wrong are not uncommon. On the other hand, requiring human approval for everything defeats the purpose of automation.

This dial determines the scope of actions permitted to the agent. It ranges from "propose only" to "fully autonomous execution" with multiple levels in between, adjustable up or down based on task type, track record, and risk. Higher autonomy increases throughput but also amplifies damage when things go wrong.

## Why Adjustment Is Needed

Requiring human approval for every operation causes delays that negate the value of agent adoption. Conversely, granting full autonomy from the start risks irreversible operations on unknown edge cases. Without a mechanism for gradual privilege escalation, you are stuck choosing between "convenient but dangerous" and "safe but slow."

## Extremes of the Range

### Too Small

Every operation waits for human approval, and the agent's processing speed is bottlenecked by human response time. Processing halts during nights and weekends, losing the benefits of asynchronous workflows. There is also the danger of approval fatigue leading to rubber-stamped "approve all."

### Too Large

The agent executes irreversible operations such as data deletion, fund transfers, or external notifications on incorrect judgments. Granting high privileges without resilience to hallucinations or prompt injection results in severe damage during incidents.

## Determining Forces

- `[F2]` Failure Cost -- The greater the financial, legal, or safety impact of failure, the lower the autonomy should be
- `[F1]` Reversibility -- If operations are reversible, autonomy can be set higher

## Guidelines (Starting Point)

- Initial deployment: Start at the lowest level (propose only)
- Escalate gradually as successful track records accumulate (e.g., next level after 100 successes)
- Irreversible operations (deletion, fund transfer, external sending): Always require approval, or at least drop one level
- Dynamically adjusting autonomy by time of day or day of week is also effective

## Practical Adjustment

- Record autonomy level as metadata and track success rate and incident rate per level
- Explicitly define escalation conditions (N consecutive successes) and demotion conditions (1 critical failure)
- When new operation types are added, reset autonomy to the lowest level
- Periodically review the appropriateness of autonomy levels to keep up with environmental changes

## Related Patterns

- [#57 Autonomy Ladder](../../glossary.md) -- Implementation pattern for track-record-based gradual autonomy escalation
