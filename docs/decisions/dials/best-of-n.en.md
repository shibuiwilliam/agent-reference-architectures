---
title: "Best-of-N (Generation Count)"
tags:
  - "Tuning Dial"
  - "F2 Failure Cost"
  - "F3 Per-Request Value"
---

# Best-of-N (Generation Count)

!!! abstract "TL;DR"
    Control the generation count N when generating multiple candidates and selecting the best one, balancing quality improvement against cost multiplication.

## Overview

Relying on a single generation for contract review results feels risky. Generating three variations and comparing them reduces oversights, but costs triple -- "how many times to generate" is a direct tradeoff between risk and cost.

This dial determines the generation count N in strategies that generate N outputs for the same input and select the best one via a scoring function or consensus. N=1 is standard single generation; N>1 is an ensemble-like approach. Since LLM call costs increase proportionally to N, differentiated usage based on request risk and value is necessary.

## Why Adjustment Is Needed

LLM output is probabilistic, and there is no guarantee that a single generation is optimal. Particularly in code generation and reasoning tasks, selecting from multiple candidates can significantly improve accuracy. However, since costs multiply by N, applying it to all requests strains the budget.

## Extremes of the Range

### Too Small

You are fully dependent on the first generation and cannot benefit from LLM output variance. When a low-quality generation happens to occur, it becomes the final output as-is. Unacceptable quality variance remains for high-risk tasks.

### Too Large

Costs inflate by N times, and latency also multiplies by N if not parallelized. Quality improvement diminishes as N increases, with improvement typically becoming marginal beyond N=5. If the scoring function quality is low, increasing candidates does not help with best selection.

## Determining Forces

- `[F2]` Failure Cost -- The greater the damage from failure, the stronger the justification for N>1
- `[F3]` Per-Request Value -- High-value requests can justify the cost increase

## Guidelines (Starting Point)

- Low-risk, routine tasks: N=1
- Medium-risk (code generation, summarization): N=3
- High-risk (legal, medical decision support): N=3-5
- N>5 is not recommended due to rapidly diminishing cost-effectiveness
- Use parallel generation + streaming to minimize perceived latency

## Practical Adjustment

- Measure the quality difference between N=1 and N=3 per task type and apply only to tasks where the improvement is significant
- Since the accuracy of the evaluation function (scoring, validation) determines Best-of-N effectiveness, establish the evaluation function first
- Compare the cost increment against request value and choose N where ROI is positive
- If diversity between generated candidates is low, also adjust temperature

## Related Patterns

- [#10 Agent Ensemble & Debate](../../glossary.md) -- Composition pattern for generating, debating, and selecting the best across multiple agents
