---
title: "HITL Frequency"
tags:
  - "Tuning Dial"
  - "F2 Failure Cost"
---

# HITL Frequency (Human-in-the-Loop)

!!! abstract "TL;DR"
    Control the frequency of human review and approval within an agent's processing flow, balancing safety and throughput.

## Overview

The approval queue has 100 items piled up, and the person in charge clicks "approve" on all of them without reading the contents -- inserting too many human checkpoints can actually undermine safety through formalization. Conversely, too few interventions let erroneous external notifications or data deletions slip through.

This dial determines when and how often to insert Human-in-the-Loop (HITL) checks. It ranges from full supervision at every step to selective supervision only at specific high-risk operations. It is closely related to autonomy level, but this dial focuses on trigger design -- "when and where to call in a human."

## Why Adjustment Is Needed

Human intervention is the most reliable guardrail in an agent system, but it does not scale. Intervening on everything makes humans the bottleneck; too few interventions lead to missed risks. Poorly designed intervention points cause time to be spent on unimportant decisions while truly dangerous ones are overlooked -- a phenomenon known as "attention dilution."

## Extremes of the Range

### Too Small

High-frequency approval requests exceed human processing capacity, leading to approval fatigue and perfunctory "approve all." Agent processing becomes bottlenecked by human response speed, and batch processing parallelism is lost. As a result, personnel costs may actually increase compared to pre-agent adoption.

### Too Large

Irreversible operations and high-stakes decisions are executed without any checks. Incorrect external notifications based on hallucinations, accidental data deletion, and inappropriate user responses are reflected in production without being caught. Post-incident investigation is also hampered by the lack of approval records.

## Determining Forces

- `[F2]` Failure Cost -- The higher the cost of failure for an operation, the denser the HITL should be. Low-cost, reversible operations can skip HITL

## Guidelines (Starting Point)

- Irreversible and high-cost operations: Always HITL
- Irreversible but low-cost operations: Sampling-based HITL (10-20%)
- Reversible operations: No HITL needed; address through post-hoc auditing
- When agent confidence falls below a threshold: Dynamically insert HITL

## Practical Adjustment

- Classify operations by risk and set HITL policies per classification
- Monitor approval wait time and queue length to detect human capacity overload
- Track the number of incidents prevented by HITL intervention and evaluate the effectiveness of intervention points
- Periodically sample-audit operations processed without HITL to detect misses

## Related Patterns

- [#31 Human Approval Checkpoint](../../glossary.md) -- Implementation of checkpoints that insert human approval before high-risk operations
