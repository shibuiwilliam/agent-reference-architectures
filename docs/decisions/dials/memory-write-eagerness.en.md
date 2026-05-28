---
title: "Memory Write Eagerness"
tags:
  - "Tuning Dial"
  - "F8 Accountability / Regulation"
---

# Memory Write Eagerness

!!! abstract "TL;DR"
    Control how aggressively an agent writes information to long-term memory, balancing learning efficiency against noise accumulation.

## Overview

A user's previously communicated preferences are not remembered by the agent. Yet for another user, even one-off casual remarks are memorized, making it feel creepy -- what to remember and what to forget directly affects trust in an agent.

This dial controls the threshold for whether an agent writes information gained during conversations and processing to long-term memory. High eagerness memorizes everything; low eagerness saves only information clearly judged as important. Write decisions can be made through model autonomous judgment, rule-based logic, or human approval.

## Why Adjustment Is Needed

An agent's long-term memory is utilized through search, so increased noise degrades search accuracy. On the other hand, failing to write important information prevents leveraging past learnings and repeats the same failures. Without write criteria, the memory store either bloats with degraded performance or remains empty and unused.

## Extremes of the Range

### Too Small

User preferences, past decision rationale, and task-specific learnings are not saved. The agent judges from scratch every time, and conversational repetition increases. The feedback loop for long-term quality improvement is severed.

### Too Large

Temporary information, noise, and contradictory information accumulate in memory. Irrelevant information contaminates search results and becomes a source of hallucinations. Storage costs increase and the burden of memory management and cleaning grows.

## Determining Forces

- `[F8]` Accountability / Regulation -- There is accountability for what is memorized, and indiscriminate writing becomes an audit risk

## Guidelines (Starting Point)

- High-confidence information (user's explicit instructions, verified facts): Auto-write
- Medium-confidence information (inference results, implicit preferences): Judge by confidence threshold
- Low-confidence information (one-off context, unverified speculation): Do not write
- In environments where human approval is possible: Make medium-confidence writes subject to approval

## Practical Adjustment

- Measure the utilization rate of written memories (proportion referenced in subsequent queries)
- Raise the write threshold for memory categories with low utilization rates
- Periodically sample-review memory quality to understand noise ratio
- Retain write decision logs to enable auditing of decision criteria

## Related Patterns

- [#25 Memory Write Gate](../../glossary.md) -- Gate pattern that makes long-term memory writes subject to approval
