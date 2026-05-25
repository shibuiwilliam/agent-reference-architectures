# XI. UI/UX & Human Collaboration


!!! tip "Key decisions for this concern"
    - **Primary forces**: `[F4]` Latency Budget, `[F6]` Task Variability, `[F2]` Failure Cost
    - **Key tradeoffs**: Plan vs. ReAct → [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

When you assign a 30-minute research task to an agent, simply watching messages scroll by in a chat window leaves you unable to tell "what it is doing now" or "when it needs my judgment." This section covers mechanisms for humans to control long-running, multi-step, side-effect-bearing work that chat alone cannot handle.

- [#49 Agent Workbench](49-agent-workbench.md) — Manage plans, progress, and approvals in a single screen
- [#50 Editable Plan](50-editable-plan.md) — Allow humans to edit the agent's plan before execution
- [#51 Agent-to-Human Escalation](51-agent-to-human-escalation.md) — Hand off to humans when confidence or permissions are insufficient
