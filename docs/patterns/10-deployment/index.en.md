# X. Deployment, Vendor Abstraction & Migration


!!! tip "Key decisions for this concern"
    - **Primary forces**: `[F9]` Provider Reliability, `[F8]` Accountability, `[F2]` Failure Cost
    - **Key tradeoffs**: Build vs. buy, Single vs. multi-provider → [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

The agent framework you chose six months ago has stalled in development, the LLM provider changed its pricing, you want to integrate AI into existing business systems but a wholesale replacement is too risky -- these situations arise frequently in production. These patterns address avoiding lock-in to specific SDKs or models and enabling incremental adoption into existing systems.

- [#45 Agent Runtime Abstraction](45-agent-runtime-abstraction.md) — Make the execution platform swappable
- [#46 Model Behavior Compatibility Layer](46-model-behavior-compatibility-layer.md) — Insert a compatibility layer to absorb cross-model differences
- [#47 Agent Capability Registry](47-agent-capability-registry.md) — Centrally manage capabilities, permissions, and costs in a registry
- [#48 Strangler Fig](48-strangler-fig.md) — Incrementally replace existing processing with agents
