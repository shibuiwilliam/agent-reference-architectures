---
title: "Excessive Guardrails"
tags:
  - "Anti-Pattern"
  - "Degree Error"
---

# 2. Excessive Guardrails

!!! abstract "TL;DR"
    An anti-pattern where guardrails are set too strictly, blocking the majority of legitimate requests and destroying the user experience.

## Common Scenario

A team built a customer support agent. During the pre-release security review, a requirement was added: "harmful output must never be produced." The team set guardrail thresholds to maximum strictness. After deployment, normal inquiries like "I'd like to return this" were frequently flagged as "negative sentiment" and blocked. Medical-related questions were also filtered as "dangerous content."

Users became frustrated by repeated blocks and started experimenting with rephrased prompts to circumvent the guardrails. As a result, the guardrails became nothing more than an obstacle for legitimate users while giving malicious users clues on how to bypass them.

## Symptoms

- False positive rate (legitimate request block rate) exceeds 10%
- Users rephrase the same intent multiple times and resubmit
- "How to ask without triggering the guardrail" tips are shared among users
- Customer support receives increasing complaints that "the agent is unusable"
- The guardrail exception list grows bloated and becomes difficult to maintain

## Root Cause

Fear of security and safety issues leads to the judgment that "stricter is safer." However, guardrail strictness should be determined by balancing `[F5]` input trust level and `[F2]` failure cost. The appropriate level of strictness differs between systems for internal users and those for the general public.

Additionally, without a mechanism to measure and improve guardrail false positive rates, the tendency is to default to "as strict as possible." The cost of false positives (user churn, reduced operational efficiency) not being quantified is also a contributing factor.

## Detection Methods

- **False positive rate measurement**: Sample blocked requests and manually review them to calculate the proportion of legitimate requests
- **User behavior analysis**: Check whether the same user repeatedly submits similar requests in a short time
- **Guardrail trigger rate**: Check whether guardrail triggers exceed 5% of all requests
- **Metrics**: `guardrail_block_rate`, `false_positive_rate`, `user_retry_rate`

## Countermeasures

### Step 1: Design tiered guardrails

Establish three tiers — "immediate block," "pass with warning," and "log only" — and route based on risk level. Don't block everything from the start.

### Step 2: Run a cycle to measure and improve false positive rates

Periodically sample blocked requests and measure the false positive rate. Adjust thresholds and iterate until the false positive rate falls within the target (e.g., below 1%).

### Step 3: Codify guardrails and make them testable

Manage rules as code and run regression tests with test cases (sets of legitimate and harmful requests).

```yaml
# Guardrail configuration example
guardrails:
  - name: toxicity_filter
    threshold: 0.85        # High threshold = block only clearly harmful content
    action: block
  - name: sentiment_check
    threshold: 0.95        # Very high threshold = almost never blocks
    action: warn_and_log
  - name: pii_detector
    threshold: 0.70
    action: redact          # Mask instead of block
```

## Examples

### Before (problematic state)

```python
# All rules applied with uniformly strict thresholds
guardrail_result = check_all_guardrails(
    input=user_message,
    threshold=0.5,  # Low threshold = blocks broadly
    action="block",
)
if guardrail_result.blocked:
    return "Sorry, we cannot handle this request."
```

### After (improved)

```python
# Tiered guardrails based on risk level
guardrail_result = check_guardrails(
    input=user_message,
    rules=load_rules("guardrails.yaml"),
)

if guardrail_result.hard_block:
    return "We cannot respond for safety reasons."
elif guardrail_result.soft_block:
    log_for_review(user_message, guardrail_result)
    return agent.run(user_message, with_disclaimer=True)
else:
    return agent.run(user_message)
```

## Related Anti-Patterns

- [Context Stuffing](05-context-stuffing.md) — Excessive guardrails create pressure to trim input to bypass them
- [No Rationale for Dial Settings](06-no-rationale.md) — Without rationale for thresholds, the default is "as strict as possible"

## Related Patterns

- [#30 Policy-as-Code Guardrail](../glossary.md) — Codify guardrails and make them testable
- [#29 Guardrail Sidecar + Self-Correction](../glossary.md) — Respond with self-correction instead of blocking
- [#57 Autonomy Ladder](../glossary.md) — Control progressively based on risk level
