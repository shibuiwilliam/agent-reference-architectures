---
title: "[C9] Behavior Change = Model Update"
tags:
  - "Characteristics"
---

# [C9] Behavior Change = Model Update

!!! abstract "Summary"
    Behavior changes with model updates without any code changes -- regressions occur that conventional CI/CD change detection cannot catch.

## Overview

In traditional software, behavior changes were accompanied by code changes and could be detected through diffs and tests. With AI agents, the provider simply updates a model and output quality, format, and tendencies change. Your code, prompts, and configuration files all remain identical, yet the service behavior changes. Looking at the Git commit history reveals no cause.

## Why This Is a Problem

The provider updates a minor version of "gpt-4o" and the JSON output format subtly changes. Downstream parsers break and error rates spike, but since no deployment was made, root cause identification takes time. In another case, a model update changes the response tone, and customer satisfaction scores drop. Teams that do not run evaluation CI/CD cannot even determine "when quality started declining." Deprecation notices for old model versions are overlooked, and the sudden inability to use them causes an outage.

## Comparison with Traditional Software

| Aspect | Traditional Software | AI Agent |
|--------|---------------------|----------|
| Behavior change trigger | Your own code changes (diff-trackable) | Provider's model update (no diff on your side) |
| Change detection | CI/CD tests + code review | Requires statistical detection via evaluation pipelines |
| Rollback | Deploy the previous code version | Requires model version pinning + prompt adjustment |
| Change blast radius | Only the modified code path | Can affect all requests |

## Affected Forces

- `[F8]` Accountability & Regulation -- Inability to detect and record behavior changes means audit requirements cannot be met
- `[F9]` Provider Reliability -- The provider's update frequency and quality of advance notice influence the risk level
- `[F2]` Failure Cost -- When model-update-induced quality degradation directly impacts the business, version pinning is essential

## Safeguard Patterns

- [#33 Version Pinning](../../glossary.md) -- Pin prompt, model, and tool versions to prevent unintended changes
- [#35 Production Replay](../../glossary.md) -- Replay production logs with the new model and detect differences from the old model
- [#36 Shadow / Canary Deployment](../../glossary.md) -- Roll out model updates gradually and auto-rollback on issues

## Related Design Decisions

- [prompt-storage](../../decisions/dials/prompt-storage.md) -- How prompts are version-managed determines rollback capability
- [trace-sampling-rate](../../decisions/dials/trace-sampling-rate.md) -- Sampling rate affects the speed at which quality drift is detected
- [same vs. different model](../../decisions/tradeoffs-catalog/same-vs-different-model.md) -- Use the same model for verification, or verify with a different model for multiple perspectives
