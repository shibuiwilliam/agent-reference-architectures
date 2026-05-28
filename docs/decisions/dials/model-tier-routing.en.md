---
title: "Model Tier (Routing Threshold)"
tags:
  - "Tuning Dial"
  - "F7 Cost Sensitivity / Scale"
  - "F3 Per-Request Value"
---

# Model Tier (Routing Threshold)

!!! abstract "TL;DR"
    Control the routing threshold for selecting LLM models based on request difficulty.

## Overview

Sending all requests to the highest-performance model made monthly costs 10x. But switching to a cheaper model noticeably degraded response quality on complex questions -- differentiating model usage is essential for balancing cost and quality.

This dial determines the classification threshold when a semantic gateway categorizes requests: routing simple ones to smaller, cheaper models and difficult ones to larger, high-performance models. Raising the threshold sends more requests to the smaller model, reducing costs, but increases the risk of sending difficult questions to the smaller model and degrading quality.

## Why Adjustment Is Needed

Sending all requests to the highest-performance model inflates monthly costs by several times to tens of times. However, misclassification causes users to perceive quality degradation. Since classifier accuracy and performance gaps between models vary significantly by task domain, no universal threshold exists.

## Extremes of the Range

### Too Small

The classifier flags a high proportion as "difficult," sending most requests to the high-cost model. Cost reduction benefits are negligible, leaving only the overhead of the routing layer.

### Too Large

Requests that truly need the high-performance model are sent to the smaller model, degrading response quality. Retries and human escalation for insufficient responses increase, ultimately raising both cost and time. User trust erodes.

## Determining Forces

- `[F7]` Cost Sensitivity / Scale -- The higher the QPS and cost pressure, the greater the value of routing
- `[F3]` Per-Request Value -- Err on the safe side (large model) for high-value requests

## Guidelines (Starting Point)

- Route to the smaller model when classifier confidence is 0.8 or higher for "easy"
- Unclassifiable or low-confidence requests default to the large model
- Tasks with small quality gaps between models (templated responses, extraction) are aggressively routed to the smaller model
- Tasks with large quality gaps (reasoning, creative writing) require higher thresholds

## Practical Adjustment

- Periodically evaluate quality scores by model and task type to verify routing appropriateness
- Detect quality degradation after small-model routing through user feedback or automated evaluation
- Recalibrate routing thresholds when new models are released
- Report cost savings and quality changes monthly and visualize the cost-effectiveness of thresholds

## Related Patterns

- [#37 Semantic Gateway / Cost-Aware Router](../../glossary.md) -- Implementation pattern for model tier routing
