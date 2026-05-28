---
title: "Checkpoint Frequency"
tags:
  - "Tuning Dial"
  - "F1 Reversibility"
---

# Checkpoint Frequency

!!! abstract "TL;DR"
    Determine how frequently to persist an agent's intermediate state, weighing redo costs against I/O overhead.

## Overview

A 10-minute research task fails at the last step, and everything must be redone -- with a single checkpoint, recovery that should have taken minutes costs the same time and expense all over again.

This dial controls the interval at which long-running agents write intermediate state to storage. Checkpoints allow resuming from that point on failure, but each write adds latency and I/O load. There are two axes: step-based (every N steps) and time-based (every N minutes).

## Why Adjustment Is Needed

Without checkpoints, when a 10-minute process fails at the last step, it must restart from the beginning. Both token costs and user wait time are wasted. On the other hand, persisting every step makes I/O dominant -- especially when using external storage, latency can inflate several times over.

## Extremes of the Range

### Too Small

On failure, a large number of steps must be redone, causing token costs and latency to spike. Re-executing steps with side effects also risks double-execution of non-idempotent operations. The longer the job, the greater the damage.

### Too Large

Checkpoint serialization and writing adds to each step's latency. For high-frequency requests, IOPS to storage becomes a bottleneck. If state objects are large, network bandwidth is also strained.

## Determining Forces

- `[F1]` Reversibility -- Whether failures can be redone directly determines the need for checkpoints. Always save before steps with irreversible side effects

## Guidelines (Starting Point)

- Before steps with side effects: Always checkpoint
- Steps without side effects: Every 3-5 steps, or every 5 minutes
- When state size is small (< 1MB): Checkpointing every step is practical
- When state size is large: Consider differential/incremental saves

## Practical Adjustment

- Quantitatively compare redo costs on failure (tokens + time) against checkpoint I/O costs
- Identify side-effect steps and mark checkpoints immediately before them as mandatory
- Include checkpoint write time in traces and monitor the proportion of overall latency
- Consider whether asynchronous writes or buffering can reduce overhead

## Related Patterns

- [#2 Durable Agent Session](../../decisions/tradeoffs-catalog/in-context-vs-external.md) -- Foundation pattern for checkpoint-based pause and resume
