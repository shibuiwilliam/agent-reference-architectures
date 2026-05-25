---
title: "No Rationale for Dial Settings"
tags:
  - "Anti-Pattern"
  - "Degree Error"
---

# 6. No Rationale for Dial Settings

!!! abstract "TL;DR"
    An anti-pattern where timeout values, retry counts, and guardrail thresholds are set "by feel" without recording the rationale, then deployed to production.

## Common Scenario

An incident occurred with an agent that a team had deployed six months ago. The timeout was set to 15 seconds, but nobody could explain why 15 seconds. The original developer had transferred to another team, and there was no mention in the design documentation. A debate started about whether it should be 10 seconds or 20 seconds, but no conclusion could be reached due to lack of evidence.

Eventually, they compromised with "let's set it to 30 seconds to be safe," which triggered a different problem (connection exhaustion). Retry counts and guardrail thresholds similarly remained as "values someone originally decided," and inconsistencies spread as the system grew.

## Symptoms

- Nobody can explain "why that value" for parameter settings
- During incidents, decision-making on "which parameter to change" is delayed
- Parameter changes are made as stopgap measures, producing side effects
- New team members can't understand the intent behind settings and are afraid to change them
- Similar systems use different parameter values with no explanation for the differences

## Root Cause

Teams focus on deciding the parameter value itself while neglecting to record "why that value." Code reviews verify implementation correctness but tend to overlook the validity and rationale of configuration values. Additionally, parameter values are often hardcoded, and the history of changes gets buried in commit logs.

Because the mapping between driving variables `[F#]` and parameters is not made explicit, when circumstances change (user growth, model changes, etc.), it's unclear which parameters need review.

## Detection Methods

- **Parameter inventory**: List all configuration parameters and check whether "why this value" can be documented for each
- **ADR existence**: Check whether Architecture Decision Records (ADRs) contain parameter rationale
- **Change history tracking**: Check whether commit messages for parameter changes include reasons
- **Check**: Show a configuration file to a new team member and ask "what is this value based on"

## Countermeasures

### Step 1: Create a parameter-to-driving-variable mapping

Explicitly document which `[F#]` each parameter depends on, enabling reverse lookup of affected parameters when a driving variable changes.

### Step 2: Record parameter rationale in ADRs

Record the initial parameter value, the rationale for choosing it (driving variable values, load test results, benchmarks, etc.), and conditions for changing it.

### Step 3: Leave rationale as comments in configuration

```yaml
# Document rationale inline in configuration files
timeout:
  sync_request: 10s
  # Rationale: 3x P99 latency of 3s (measured 2024-01) + margin
  # Driving variable: [F4] Latency budget = user-facing UI, dropout rate spikes above 10s
  # Review conditions: On model change, on 2x traffic increase
  # ADR: docs/adr/003-timeout-policy.md

retry:
  max_attempts: 3
  # Rationale: LLM provider transient failure rate 0.1% (2024-01 actual)
  # Driving variable: [F9] Provider reliability = high (SLA 99.9%)
  # 3 attempts provides sufficient coverage (1-(0.001^3) ≈ 99.9999%)
```

## Examples

### Before (problematic state)

```python
# Magic numbers scattered throughout
TIMEOUT = 15          # Why 15?
MAX_RETRIES = 5       # Why 5?
GUARDRAIL_THRESHOLD = 0.6  # Why 0.6?
TOP_K = 10            # Why 10?
```

### After (improved)

```python
# Structured parameters linked to rationale
AGENT_CONFIG = {
    "timeout_seconds": 10,        # ADR-003: [F4] P99=3s x 3 + margin
    "max_retries": 3,             # ADR-004: [F9] SLA 99.9% -> 3 attempts sufficient
    "guardrail_threshold": 0.85,  # ADR-005: [F5][F2] false positive rate below 1%
    "retrieval_top_k": 5,         # ADR-006: [F7] quality peak at k=5 (evaluation results)
}
```

## Related Anti-Patterns

- [Infinite / Excessive Timeout](01-infinite-timeout.md) — Result of setting values "long to be safe" without rationale
- [Excessive Guardrails](02-excessive-guardrails.md) — Result of setting values "strict to be safe" without rationale
- [Strongest Model Only](03-strongest-model-only.md) — Model selection criteria not documented

## Related Patterns

- [Pattern Parameterization](../decisions/parameterization.md) — Best practices for parameter management
- [Architecture Decision Record (ADR)](../decisions/adr-template.md) — Template for recording decision rationale
- [#32 Agent Trace](../patterns/07-observability/32-agent-trace.md) — Include configuration values in traces
