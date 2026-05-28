---
title: "Full Observability Deployment"
tags:
  - "Anti-Pattern"
  - "Degree Error"
---

# 4. Full Observability Deployment

!!! abstract "TL;DR"
    An anti-pattern where all requests and all tokens are fed through an expensive analysis pipeline, causing observability costs to exceed the LLM usage costs themselves.

## Common Scenario

A team set up a configuration to send all request prompts and responses to a real-time analysis pipeline for production agent quality monitoring. For each request, they ran toxicity scoring, hallucination detection, topic classification, and sentiment analysis using LLM-based evaluators. Initially, with only a few hundred requests per day, there were no issues. But when usage grew to tens of thousands of requests per day, the observability pipeline's LLM costs reached 3x the agent's own LLM costs.

Storage also ballooned. Retaining all traces indefinitely, they reached several TB within months, and queries to search logs during incident investigation took minutes. "Observability for observability's sake" was undermining its original purpose.

## Symptoms

- Observability and monitoring costs exceed 50% of LLM usage costs
- Log storage grows rapidly and search performance degrades
- The observability pipeline itself becomes a SPOF (single point of failure)
- Massive alert volumes bury important alerts (alert fatigue)
- The majority of observability data is retained without ever being referenced

## Root Cause

Anxiety-driven design — "we don't know what will happen, so record everything" — is the cause. In traditional web systems, log costs were relatively low, but quality analysis using LLM-based evaluators has a high per-item cost. Additionally, know-how for designing log retention periods and sampling rates in tiers is not yet established.

The balance between `[F8]` accountability and `[F7]` cost sensitivity is off.

## Detection Methods

- **Cost ratio check**: Compare observability-related costs (LLM evaluators, storage, analysis infrastructure) against the agent's LLM costs
- **Data utilization check**: Determine what proportion of stored logs/traces have actually been referenced (queried, displayed on dashboards)
- **Retention period check**: Verify whether logs older than 90 days have ever been referenced
- **Metrics**: `observability_cost / agent_cost`, `log_storage_gb`, `log_query_latency_p99`

## Countermeasures

### Step 1: Separate into Hot/Cold/Archive tiers

Keep recent data (Hot) in fast storage with full detail, move older data (Cold) to cheap storage with compression. Beyond a certain period, retain only aggregated values and delete raw data.

### Step 2: Set tiered sampling rates

Record normal requests via sampling (e.g., 10%), and only record full details for errors and anomaly-detected requests.

### Step 3: Limit LLM-based evaluation to samples

Instead of running LLM evaluators on all requests, only evaluate sampled requests. For items requiring real-time checks, substitute lightweight rule-based checks.

```yaml
# Observability configuration example
observability:
  tracing:
    normal_sampling_rate: 0.10   # Normal: 10% sampling
    error_sampling_rate: 1.0     # Errors: record all
    slow_request_threshold: 10s  # Slow: record all
  storage:
    hot_retention: 7d
    cold_retention: 90d
    archive: aggregates_only
  llm_evaluation:
    sampling_rate: 0.05          # Only 5% get LLM evaluation
    rule_based_check: all        # All get rule-based check
```

## Examples

### Before (problematic state)

```python
# All requests analyzed through the full pipeline
for request in all_requests:
    trace = record_full_trace(request)
    toxicity = llm_evaluate_toxicity(trace)
    hallucination = llm_detect_hallucination(trace)
    topic = llm_classify_topic(trace)
    store_forever(trace, toxicity, hallucination, topic)
# Observability cost: 3x agent cost
```

### After (improved)

```python
for request in all_requests:
    trace = record_lightweight_trace(request)  # Lightweight metadata
    rule_check = rule_based_check(trace)       # Rule-based (low cost)

    if rule_check.anomaly or is_sampled(rate=0.05):
        # Detailed analysis only for anomalies or sampled items
        llm_evaluate(trace)
        store_hot(trace, retention="7d")
    else:
        store_cold(trace.summary(), retention="90d")
# Observability cost: 15% of agent cost
```

## Related Anti-Patterns

- [Strongest Model Only](03-strongest-model-only.md) — Same "highest quality everywhere" mindset
- [No Rationale for Dial Settings](06-no-rationale.md) — No rationale for sampling rates or retention periods

## Related Patterns

- [#54 Tiered (Hot/Cold) Observability](../glossary.md) — Hot/Cold separation architecture
- [#32 Agent Trace](../glossary.md) — Trace design
- [#34 Evaluation CI/CD](../glossary.md) — Integrate evaluation into CI/CD
