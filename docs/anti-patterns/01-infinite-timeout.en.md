---
title: "Infinite / Excessive Timeout"
tags:
  - "Anti-Pattern"
  - "Degree Error"
---

# 1. Infinite / Excessive Timeout

!!! abstract "TL;DR"
    An anti-pattern where timeouts or budget caps are not set, or are set excessively high, allowing runaway agents to consume resources and costs.

## Common Scenario

A team developed an internal document summarization agent. Since processing completed in tens of seconds in the development environment, they deployed to production with the default 30-minute timeout. One day, a user uploaded a several-hundred-page PDF, and the agent fell into a summarize-then-self-correct-then-re-summarize loop. Processing continued for 25 minutes, consuming tens of thousands of tokens. Multiple similar requests piled up and hit the API rate limit, causing other users' requests to fail as collateral damage.

In another case, a multi-agent configuration without cost caps had a parent agent recursively calling child agents. Bills of tens of thousands of yen per request accumulated, and the team only noticed when the monthly invoice arrived.

## Symptoms

- Processing time for a single request sometimes exceeds 10x the expected duration
- Monthly LLM API costs significantly exceed the budget
- A single request consumes thousands to tens of thousands of tokens, exhausting rate limits for other requests
- The agent's self-correction loop fails to converge, endlessly repeating the same processing
- Connection pools are exhausted, degrading overall system throughput

## Root Cause

In development environments, inputs are small and processing completes normally, so problems don't surface. Timeout design doesn't account for worst-case scenarios, and "just set it long to be safe" margins become the production settings. Additionally, even though LLM call costs are usage-based, teams apply the same mindset as traditional API calls — thinking "timeouts are enough" — and overlook token count and cost caps.

In multi-agent configurations, parent task budgets don't propagate to child tasks, so child tasks independently consume budgets and total costs become uncontrollable.

## Detection Methods

- **Latency distribution check**: Watch out if P99 latency is 10x or more than P50
- **Cost distribution check**: Review histograms of per-request token consumption for outliers
- **Timeout setting inventory**: List all service timeout values and verify whether the rationale for each can be explained
- **Metrics**: `request_duration_seconds` P99, `tokens_per_request` max, `cost_per_request` max

## Countermeasures

### Step 1: Set caps on 3 axes

Set caps on time, token count (or step count), and cost. Abort processing when any one cap is reached.

```yaml
# Configuration example
timeout:
  sync_request: 10s
  async_job: 300s
budget:
  max_tokens_per_request: 50000
  max_cost_per_request_usd: 0.50
  max_steps: 20
```

### Step 2: Propagate budgets to child tasks

In multi-agent configurations, pass the parent task's remaining budget to child tasks. Ensure the sum of child task budgets does not exceed the parent's budget.

### Step 3: Set up monitoring and alerts

Issue alerts when 80% of a cap is reached, and record and analyze cases where caps are actually hit. Periodically review whether cap values are appropriate.

## Examples

### Before (problematic state)

```python
# No timeout, no budget cap
response = agent.run(
    prompt=user_input,
    # timeout not set (default: unlimited)
    # max_tokens not set
)
```

### After (improved)

```python
from agent_framework import BudgetPolicy

budget = BudgetPolicy(
    timeout_seconds=30,
    max_llm_calls=10,
    max_tokens=30000,
    max_cost_usd=0.30,
)

response = agent.run(
    prompt=user_input,
    budget=budget,
    on_budget_exceeded="return_partial",  # Return partial results
)
```

## Related Anti-Patterns

- [Retry Storm](09-retry-storm.md) — Long timeouts compound the damage when combined with retries
- [No Rationale for Dial Settings](06-no-rationale.md) — Without rationale for timeout values, they can't be reviewed

## Related Patterns

- [#5 Time-Budgeted Agent Loop](../decisions/dials/budget-cap.md) — Set caps on 3 axes: time, steps, and cost
- [#55 Deadline & Budget Cascade](../decisions/dials/budget-cap.md) — Propagate budgets to child tasks
- [#1 Request-to-Job Gateway](../decisions/tradeoffs-catalog/sync-vs-async.md) — Allocate budgets at request intake
