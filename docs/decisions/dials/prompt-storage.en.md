---
title: "Prompt Storage Location / Granularity"
tags:
  - "Tuning Dial"
  - "F8 Accountability / Regulation"
---

# Prompt Storage Location / Granularity

!!! abstract "TL;DR"
    Control the granularity and storage method of prompt version management, weighing change tracking against repository management overhead.

## Overview

"It was working fine until last week, but answer quality suddenly dropped" -- investigation reveals someone had modified the prompt, but no change history was retained. Prompts are the most impactful configuration determining agent behavior, and how they are managed affects both team productivity and quality.

This dial determines where and at what granularity to store an agent's system prompts, templates, and few-shot examples. Options range from managing them alongside code in a Git repository to externalizing them to a dedicated prompt registry. Granularity concerns whether the entire prompt is a single file or split by section.

## Why Adjustment Is Needed

Prompts are the most impactful configuration determining agent behavior, but unlike code, diffs are hard to read and the impact of changes is difficult to predict in advance. Without version control, "who changed what and when" cannot be tracked, making quality regression investigation impossible. On the other hand, excessively fine-grained management leads to repository bloat and increased management costs.

## Extremes of the Range

### Too Small

No prompt change history is retained, making regression investigation difficult. "It was working until last week" problems cannot be addressed. Prompts fall out of sync across team members, leading to different prompts running in different environments.

### Too Large

Even minor prompt modifications trigger a large number of file changes, increasing review burden. Repository size grows, slowing CI/CD pipelines. Running a separate prompt registry adds infrastructure costs.

## Determining Forces

- `[F8]` Accountability / Regulation -- The degree to which audit requirements demand traceability of prompt changes

## Guidelines (Starting Point)

- Basic approach: Manage in a Git repository with version tags
- Granularity: 1 agent = 1 file (split sections only when shared components exist)
- Tag format: Semantic versioning (`prompt-v1.2.0`)
- Record the prompt version as metadata at deploy time and link it to traces
- Manage few-shot examples in separate files from prompts so they can be updated independently

## Practical Adjustment

- Automatically test the impact on quality via evaluation CI/CD when prompts change
- State the reason for changes in commit messages and establish a review process
- Make prompt deployment independently rollbackable from code deployment
- Periodically check prompt diffs across environments (development, staging, production)

## Related Patterns

- [#33 Version Pinning](../../decisions/dials/prompt-storage.md) -- Pin prompt, model, and tool versions to ensure reproducibility
