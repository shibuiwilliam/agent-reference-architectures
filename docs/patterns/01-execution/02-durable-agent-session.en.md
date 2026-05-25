---
title: "Durable Agent Session"
tags:
  - "Execution, Session & Orchestration"
  - "F1 Reversibility"
---

# #2 Durable Agent Session

!!! abstract "TL;DR"
    Persist agent execution state to an external store so that processing can resume from where it left off after process failures, restarts, or interruptions.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #2 Durable Agent Session</summary>

| Field | Value |
|------|-----|
| **ID** | 2 |
| **Category** | 01-execution — Execution, Session & Orchestration |
| **Forces** | `[F1]` |
| **Dials** | checkpoint-frequency |
| **Tradeoffs** | in-context-vs-external |
| **Related Patterns** | #1, #6, #4, #32 |
| **When to Use** | Multi-step research, code generation, data pipelines, rolling deployment environments |
| **When Not to Use** | Single-shot LLM calls; real-time conversations where serialization cost outweighs benefit |
| **Element Technologies** | Redis, PostgreSQL, DynamoDB, Temporal, Azure Durable Functions, JSON/Protobuf |

</details>
<!-- END:GEN:meta -->

## Overview

If a process crashes while an agent is midway through a research task that has been running for tens of minutes, everything must be restarted from scratch — this is unacceptable in production environments.

This pattern writes agent session state (conversation history, intermediate results, step counters, retrieved context) to an external durable store rather than keeping it in-memory. This allows state to be restored from the store after a process crash, resuming from the last checkpoint. Furthermore, since stateless workers can pick up any session, this approach is also compatible with scale-out and rolling deployments.

!!! info "Position in Decision Framework"
    - **Driving Forces**: `[F1]` Reversibility
    - **Related Decisions**: [Tuning Dials](../../decisions/tuning-dials.md) — Checkpoint Frequency
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

```mermaid
flowchart LR
    W[Agent Worker] -->|"read/write"| SS[(Session Store)]
    W -->|"checkpoint"| CP[Checkpoint Log]
    LB[Load Balancer] -->|"route to any worker"| W
    SS -->|"restore"| W2[Another Worker (resume)]
```

Session state is written to the store at the completion of each step (checkpoint). The key is `session_id`, with a TTL attached to automatically expire old sessions. On restoration, the latest checkpoint is loaded, and idempotency keys are used for steps with side effects to prevent duplicate execution.

## Problem Solved

Agent execution can span minutes to tens of minutes, during which process crashes, deployments, or spot instance reclamation may occur. If state exists only in memory, users must start over from the beginning. From the perspective of `[F1]` Reversibility, the ability to resume without losing intermediate results is a prerequisite for production operation.

## When to Use / When Not to Use

- **When to Use**: Suitable for multi-step research, code generation, data pipelines, and other tasks where completion takes time and intermediate results have value. Also effective when sessions need to continue during rolling deployments.
- **When Not to Use**: Excessive for simple Q&A that completes in a single LLM call. Also not suited for real-time conversations where state serialization cost does not justify the latency impact.

## Element Technologies

- Store: Redis (fast, with volatility risk), PostgreSQL / DynamoDB (durability-first)
- Checkpoint: Temporal Workflow continuation, Durable Functions checkpoint, or custom UPSERT on step completion
- Idempotency: Assign idempotency keys to side-effect steps to prevent double processing on replay
- Serialization: JSON/Protobuf serialization of session state. Raw LLM token streams are not persisted; summaries are stored instead

## Tuning (Dials)

- **Checkpoint frequency** — Recording every step increases I/O overhead. On the other hand, checkpointing too infrequently leads to large rollbacks on failure / Deciding factor: `[F1]` / Guideline: checkpoint before and after steps with side effects; batch read-only steps every few iterations. → [Tuning Dials](../../decisions/tuning-dials.md)

## Related Patterns

- [#1 Request-to-Job Gateway](01-request-to-job-gateway.md) — This pattern persists the state of async jobs separated from the acceptance tier
- [#6 Interruptible Agent](06-interruptible-agent.md) — After receiving an interrupt signal, resumes from this pattern's state
- [#4 Agent Saga](04-agent-saga.md) — Compensating transactions are only possible because persisted state exists
- [#32 Agent Trace](../07-observability/32-agent-trace.md) — Checkpoint logs can also serve as part of the trace for auditing

## References

- Temporal.io Workflow Durable Execution model
- Azure Durable Functions checkpoint mechanism
