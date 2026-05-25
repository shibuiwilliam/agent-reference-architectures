---
title: "[F6] Task Variability"
tags:
  - "Driving Variables"
---

# [F6] Task Variability

!!! abstract "Summary"
    A force that measures whether tasks are routine or exploratory. The higher the variability, the more agent autonomy is needed; the lower it is, the more a workflow suffices.

## Overview

If processing invoices follows a standard procedure, you can chart it as a flowchart. But investigating an unknown bug requires deciding which files to read, which logs to trace, and who to ask -- all while executing. This "can you determine the procedure in advance?" is the fork between workflows and agents.

Task variability represents the predictability of processing steps. This force determines the fundamental fork of "how much judgment to delegate to the LLM."

## Why It Matters

Introducing agent autonomous judgment to low-variability tasks invites unnecessary hallucination risk and cost. Conversely, forcing high-variability tasks into fixed workflows results in frequent errors on unexpected cases. A mismatch between task nature and control structure degrades both reliability and cost.

## Interpreting the Value Range

### When Low

Situations where procedures are fixed and input variations are limited. Examples include routine invoice processing, data conversion of known formats, template-based notification generation, and periodic report aggregation. Branch conditions can be enumerated in advance, and workflow engines or rule-based processing are sufficient. LLMs are used only for specific natural language processing nodes.

### When High

Situations where the procedure itself cannot be determined in advance and must be planned during execution. Typical examples include open-ended research, unknown bug investigation, complex requirements code generation, and multi-stage negotiations. The agent must autonomously select needed tools, determine execution order, and make termination decisions, requiring Plan-and-Execute or ReAct-style loops.

## Evaluation Guidelines

- Can the task's processing steps be described in a flowchart in advance?
- Are the types of input patterns finite, or nearly infinite?
- What percentage of past requests were "unexpected" cases?
- Does dynamic external information retrieval or additional tool calls become necessary during processing?
- When different people handle the same task, do their procedures differ significantly?

## Influenced Design Decisions

### Related Dials

- [Autonomy Level](../../decisions/dials/autonomy-level.md) -- Higher variability calls for higher agent autonomy
- [Exposed Tool Count](../../decisions/dials/exposed-tool-count.md) -- Increase available tools for exploratory tasks
- [Temperature](../../decisions/dials/temperature.md) -- Raise temperature for exploratory tasks to get diverse outputs

### Related Tradeoffs

- [Workflow vs. Agent](../../decisions/tradeoffs-catalog/workflow-vs-agent.md) -- Workflow for low variability, agent for high variability
- [Plan vs. React](../../decisions/tradeoffs-catalog/plan-vs-react.md) -- Plan-driven for moderate variability, reaction-driven for extremely high variability
- [Orchestration vs. Choreography](../../decisions/tradeoffs-catalog/orchestration-vs-choreography.md) -- Choreography can be advantageous when variability is high and participants are many
- [Structured vs. Freeform](../../decisions/tradeoffs-catalog/structured-vs-freeform.md) -- Structured I/O is sufficient for routine tasks; exploratory tasks need freeform

## Related Patterns

- [#3 Workflow Backbone + Agent Node](../../patterns/01-execution/03-workflow-backbone-agent-node.md) -- Workflow as the backbone, delegating only decision-requiring nodes to agents
- [#59 Workflow-Agent Spectrum Selector](../../patterns/01-execution/59-workflow-agent-spectrum-selector.md) -- Select the determinism vs. autonomy balance per subtask
- [#12 Blackboard](../../patterns/02-composition/12-blackboard.md) -- Multiple agents coordinate via a shared blackboard for exploratory tasks
- [#50 Editable Plan](../../patterns/11-ux/50-editable-plan.md) -- Humans edit the agent's plan before execution
- [#9 Supervisor & Specialist Agents](../../patterns/02-composition/09-supervisor-specialist-agents.md) -- Dynamically delegate high-variability tasks to specialist agents
