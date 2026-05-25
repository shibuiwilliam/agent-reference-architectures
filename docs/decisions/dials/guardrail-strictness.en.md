---
title: "Guardrail Strictness"
tags:
  - "Tuning Dial"
  - "F5 Input Trustworthiness"
  - "F2 Failure Cost"
---

# Guardrail Strictness

!!! abstract "TL;DR"
    Control input/output inspection thresholds to balance between missed harmful outputs (false negatives) and over-detection (false positives).

## Overview

"We tightened the guardrails and legitimate requests started getting blocked, triggering a flood of user complaints" -- the tension between security and usability is one of the most commonly faced dilemmas in agent operations.

This dial determines the judgment thresholds and scope of guardrails (input filters, output validation, policy checks). Stricter thresholds more reliably block harmful outputs, but also increase the rate of incorrectly blocking normal outputs. Adjustment based on the risk profile of the use case is essential.

## Why Adjustment Is Needed

Default guardrail settings are generic and may be too strict or too lenient for specific domains. In high-risk areas like healthcare and finance, missed detections can be fatal, while in creative use cases, over-detection severely damages user experience. If thresholds are set once and left alone, they cannot keep up with evolving attack techniques or changing input patterns.

## Extremes of the Range

### Too Small

Policy violations, harmful content, and prompt injection outputs slip through inspection. The risk of regulatory violations and brand damage increases. After an incident, you face the question "why wasn't this detected?"

### Too Large

Normal outputs are frequently blocked, leading users to judge the system as "unusable." Processing over-detections (retries, human escalation) increases system load. Users rewrite prompts unnaturally to circumvent guardrails, which actually degrades quality.

## Determining Forces

- `[F5]` Input Trustworthiness -- In environments with high attack or contamination probability, set thresholds stricter
- `[F2]` Failure Cost -- The greater the damage from harmful output, the more thresholds should favor reducing false negatives

## Guidelines (Starting Point)

- Classifier-based guardrails: Threshold 0.7-0.9 (tune per domain)
- High-risk domains (healthcare, finance): Prioritize minimizing false negatives; set thresholds higher
- Creative use cases: Prioritize minimizing false positives; set thresholds lower
- Rule-based policies (regex, block lists): Measure false positive rate before enabling

## Practical Adjustment

- Measure false positive and false negative rates weekly and track the optimal point on the ROC curve
- Review over-detected cases and feed back into guardrail rule improvements
- Use A/B testing to quantitatively evaluate the impact of threshold changes (task completion rate, user satisfaction)
- Periodically update rules and thresholds in response to new attack techniques or policy changes

## Related Patterns

- [#29 Guardrail Sidecar + Self-Correction](../../patterns/06-reliability/29-guardrail-sidecar-self-correction.md) -- Implementation of guardrail inspection and self-correction loops
- [#30 Policy-as-Code Guardrail](../../patterns/06-reliability/30-policy-as-code-guardrail.md) -- Managing and applying policies as code
