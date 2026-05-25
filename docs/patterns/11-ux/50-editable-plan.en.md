---
title: "Editable Plan"
tags:
  - "UI/UX & Human Collaboration"
  - "F6 Task Variability"
---

# #50 Editable Plan

!!! abstract "TL;DR"
    Allow humans to review, edit, reorder, and delete steps in the agent's generated execution plan before it runs.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #50 Editable Plan</summary>

| Field | Value |
|------|-----|
| **ID** | 50 |
| **Category** | 11-ux — UI/UX & Human Collaboration |
| **Forces** | `[F6]` |
| **Dials** | — |
| **Tradeoffs** | plan-vs-react |
| **Related Patterns** | #49, #8, #51 |
| **When to Use** | Multi-step, variable procedures, high re-execution cost |
| **When Not to Use** | 1-2 step automation; real-time zero-review required; fully autonomous batch |
| **Element Technologies** | JSON/YAML plan structure, drag & drop, inline editing, re-planning proposal loop |

</details>
<!-- END:GEN:meta -->

## Overview

You asked an agent to "create a competitive analysis report," but it started researching the wrong information sources and the report that came back 30 minutes later was off-target -- a failure that could have been prevented if the plan had been reviewed before execution.

When an agent receives a task, it internally generates an execution plan (a sequence of steps). Rather than "executing immediately as a black box," the plan is presented to the user with an opportunity to edit. By accepting additions, deletions, reordering, and parameter modifications before execution, the agent's judgment errors can be corrected before they happen. The more exploratory the task, the less accurate the plan tends to be `[F6]`, making human corrections highly valuable.

!!! info "Position in decision-making"
    - **Driving force**: `[F6]` Task Variability
    - **Related decision**: Plan vs. ReAct in [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

1. User gives a task instruction
2. Agent generates a plan and returns it to the UI as structured data (JSON / YAML)
3. UI displays the plan as a step list. Each step can be edited, deleted, and reordered
4. When the user clicks "Execute," the agent operates on the edited plan
5. If plan changes are needed during execution, the agent proposes a re-plan and accepts edits again

The plan structure is schematized with [#14 Structured Output Contract](../03-io-contract/14-structured-output-contract.md) to serve as the contract between UI and agent.

## Problems Solved

Agent planning capability is not infallible -- particularly for unknown domains or complex tasks, plans may contain inappropriate steps `[F6]`. Discovering errors after execution incurs the cost of rolling back side effects. If humans can review and modify the plan before execution, the cost of such trial and error can be significantly reduced.

## When to Use / When Not to Use

- **When to Use**: Multi-step tasks where step order and content significantly affect outcomes. Workflows with side effects where redo costs are high.
- **When Not to Use**: Tasks with obvious 1-2 step plans. Cases requiring real-time execution where waiting for human edits is unacceptable. Fully autonomous batch processing.

## Element Technologies

- Plan format: JSON / YAML with structured steps (title, description, tool, parameters)
- UI: Drag & drop step editor, inline editing
- Re-planning: Feedback loop where the agent proposes plan changes during execution

## Related Patterns

- [#49 Agent Workbench](49-agent-workbench.md) — Implemented as the plan panel within the Workbench
- [#8 Planner-Executor-Reviewer](../02-composition/08-planner-executor-reviewer.md) — Human edits the Planner's generated plan before passing to Executor
- [#51 Agent-to-Human Escalation](51-agent-to-human-escalation.md) — Escalation when re-planning is needed during execution

## References

- GitHub Copilot Workspace plan step editing UI
