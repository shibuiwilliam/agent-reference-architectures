---
title: "Retry Storm"
tags:
  - "Anti-Pattern"
  - "Tradeoff Mis-selection"
---

# 9. Retry Storm

!!! abstract "TL;DR"
    An anti-pattern where retries flood the LLM provider during a transient failure, amplifying the outage further.

## Common Scenario

In a production system, an LLM provider began returning temporary rate limits (429 errors). Each system component had retry logic built in, but backoff settings were insufficient. The API gateway retried 3 times, the inner agent framework also retried 3 times, and the innermost LLM client also retried 3 times. As a result, a single request failure could generate up to 27 API calls.

With thousands of concurrent requests in this state, request volume to the LLM provider swelled to over 20x normal. The provider's outage worsened, and recovery time extended significantly. Even after recovery, retries from the accumulated backlog were sent all at once, hitting rate limits again — a vicious cycle.

## Symptoms

- Request volume spikes dramatically (10x or more) during LLM provider transient failures
- System recovery takes a long time even after the failure is resolved
- Multi-layer retry stacking causes exponential request amplification
- API costs spike (if 429 responses are also counted)
- Normal requests experience collateral delay

## Root Cause

Retry logic is implemented independently per layer without designing an overall retry strategy. Each layer retries "on its own responsibility," causing multiplicative retry amplification.

Additionally, the choice between fail-fast and graceful degradation is not designed based on `[F9]` provider reliability and `[F3]` request value — it's built on the assumption that "retrying will fix things." Circuit breakers are often missing.

## Detection Methods

- **Retry amplification factor**: Calculate the maximum number of API calls that can result from a single original request (product of retry counts across all layers)
- **Traffic multiplier during failures**: Compare LLM API call volume before and after failure onset
- **Retry layer inventory**: Identify all layers in the system that perform retries
- **Metrics**: `retry_count_per_original_request`, `api_call_amplification_ratio`, `circuit_breaker_open_count`

## Countermeasures

### Step 1: Consolidate retries to a single layer

Retry only at the outermost layer, and do not retry at inner layers (propagate errors upward).

### Step 2: Mandate exponential backoff with jitter

Set retry intervals as `base_delay * 2^attempt + random_jitter` to prevent many clients from retrying at the same time.

### Step 3: Introduce circuit breakers

After a certain number of consecutive errors, "Open" the circuit and stop retrying altogether. After a set time, try "Half-Open" to verify recovery before returning to "Closed."

```python
# Retry with circuit breaker example
from circuitbreaker import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=5,      # Open after 5 consecutive failures
    recovery_timeout=30,      # Half-Open after 30 seconds
    expected_exception=RateLimitError,
)

@breaker
async def call_llm_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await llm_client.chat(prompt)
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
```

## Examples

### Before (problematic state)

```python
# 3 layers each retrying -> max 3x3x3 = 27 calls
# Layer 1: API Gateway
response = retry(times=3)(api_gateway.forward)(request)

# Layer 2: Agent framework (internal)
result = retry(times=3)(agent.execute)(task)

# Layer 3: LLM client (internal)
completion = retry(times=3)(llm_client.chat)(prompt)
```

### After (improved)

```python
# Retry only at outermost layer, inner layers fail-fast
# Layer 1: API Gateway — circuit breaker + retry
@circuit_breaker(failure_threshold=5, recovery_timeout=30)
@retry(times=3, backoff=exponential_with_jitter)
async def handle_request(request):
    return await agent.execute(request)

# Layer 2: Agent framework — no retry
async def execute(self, task):
    return await self.llm_client.chat(task.prompt)  # Errors propagate upward

# Layer 3: LLM client — no retry
async def chat(self, prompt):
    response = await self.http.post(self.endpoint, json={"prompt": prompt})
    if response.status == 429:
        raise RateLimitError(response)  # Propagate upward
    return response.json()
```

## Related Anti-Patterns

- [Infinite / Excessive Timeout](01-infinite-timeout.md) — Long timeouts amplify retry impact
- [All Sync / All Async](07-all-sync-or-async.md) — Sync processing timeouts trigger retries

## Related Patterns

- [#40 Fallback & Graceful Degradation](../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) — Graceful degradation when retries fail
- [#5 Time-Budgeted Agent Loop](../decisions/dials/budget-cap.md) — Overall budget management including retries
- [#37 Semantic Gateway & Cost-Aware Router](../decisions/dials/model-tier-routing.md) — Dynamic routing to alternative providers
