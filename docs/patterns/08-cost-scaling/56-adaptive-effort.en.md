---
title: "Adaptive Effort"
tags:
  - "Cost, Performance & Scaling"
  - "F7 Cost Sensitivity & Scale"
  - "F2 Failure Cost"
---

# #56 Adaptive Effort

!!! abstract "TL;DR"
    **Scale the compute investment (reasoning steps, token count, verification rounds) up or down** based on request difficulty and importance.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #56 Adaptive Effort</summary>

| Field | Value |
|------|-----|
| **ID** | 56 |
| **Category** | 08-cost-scaling — Cost, Performance & Scaling |
| **Forces** | `[F7]`, `[F2]` |
| **Dials** | — |
| **Tradeoffs** | — |
| **Related Patterns** | #37, #5, #28 |
| **When to Use** | Workloads with variable difficulty, thinking-budget API available, quality flexibility under cost constraints |
| **When Not to Use** | Uniform complexity; maximum effort always required (medical diagnosis); cost >> quality |
| **Element Technologies** | Lightweight difficulty classifier, Anthropic thinking budget, OpenAI reasoning effort, dynamic max_tokens |

</details>
<!-- END:GEN:meta -->

## Overview

"Tell me tomorrow's schedule" and "Analyze the risks in this contract" require completely different depths of reasoning. Running 5-step verification on the former is wasteful, and handling the latter in a single step is dangerous.

While [#37 Semantic Gateway](37-semantic-gateway-cost-aware-router.md) switches models, Adaptive Effort adjusts the compute investment within the same model. Simple queries get short reasoning and fewer steps for quick answers, while complex or high-risk queries receive deeper Chain-of-Thought, multi-pass verification, and additional tool calls. Rather than "full effort on everything," compute resources are allocated proportionally based on difficulty and failure cost.

!!! info "Position in decision-making"
    - **Driving force**: `[F7]` Cost Sensitivity & Scale, `[F2]` Failure Cost
    - **Related decision**: Model tier in [Tuning Dials](../../decisions/tuning-dials.md)
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

Upon receiving a request, a lightweight difficulty estimation is performed first (input length, complexity score, domain classification). Based on this estimation, the agent's execution parameters are dynamically configured -- specifically, maximum reasoning steps, thinking token budget, whether to activate verifiers, and ensemble count. An escalation mechanism is also built in: if the initial response shows low confidence, it is retried at a higher effort level.

## Problems Solved

Agent compute costs are proportional to step count and token count. Allocating maximum reasoning resources to all requests inflates costs `[F7]`. Conversely, applying uniform limits degrades quality for high-risk requests `[F2]`. Adaptive Effort dynamically optimizes resource allocation to maximize expected quality within the same budget.

## When to Use / When Not to Use

- **When to Use**: Workloads with high difficulty variance, operations with limited cost budgets, environments that can leverage LLM thinking budget features.
- **When Not to Use**: When all requests have equal complexity, the effect is minimal. Also unsuitable for high-risk domains where difficulty estimation errors lead to critical consequences (e.g., medical diagnosis, where maximum effort is always required).

## Element Technologies

- Difficulty estimation: Small classification models, rule-based (input length, keywords), confidence from upstream LLM
- Effort adjustment: Anthropic extended thinking budget, OpenAI reasoning effort, dynamic max_tokens configuration
- Verification scaling: Make [#28 Verifier Agent](../06-reliability/28-verifier-agent-critic.md) activation conditions difficulty-dependent

## Tuning (Dials)

- **Effort range** (minimum effort vs. maximum effort) — Minimum too low degrades quality even for easy queries vs. maximum too high causes cost/latency explosion / Deciding factors `[F7]` `[F2]` / Guideline: Minimum = single-pass inference, Maximum = 3-pass inference with verification. → [Tuning Dials](../../decisions/tuning-dials.md)

## Related Patterns

- [#37 Semantic Gateway](37-semantic-gateway-cost-aware-router.md) — Model selection-level optimization (Adaptive Effort adjusts compute within the model)
- [#5 Time-Budgeted Agent Loop](../01-execution/05-time-budgeted-agent-loop.md) — Combine with time/iteration budget constraints
- [#28 Verifier Agent / Critic](../06-reliability/28-verifier-agent-critic.md) — Used to decide whether to add verification at high effort levels

## References

- Anthropic Extended Thinking Documentation
- OpenAI Reasoning Effort Parameter
