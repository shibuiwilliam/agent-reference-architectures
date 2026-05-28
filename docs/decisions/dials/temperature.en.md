---
title: "Temperature"
tags:
  - "Tuning Dial"
  - "F6 Task Variability"
---

# Temperature

!!! abstract "TL;DR"
    Control how much to smooth the LLM's output probability distribution, balancing between reproducibility and creativity.

## Overview

A data extraction task returns slightly different formats each time. Or you ask for brainstorming but always get the same ideas -- both are often caused by incorrect Temperature settings.

Temperature is a parameter that adjusts the sharpness of the LLM's softmax output. Values closer to 0 make the highest-probability token more likely to be selected, making output deterministic; higher values make lower-probability tokens more likely, diversifying the output. In agent systems, temperature may be varied per step depending on the nature of the task.

## Why Adjustment Is Needed

Setting high temperature on routine extraction or classification tasks introduces unnecessary variation that reduces accuracy. Conversely, setting low temperature on creative or exploratory reasoning tasks leads to getting stuck in local optima. Since each agent step (planning, execution, verification) has a different optimal temperature, a uniform setting cannot extract full performance.

## Extremes of the Range

### Too Small

Output becomes overly deterministic, returning the same output for the same input every time. Exploratory tasks get locked into local solutions and cannot propose diverse approaches. Best-of-N strategies also fail as candidates become identical.

### Too Large

Output randomness increases, leading to more hallucinations and context-divergent responses. Format violations in structured output also increase. Reproducibility is lost, making debugging and evaluation difficult as results differ each time for the same request.

## Determining Forces

- `[F6]` Task Variability -- Low temperature for routine tasks, high temperature for exploratory tasks is the basic approach

## Guidelines (Starting Point)

- Classification, extraction, structured output: 0.0-0.3
- Summarization, translation: 0.3-0.5
- Creative writing, brainstorming: 0.5-0.8
- Code generation: 0.0-0.2 (accuracy-first)
- Agent planning steps: 0.3-0.5 (some exploration is beneficial)

## Practical Adjustment

- Implement routing that varies temperature by task type (avoid uniform settings)
- When changing temperature, quantitatively measure quality changes on an evaluation set
- When combining with Best-of-N, set temperature slightly higher to ensure candidate diversity
- Manage temperature as part of deployment configuration alongside version pinning

## Related Patterns

- [#33 Version Pinning](../../decisions/dials/prompt-storage.md) -- Pin prompts, models, and parameters to ensure reproducibility
