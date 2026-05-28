---
title: "[C1] Non-Deterministic Output"
tags:
  - "Characteristics"
---

# [C1] Non-Deterministic Output

!!! abstract "Summary"
    The same input yields different outputs each time -- the foundations of testing, reproduction, and comparison are fundamentally undermined.

## Overview

Traditional software returns the same output for the same input. AI agents do not. Due to the probabilistic sampling of LLMs, the tone, structure, and content of responses vary even for identical prompts. Even with temperature=0, complete reproducibility is not guaranteed due to non-determinism in floating-point arithmetic and batching differences.

## Why This Is a Problem

The most painful situation in production is "a test that passed yesterday fails today." Regression test reliability collapses, and release decisions become subjective. When a customer reports "I got a different answer than before," the cause is difficult to pinpoint because the output differs despite identical input in the logs. Furthermore, when evaluating A/B test differences, the noise is so large that enormous sample sizes are needed for statistical significance. The situation where "reproduction steps" fail to reproduce -- nearly unthinkable in traditional software engineering -- becomes routine.

## Comparison with Traditional Software

| Aspect | Traditional Software | AI Agent |
|--------|---------------------|----------|
| Output for same input | Deterministic (identical) | Probabilistic (may vary each time) |
| Regression testing | Strict comparison with assert | Evaluation via semantic similarity or scores |
| Bug reproduction | Same result if input is reproduced | Different results possible even with identical input |
| Release decision | All tests pass = Go | Judgment based on statistical thresholds of evaluation scores |

## Affected Forces

- `[F2]` Failure Cost -- When high, output variability becomes a direct financial/legal risk
- `[F8]` Accountability & Regulation -- Creates the problem of being unable to explain "why this output was produced" during audits
- `[F3]` Request Value -- The higher the request value, the greater the impact of output quality variability

## Safeguard Patterns

- [#14 Structured Output Contract](../../decisions/tradeoffs-catalog/structured-vs-freeform.md) -- Constrain output with a schema to reduce structural variability
- [#28 Verifier Agent / Critic](../../decisions/tradeoffs-catalog/inline-vs-post-verification.md) -- Inspect output quality with an independent verifier before shipment
- [#34 Evaluation CI/CD](../../foundations/forces/f8-accountability.md) -- Automatically run statistical quality evaluations per change to detect regressions

## Related Design Decisions

- [self-correction-loops](../../decisions/dials/self-correction-loops.md) -- Accept variability while ensuring quality through the number of correction loops
- [temperature](../../decisions/dials/temperature.md) -- Lower values reduce variability but also reduce creativity
- [structured vs. freeform](../../decisions/tradeoffs-catalog/structured-vs-freeform.md) -- Limit variability range with structured output, or preserve flexibility with freeform
