---
title: "[F2] Failure Cost"
tags:
  - "Driving Variables"
---

# [F2] Failure Cost

!!! abstract "Summary"
    A force that measures how much pain (financial, legal, safety, reputational) results when an agent produces incorrect output or operations.

## Overview

When an internal chatbot gives an off-target answer to an employee's question, it is laughable. But when a medical diagnosis support AI presents an incorrect dosage, patient lives are at stake. The same "mistake" demands vastly different defenses depending on the severity of its consequences.

Failure cost represents the severity of damage caused by agent errors. The higher this force, the thicker the verification, approval, and audit layers need to be.

## Why It Matters

Underestimating failure cost leads to complacency with a system that "happens to work" in production, where rare failures lead directly to lawsuits, regulatory violations, or human harm. Overestimating it means imposing heavy approval flows on every operation, collapsing throughput. Accurate estimation determines the appropriate thickness of defense layers.

## Interpreting the Value Range

### When Low

Situations where errors have minimal real-world impact. Typical examples include internal FAQ bots, draft document generation, and developer-facing code completion. Users visually review results before using them, and the feedback loop for errors is short. In this range, guardrails can be kept light, prioritizing speed and convenience.

### When High

Situations where errors directly result in financial loss, legal liability, or safety hazards. Examples include financial trade execution, medical report generation, legal document review, and automated infrastructure changes. A single error can lead to millions in damages or sanctions from regulators. Multi-stage verification, independent Verifier agents, and Policy-as-Code constraint codification become necessary.

## Evaluation Guidelines

- Does the agent's erroneous output reach users or external systems directly, or does it go through human review?
- What is the worst-case financial loss per incident?
- Could an error trigger legal liability or regulatory violations?
- Could an error affect human safety or health?
- What was the blast radius of past incidents in similar systems?

## Influenced Design Decisions

### Related Dials

- [Self-Correction Loop Count](../../decisions/dials/self-correction-loops.md) -- The higher the failure cost, the more self-verification and correction loops to add
- [Guardrail Strictness](../../decisions/dials/guardrail-strictness.md) -- Set strict guardrails in high-cost domains
- [HITL Frequency](../../decisions/dials/hitl-frequency.md) -- Increase human approval frequency in proportion to failure cost
- [Best-of-N](../../decisions/dials/best-of-n.md) -- Select the best from multiple candidates for high-cost decisions
- [Autonomy Level](../../decisions/dials/autonomy-level.md) -- Suppress autonomy level as failure cost increases

### Related Tradeoffs

- [Single vs. Multi-Agent](../../decisions/tradeoffs-catalog/single-vs-multi-agent.md) -- When failure cost is high, multi-agent composition with a separate verifier role is advantageous
- [Same vs. Different Model](../../decisions/tradeoffs-catalog/same-vs-different-model.md) -- For high-cost decisions, verify with a different model to avoid shared blind spots
- [Inline vs. Post Verification](../../decisions/tradeoffs-catalog/inline-vs-post-verification.md) -- When failure cost is high, prioritize inline verification
- [Workflow vs. Agent](../../decisions/tradeoffs-catalog/workflow-vs-agent.md) -- In high-cost domains, use workflows to ensure controllability

## Related Patterns

- [#28 Verifier Agent / Critic](../../patterns/06-reliability/28-verifier-agent-critic.md) -- Pre-shipment inspection with an independent verifier
- [#31 Human Approval Checkpoint](../../patterns/06-reliability/31-human-approval-checkpoint.md) -- Require human approval before high-risk operations
- [#30 Policy-as-Code Guardrail](../../patterns/06-reliability/30-policy-as-code-guardrail.md) -- Codify constraints for mechanical evaluation
- [#10 Agent Ensemble & Debate](../../patterns/02-composition/10-agent-ensemble-debate.md) -- Improve robustness through multi-agent deliberation
- [#8 Planner-Executor-Reviewer](../../patterns/02-composition/08-planner-executor-reviewer.md) -- Separate planning, execution, and review to ensure quality at each stage
