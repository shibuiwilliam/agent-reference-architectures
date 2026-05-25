---
title: "Self-Correction Loop Count"
tags:
  - "Tuning Dial"
  - "F7 Cost Sensitivity / Scale"
  - "F3 Per-Request Value"
---

# Self-Correction Loop Count

!!! abstract "TL;DR"
    Control the number of times an agent attempts self-correction on guardrail violations, balancing between token waste and giving up too soon.

## Overview

An agent was supposed to return JSON but failed with a syntax error. It regenerated and this time it passed -- there are many situations where "just try again" works. But for fundamentally unsolvable problems, repeated regeneration only wastes tokens and time.

This dial sets the upper limit on the number of loops where the agent attempts regeneration with the error message attached when output fails validation or guardrail checks. Increasing the count improves autonomous recovery, but also risks falling into wasteful loops that repeat the same mistake.

## Why Adjustment Is Needed

LLMs sometimes repeat the same mistake with the same prompt. An unlimited self-correction loop consumes massive tokens and inflates latency by several times. On the other hand, zero loops (no correction) means the only options are returning the guardrail-detected problem as-is or returning an error, which degrades quality.

## Extremes of the Range

### Too Small

Even problems that would be fixed by retrying -- such as format errors or minor policy violations -- result in immediate failure. The frequency of errors returned to users increases, creating a perception that the system is "unusable." Human intervention costs also increase.

### Too Large

Tokens are wasted on structurally unsolvable problems (model capability limits or prompt design flaws). The success rate of corrections drops sharply after the 3rd attempt, so cost-effectiveness deteriorates. Latency also increases linearly, raising the probability of hitting timeouts.

## Determining Forces

- `[F7]` Cost Sensitivity / Scale -- Each loop iteration adds LLM call costs
- `[F3]` Per-Request Value -- High-value requests can justify more loop iterations

## Guidelines (Starting Point)

- General use: 1-3 iterations
- High-value, low-frequency tasks: Up to 5 iterations (but vary the prompt per loop)
- If the same error occurs twice consecutively, terminate early
- Determine loop count by calculating the break-even point from request value and token unit cost

## Practical Adjustment

- Measure correction success rate per loop iteration and set the upper limit at the iteration where the success rate drops significantly
- Add logic to terminate before the limit if the same error is detected repeatedly
- Record token consumption within loops in traces and incorporate into cost monitoring
- Route error types with low correction success rates to guardrail or prompt improvements

## Related Patterns

- [#29 Guardrail Sidecar + Self-Correction](../../patterns/06-reliability/29-guardrail-sidecar-self-correction.md) -- Implementation pattern for self-correction loops
