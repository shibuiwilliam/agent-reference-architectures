---
title: "[F1] Reversibility"
tags:
  - "Driving Variables"
---

# [F1] Reversibility

!!! abstract "Summary"
    A force that measures whether failures can be "undone." The more irreversible side effects there are, the more defensive design becomes essential.

## Overview

An agent accidentally sends a quote email to a customer -- a database record can be rolled back, but a sent email cannot be recalled. This question of "whether you can redo it" significantly influences the depth of safety measures required by the architecture.

Reversibility represents the degree to which side effects caused by an agent can be undone after the fact. This difference determines the depth of safety measures the architecture demands.

## Why It Matters

If you design without considering reversibility, agent hallucinations or erroneous tool calls produce **irreversible consequences**. For example, sending a contract email to the wrong recipient or calling a payment API with the wrong amount are incidents that cannot be resolved by post-hoc log analysis or apologies. Systems containing operations with low reversibility require structural safeguard layers such as pre-execution verification, approval gates, and dry runs.

## Interpreting the Value Range

### When Low

Situations where the majority of operations involve irreversible side effects. Examples include sending to external APIs (email, SMS, webhooks), confirming financial transactions, controlling physical devices, and submitting legal documents. Once executed, they can only be partially undone through compensating transactions, which themselves carry costs. This range strongly calls for Human-in-the-Loop and dry-run-first execution.

### When High

Situations where operations can be easily redone. Typical examples include writes to internal databases (with transactions), draft document generation, and read-centric tasks like search and summarization. Failures can be retried, and the actual harm to users is minimal. In this case, guardrails can be kept lightweight, prioritizing throughput and latency.

## Evaluation Guidelines

- Are there any operations among the tools/APIs the agent calls that cannot be undone after execution?
- To what degree can damage be recovered through compensating transactions (refunds, cancellation notices, etc.)?
- How long does it take from when an erroneous operation is discovered to when it is corrected?
- Can side effects be simulated in a test environment or sandbox?
- Is it safe to execute the same request multiple times (is idempotency guaranteed)?

## Influenced Design Decisions

### Related Dials

- [Retry Count](../../decisions/dials/retry-count.md) -- When reversibility is high, retries can be set aggressively. When low, zero retries or only after dry run
- [Autonomy Level](../../decisions/dials/autonomy-level.md) -- Lower autonomy level for operations with low reversibility, inserting human approval
- [Checkpoint Frequency](../../decisions/dials/checkpoint-frequency.md) -- Taking checkpoints before irreversible operations enables partial rollback
- [HITL Frequency](../../decisions/dials/hitl-frequency.md) -- The lower the reversibility, the more approval gates should be added

### Related Tradeoffs

- [Sync vs. Async](../../decisions/tradeoffs-catalog/sync-vs-async.md) -- Make irreversible operations async to facilitate approval waiting
- [Workflow vs. Agent](../../decisions/tradeoffs-catalog/workflow-vs-agent.md) -- The more irreversible steps there are, the safer workflow-oriented control becomes
- [Inline vs. Post Verification](../../decisions/tradeoffs-catalog/inline-vs-post-verification.md) -- When reversibility is low, prioritize inline (pre-execution) verification

## Related Patterns

- [#4 Agent Saga](../../decisions/dials/checkpoint-frequency.md) -- Roll back irreversible side-effect chains with compensating transactions
- [#19 Dry-Run First Tool Execution](../../foundations/forces/f1-reversibility.md) -- Simulate side effects first, then execute after approval
- [#31 Human Approval Checkpoint](../../decisions/dials/autonomy-level.md) -- Obtain human approval before high-risk operations
- [#57 Autonomy Ladder](../../decisions/dials/autonomy-level.md) -- Gradually promote autonomy based on track record
- [#16 Ambiguity Negotiation](../../foundations/forces/f1-reversibility.md) -- Confirm before executing irreversible operations on ambiguous instructions
