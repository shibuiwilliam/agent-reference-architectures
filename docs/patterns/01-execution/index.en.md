# I. Execution, Session & Orchestration


!!! tip "Key decisions for this concern"
    - **Primary Forces**: `[F4]` Latency Budget, `[F1]` Reversibility, `[F7]` Cost Sensitivity
    - **Primary Dials**: Timeout, Checkpoint Frequency, Budget Cap → [Tuning Dials](../../decisions/tuning-dials.md)
    - **Primary Tradeoffs**: Sync ↔ Async, Workflow ↔ Agent → [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

When delegating tasks to AI agents, execution may finish in seconds or take tens of minutes, and processes can crash midway or users may want to change direction. These patterns provide the foundation for safely executing such unpredictable, long-running tasks by decoupling them from the web tier.

- [#1 Request-to-Job Gateway](01-request-to-job-gateway.md) — Accept a single request as an asynchronous job
- [#2 Durable Agent Session](02-durable-agent-session.md) — Persist state to withstand interruption and resumption
- [#3 Workflow Backbone + Agent Node](03-workflow-backbone-agent-node.md) — Keep the overall skeleton deterministic, delegating only judgment-requiring parts to agents
- [#4 Agent Saga](04-agent-saga.md) — Make chains of side effects reversible through compensating actions
- [#5 Time-Budgeted Agent Loop](05-time-budgeted-agent-loop.md) — Set budgets for time, iterations, and cost to prevent runaway execution
- [#6 Interruptible Agent](06-interruptible-agent.md) — Allow mid-execution stops and course corrections
- [#7 Streaming Progress](07-streaming-progress.md) — Incrementally display execution progress as auditable summaries
- [#55 Deadline & Budget Cascade](55-deadline-budget-cascade.md) — Propagate deadlines and budgets across the entire call tree
- [#58 Sync Facade over Async Core](58-sync-facade-over-async-core.md) — Return short tasks synchronously, promoting to async when a threshold is exceeded
- [#59 Workflow–Agent Spectrum Selector](59-workflow-agent-spectrum-selector.md) — Select the balance between determinism and autonomy per sub-task
