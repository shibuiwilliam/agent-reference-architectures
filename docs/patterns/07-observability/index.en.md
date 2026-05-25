# VII. Observability, Auditing & Evaluation


!!! tip "Key decisions for this concern"
    - **Primary forces**: `[F8]` Accountability, `[F7]` Cost Sensitivity, `[F9]` Provider Reliability
    - **Key dials**: Trace sampling rate, Log retention period, Prompt storage granularity → [Tuning Dials](../../decisions/tuning-dials.md)
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

When an agent returns an incorrect answer in production, improvement becomes guesswork if you cannot trace "why it happened." You also cannot detect when a model update degrades quality. These patterns enable observing, reproducing, and detecting regressions in non-deterministic behavior, and managing behavioral changes that come with deployments in a disciplined manner.

- [#32 Agent Trace](32-agent-trace.md) — Record all steps as append-only logs for replay
- [#54 Tiered (Hot/Cold) Observability](54-tiered-observability.md) — Manage observability data across hot and cold tiers
- [#33 Prompt/Model/Tool Version Pinning](33-version-pinning.md) — Pin prompt, model, and tool versions
- [#34 Evaluation CI/CD](34-evaluation-ci-cd.md) — Run automated evaluations on every change to detect regressions
- [#35 Production Replay](35-production-replay.md) — Replay production logs to compare old and new version differences
- [#36 Shadow / Canary Deployment](36-shadow-canary-deployment.md) — Deploy incrementally and auto-rollback on issues
