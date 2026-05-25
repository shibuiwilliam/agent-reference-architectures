---
title: "Autonomy Ladder"
tags:
  - "Reliability, Verification, Guardrails & Autonomy"
  - "F1 Reversibility"
  - "F2 Failure Cost"
---

# #57 Autonomy Ladder

!!! abstract "TL;DR"
    **Define agent autonomy levels in graduated steps**, promoting and demoting based on track record and trust.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #57 Autonomy Ladder</summary>

| Field | Value |
|------|-----|
| **ID** | 57 |
| **Category** | 06-reliability — Reliability, Verification, Guardrails & Autonomy |
| **Forces** | `[F1]`, `[F2]` |
| **Dials** | autonomy-level |
| **Tradeoffs** | — |
| **Related Patterns** | #31, #5, #51 |
| **When to Use** | Graduated rollout of agent permissions, task types with varying risk levels |
| **When Not to Use** | Fixed requirements (always L1 or L3); insufficient task volume for statistics |
| **Element Technologies** | Feature Flag (LaunchDarkly/Unleash), success/failure counters, confidence interval scoring |

</details>
<!-- END:GEN:meta -->

## Overview

You would not give full authority to a newly hired employee immediately. First, you have them make proposals, a supervisor approves, and authority gradually expands as track record develops. Agent autonomy can be managed with the same approach. Granting full autonomy from the start is high risk, but requiring human approval for everything eliminates the value of automation. Autonomy Ladder defines autonomy levels as explicit steps (e.g., L0 propose only → L1 execute after approval → L2 auto-execute with post-notification → L3 fully automatic) and introduces a mechanism to move levels up and down based on the agent's track record, success rate, and failure history.

!!! info "Position in Decision Framework"
    - **Driving Forces**: `[F1]` Reversibility, `[F2]` Failure Cost
    - **Related Decisions**: [Tuning Dials](../../decisions/tuning-dials.md) — Autonomy Level
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

| Level | Behavior | Human Involvement |
|--------|------|------------|
| L0 | Present proposals only | Human executes everything |
| L1 | Present execution plan, execute after approval | Pre-approval |
| L2 | Auto-execute, notify afterward | Post-review |
| L3 | Fully automatic. Notify only on anomalies | Exception-only |

Promotion conditions are defined quantitatively (e.g., promote from L1 → L2 when the success rate for the last 100 tasks exceeds 95%). Demotion conditions are similarly defined (e.g., immediate demotion on serious incident), and it is important not to make it one-directional. Levels are managed independently per task type — for example, "email drafting is L2 but fund transfers are L1."

## Problem Solved

Treating autonomy as all-or-nothing means either the agent cannot scale until its capability is proven `[F1]`, or authority is granted without proof and leads to accidents `[F2]`. With a ladder approach: (1) risk is limited during initial introduction, (2) trust accumulation is quantitatively managed, and (3) permissions can be immediately tightened when problems occur. This gradually resolves the common organizational adoption state of "too scary, so everything is manual."

## When to Use / When Not to Use

- **When to Use**: Suitable for business processes where automation scope should be gradually expanded, and multi-task agents where risk levels differ by task.
- **When Not to Use**: Unnecessary when all tasks are the same risk and always require human oversight (L1 fixed is sufficient). Also less effective when task volume is too low for statistical confidence assessment.

## Element Technologies

- Level Management: Configuration DB / Feature Flags (LaunchDarkly, etc.)
- Track Record: Success/failure/incident counters, scoring models
- Promotion/Demotion Logic: Rule-based (thresholds), or statistical confidence intervals
- Notification: Alerts on level changes, dashboard display

## Tuning (Dials)

- **Promotion threshold** — Too low promotes prematurely; too high keeps agents at L0 forever / Deciding factors: `[F1][F2]` / Vary threshold by task irreversibility. → [Tuning Dials](../../decisions/tuning-dials.md)

## Selection (Tradeoffs)

- **Autonomy ↔ Human Control** — Where to set the agent's autonomy level is this pattern's core decision `[F1][F2]`. → [Tradeoff Selection Criteria](../../decisions/tradeoffs.md)

## Related Patterns

- [#31 Human Approval Checkpoint](31-human-approval-checkpoint.md) — The concrete implementation mechanism for L1 level
- [#5 Time-Budgeted Agent Loop](../01-execution/05-time-budgeted-agent-loop.md) — Adjust budgets according to autonomy level
- [#51 Agent-to-Human Escalation](../11-ux/51-agent-to-human-escalation.md) — Human handoff for situations exceeding the autonomy level
