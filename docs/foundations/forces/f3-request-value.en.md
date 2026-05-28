---
title: "[F3] Request Value"
tags:
  - "Driving Variables"
---

# [F3] Request Value

!!! abstract "Summary"
    A force that measures how much a single request contributes to revenue or decision-making. The higher the value, the more compute resources and verification cost can be justified per request.

## Overview

Using an expensive large-scale model for a single search suggestion would quickly turn into a loss, but for due diligence on a deal worth hundreds of millions, calling the model multiple times more than pays for itself. How many resources to invest per request depends on the value that request generates.

Request value represents the magnitude of business impact of each individual request. Acceptable cost and quality requirements change in proportion to this value.

## Why It Matters

Ignoring this force leads to either using expensive models for low-value requests (causing losses) or assigning cheap models to high-value requests (leading to insufficient quality). Without resource allocation proportional to request value, the business cannot sustain itself.

## Interpreting the Value Range

### When Low

Situations where per-request value is small and requests are processed in high volume. Typical examples include routine customer support responses, product recommendations, and search query classification. Rather than maximizing quality per request, cost efficiency and latency for bulk processing take priority. Cache utilization and routing to lightweight models become effective.

### When High

Situations where a single request is tied to contracts or decisions worth millions to billions. Examples include investment decision support, legal contract review, medical diagnosis reports, and final-stage hiring evaluations. Investing in multiple calls to large models, ensembles, and human review per request more than pays for itself. Quality and accuracy take priority over throughput.

## Evaluation Guidelines

- What is the direct revenue or cost savings from a successful request?
- What is the maximum LLM API cost that can be spent per request?
- How much does processing quality improvement affect customer satisfaction or retention?
- What is the daily/monthly request volume (consider the total of unit price x volume)?
- What would it cost for a human to perform the same task?

## Influenced Design Decisions

### Related Dials

- [Model Tier Routing](../../decisions/dials/model-tier-routing.md) -- Assign higher-tier models to high-value requests
- [Best-of-N](../../decisions/dials/best-of-n.md) -- Higher value justifies the cost of generating multiple candidates
- [Budget Cap](../../decisions/dials/budget-cap.md) -- Scale per-request caps proportionally to request value
- [Self-Correction Loop Count](../../decisions/dials/self-correction-loops.md) -- Additional correction passes are acceptable for high value

### Related Tradeoffs

- [Single vs. Multi-Agent](../../decisions/tradeoffs-catalog/single-vs-multi-agent.md) -- For high value, deploying multiple agents is worthwhile
- [RAG vs. Fine-Tuning](../../decisions/tradeoffs-catalog/rag-vs-finetuning.md) -- For high-volume, low-unit-price scenarios, fine-tuning can reduce inference cost
- [LLM vs. Tool](../../decisions/tradeoffs-catalog/llm-vs-tool.md) -- Route low-value routine processing to traditional tools, reserving LLMs for high-value tasks

## Related Patterns

- [#10 Agent Ensemble & Debate](../../decisions/tradeoffs-catalog/same-vs-different-model.md) -- Strengthen high-value decisions through multi-agent deliberation
- [#37 Semantic Gateway & Cost-Aware Router](../../decisions/dials/model-tier-routing.md) -- Dynamically select models by difficulty and value
- [#56 Adaptive Effort](../../foundations/forces/f7-cost-sensitivity.md) -- Scale compute effort up or down by difficulty
- [#5 Time-Budgeted Agent Loop](../../decisions/dials/budget-cap.md) -- Control loop iterations with a budget proportional to request value
- [#55 Deadline & Budget Cascade](../../decisions/dials/budget-cap.md) -- Propagate budgets to subtasks
