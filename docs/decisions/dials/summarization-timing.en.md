---
title: "Summarization Timing"
tags:
  - "Tuning Dial"
  - "F4 Latency Budget"
---

# Summarization Timing

!!! abstract "TL;DR"
    Control when to compress conversation history and context into summaries, balancing context overflow against information loss.

## Overview

Mid-conversation, the agent suddenly returns a "context length exceeded" error. Or, summarization was triggered too early and the agent can no longer answer "What was the amount I mentioned earlier?" -- compressing context too early or too late both cause problems.

This dial determines when to replace accumulated context with summaries during long conversations or multi-step processing. Earlier summarization frees up context window space but loses details. Delaying preserves the original text but risks window overflow, causing errors or performance degradation.

## Why Adjustment Is Needed

The LLM's context window is finite, and long agent sessions will inevitably hit the limit. When the window overflows, either an API error or forced truncation of old context occurs. However, premature summarization can lose specific numbers, proper nouns, and conditional branches needed in later steps.

## Extremes of the Range

### Too Small

Frequent summarization over-compresses context, losing important details (specific numbers, conditions, exceptions). The LLM call costs for summarization itself also accumulate. If summarization quality is low, there is also a risk of information distortion.

### Too Large

The context window limit is reached, causing API errors or forced truncation. When window utilization is high, the "lost in the middle" problem diffuses the LLM's attention, potentially overlooking the most recent instructions. Token costs also increase unnecessarily.

## Determining Forces

- `[F4]` Latency Budget -- Summarization processing itself adds latency, and window overflow causes errors

## Guidelines (Starting Point)

- Trigger summarization when token usage reaches 70% of the context window
- Exclude important information (user instructions, constraints) from summarization and retain as original text
- Progressive compression: Keep the most recent N entries as original, summarize older ones, and summarize the summaries for even older ones
- Perform summarization during gaps in user input (asynchronously) to minimize perceived latency

## Practical Adjustment

- Monitor context window utilization in real time and trigger auto-summarization at threshold
- Compare answer quality before and after summarization to detect quality degradation from information loss
- Define categories of information exempt from summarization (constraints, user attributes, etc.) as rules
- Periodically evaluate the quality of summarization prompts and improve information retention rates

## Related Patterns

- [#23 Layered Memory](../../patterns/05-memory-context/23-layered-memory.md) -- Hierarchization of short-term, long-term, and shared memory with compression strategies
