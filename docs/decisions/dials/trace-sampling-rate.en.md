---
title: "Trace Sampling Rate"
tags:
  - "Tuning Dial"
  - "F8 Accountability / Regulation"
  - "F7 Cost Sensitivity / Scale"
---

# Trace Sampling Rate

!!! abstract "TL;DR"
    Control the proportion of agent execution traces recorded, balancing observability against storage costs.

## Overview

An incident occurs in production, but the trace for the request in question was not retained -- the result of over-reducing the sampling rate. Meanwhile, recording everything made monthly storage costs rival the LLM usage fees -- that story is not uncommon either.

This dial determines the proportion of each agent step (LLM calls, tool execution, decision branches) recorded as traces. At 100%, traces for all requests are saved; at 1%, only 1 in 100 requests is recorded. High sampling rates are needed during development and debugging, but cost optimization is required in high-traffic production environments.

## Why Adjustment Is Needed

Agent traces include the full input/output text of LLMs, making data volumes tens of times larger than typical web applications. Recording everything can result in monthly storage costs rivaling LLM costs themselves. However, without traces, incident investigation is impossible and no data is available for quality improvement.

## Extremes of the Range

### Too Small

When incidents occur, traces for the relevant request do not exist, making root cause identification difficult. Insufficient data for quality evaluation prevents the improvement cycle from functioning. Reproducing rare edge cases becomes impossible.

### Too Large

Storage costs become enormous. Traces including full LLM input/output can be several KB to several MB per request, generating TB-scale data daily under high QPS. Write load on the logging infrastructure may also impact application performance.

## Determining Forces

- `[F8]` Accountability / Regulation -- When audit requirements exist, full recording of specific categories may be mandatory
- `[F7]` Cost Sensitivity / Scale -- The higher the QPS, the greater the cost impact of sampling rate

## Guidelines (Starting Point)

- Development / staging: 100%
- Production (low traffic): 10-50%
- Production (high traffic): 1-10%
- Error requests: Always 100% (full recording on errors)
- High-risk operations: Maintain 100% by category

## Practical Adjustment

- Set rules to record 100% for error and anomaly-detected requests first
- Review storage costs and required trace coverage monthly
- Filter out information that should be excluded from sampling (personal data, confidential information)
- Combine with Hot/Cold tiering: place recent traces on fast storage and older ones on cheaper storage

## Related Patterns

- [#32 Agent Trace](../../patterns/07-observability/32-agent-trace.md) -- Foundation for recording all agent steps as traces
- [#54 Tiered Observability](../../patterns/07-observability/54-tiered-observability.md) -- Pattern for tiering observability data into Hot/Cold
