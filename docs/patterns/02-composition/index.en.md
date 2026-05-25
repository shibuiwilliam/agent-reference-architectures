# II. Agent Composition & Division of Labor


!!! tip "Key decisions for this concern"
    - **Primary Forces**: `[F6]` Task Variability, `[F2]` Failure Cost, `[F3]` Per-Request Value
    - **Primary Dials**: Best-of-N → [Tuning Dials](../../decisions/tuning-dials.md)
    - **Primary Tradeoffs**: Single ↔ Multi-Agent, Centralized ↔ Choreography, Plan ↔ ReAct → [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

When a single agent handles everything, prompts bloat, expertise dilutes, and it may overlook its own mistakes. Just as human teams divide roles, these patterns overcome the limitations of agent capabilities and context windows through structural role separation.

- [#8 Planner-Executor-Reviewer](08-planner-executor-reviewer.md) — Separate planning, execution, and review into distinct roles to improve quality
- [#9 Supervisor & Specialist Agents](09-supervisor-specialist-agents.md) — A supervisor delegates tasks to specialists
- [#10 Agent Ensemble & Debate](10-agent-ensemble-debate.md) — Multiple agents solve the same problem; consensus or debate improves robustness
- [#11 Deterministic Core, Probabilistic Edge](11-deterministic-core-probabilistic-edge.md) — Keep the core deterministic, using AI only at the periphery
- [#12 Blackboard](12-blackboard.md) — Loosely coupled coordination through a shared blackboard
