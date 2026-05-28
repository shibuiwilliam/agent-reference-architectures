---
title: "[C3] Side Effects on the External World"
tags:
  - "Characteristics"
---

# [C3] Side Effects on the External World

!!! abstract "Summary"
    Agents modify the external world through tool calls -- sending emails, updating databases, calling APIs -- and autonomously execute operations that cannot be undone.

## Overview

In traditional software, side-effect locations were explicitly managed in code. AI agents select and execute tools based on LLM judgment, making it impossible to determine which side effects occur and when through code review alone. Moreover, many side effects are irreversible -- "undo it because it was wrong" may be physically impossible.

## Why This Is a Problem

An agent sends an email to a hallucinated recipient. It references a non-existent ticket ID in a database update, causing data inconsistency. It makes consecutive calls that exceed an external API's rate limit, getting the account banned. When a multi-step process fails partway through, only the earlier side effects persist, breaking business consistency (e.g., a calendar reservation was made but the ticket was not created). These are not problems that "get solved when the agent gets smarter" -- they require structural defense.

## Comparison with Traditional Software

| Aspect | Traditional Software | AI Agent |
|--------|---------------------|----------|
| Side-effect locations | Statically determined in code | Dynamically determined by LLM judgment |
| Transaction management | DB ACID / 2PC | ACID is unavailable across external APIs |
| Rollback on failure | Framework handles automatically | Compensating transactions must be explicitly designed |
| Testing | Mock substitution is sufficient | Tool call patterns are non-deterministic |

## Affected Forces

- `[F1]` Reversibility -- The more irreversible the operations, the greater the importance of pre-confirmation and dry runs
- `[F2]` Failure Cost -- Side effects that directly impact finances, legal standing, or safety require approval gates
- `[F5]` Input Trust -- Side effects triggered from untrusted input become Confused Deputy attacks

## Safeguard Patterns

- [#4 Agent Saga](../../decisions/dials/checkpoint-frequency.md) -- Embed compensating transactions into side-effect chains to roll back on partial failure
- [#19 Dry-Run First](../../foundations/forces/f1-reversibility.md) -- Simulate execution to confirm the blast radius before proceeding, then execute after approval
- [#31 Human Approval Checkpoint](../../decisions/dials/autonomy-level.md) -- Require human approval before high-risk side effects

## Related Design Decisions

- [autonomy-level](../../decisions/dials/autonomy-level.md) -- Higher autonomy means more automated side-effect execution and greater risk
- [hitl-frequency](../../decisions/dials/hitl-frequency.md) -- Where to set the frequency of human intervention
- [checkpoint-frequency](../../decisions/dials/checkpoint-frequency.md) -- Checkpoint interval determines the granularity of compensating transactions
