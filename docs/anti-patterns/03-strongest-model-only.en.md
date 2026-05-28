---
title: "Strongest Model Only"
tags:
  - "Anti-Pattern"
  - "Degree Error"
---

# 3. Strongest Model Only

!!! abstract "TL;DR"
    An anti-pattern where the largest, highest-performance model is used for all requests, causing costs to scale linearly.

## Common Scenario

A startup built a Q&A agent for their internal knowledge base. During development, they validated with the latest large model, were satisfied with the high answer quality, and deployed it to production as-is. As the number of users grew, monthly LLM API costs surged. Analyzing the breakdown revealed that 70% of requests were routine questions like "What are the office hours?" or "How do I book a meeting room?" — questions that the smallest model could answer perfectly well.

The team avoided changing models because they "didn't want to compromise quality," but costs exceeded the budget and they were forced to impose usage limits. What was supposed to give everyone high-quality answers instead restricted everyone's usage — a counterproductive outcome.

## Symptoms

- LLM API costs scale linearly with request count, becoming a scaling bottleneck
- Even simple questions incur multi-second latency, making users wait
- Cost reduction forces the introduction of request or rate limits
- "Wouldn't a cheaper model suffice?" debates recur, but there are no switching criteria

## Root Cause

The oversimplification that "using the highest-quality model is always the right choice" is the cause. Task difficulty is not uniform — the majority of requests can achieve sufficient quality with small to medium models. However, building a mechanism for dynamic per-request model selection is costly, and using a single large model for everything is seen as "easier."

The balance between `[F7]` cost sensitivity and `[F3]` request value is off. All requests are treated as having equal value.

## Detection Methods

- **Task difficulty distribution**: Sample requests and evaluate quality when answered by a small model. Calculate the proportion of requests where quality is sufficient
- **Cost-quality analysis**: Plot quality scores and costs by model size and draw a cost-effectiveness curve
- **Metrics**: `cost_per_request` (by model), `quality_score` (by model), `task_complexity_distribution`

## Countermeasures

### Step 1: Introduce a task difficulty classifier

Assess request difficulty with a lightweight classifier (rule-based or small model) and route to the appropriate model.

### Step 2: Implement cascading model calls

First generate an answer with a small model, and escalate to a large model only if confidence is low.

### Step 3: Adjust thresholds with quality monitoring

Continuously measure answer quality per model and adjust routing thresholds.

```yaml
# Model routing configuration example
routing:
  - condition: "complexity <= simple"
    model: "small-model"
    max_cost: 0.001
  - condition: "complexity <= moderate"
    model: "medium-model"
    max_cost: 0.01
  - condition: "complexity > moderate"
    model: "large-model"
    max_cost: 0.10
```

## Examples

### Before (problematic state)

```python
# All requests processed with the largest model
response = llm_client.chat(
    model="gpt-4o",
    messages=[{"role": "user", "content": user_query}],
)
# Cost: uniform $0.01-0.05/request
```

### After (improved)

```python
# Model routing based on difficulty
complexity = classify_complexity(user_query)  # Lightweight classifier

model_map = {
    "simple": "gpt-4o-mini",    # $0.0001/request
    "moderate": "gpt-4o-mini",  # $0.001/request
    "complex": "gpt-4o",        # $0.01/request
}

response = llm_client.chat(
    model=model_map[complexity],
    messages=[{"role": "user", "content": user_query}],
)
# Average cost: $0.002/request (approx. 80% reduction)
```

## Related Anti-Patterns

- [Full Observability Deployment](04-full-observability.md) — Shares the "highest quality everywhere" mindset
- [No Rationale for Dial Settings](06-no-rationale.md) — Without documented model selection criteria, the default is the strongest model

## Related Patterns

- [#37 Semantic Gateway & Cost-Aware Router](../decisions/dials/model-tier-routing.md) — Route to different models based on difficulty
- [#56 Adaptive Effort](../foundations/forces/f7-cost-sensitivity.md) — Dynamically adjust computational effort
- [#40 Fallback & Graceful Degradation](../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) — Cascading model switching
