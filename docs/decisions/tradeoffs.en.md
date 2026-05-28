---
title: Criteria for Selecting Between Opposing Mechanisms
---

# Criteria for Selecting Between Opposing Mechanisms

!!! abstract "TL;DR"
    When stuck choosing "A or B," use this either-or catalog where driving variables `[F#]` guide the decision.

## What Are Tradeoffs?

"Should this be processed synchronously or asynchronously?" "Single agent or multi-agent?" — In design practice, you repeatedly face these kinds of either-or decisions. Which is correct depends on the context — that is, the value ranges of the [Driving Variables](../foundations/forces.md).

## Approach

Either-or decisions are not questions where "one side is always correct." Use the following principles to decide:

1. **Start from the default** — Each either-or has a "when in doubt, choose this" default. Start there and only choose the opposite when forces clearly negate the default
2. **Consider hybrid approaches** — Many either-or decisions have practical middle-ground solutions combining A and B. Don't stop at a binary opposition; consider gradual application
3. **Record the rationale** — Document "why A was chosen" in design documents or an [ADR](adr-template.md). This becomes the starting point for re-evaluation when forces change

## Classification and Meaning of Either-Or Decisions

The 16 either-or decisions can be classified into 4 categories by design domain.

### Execution Model

Either-or decisions about the agent's execution mode and control flow.

| Option A | Option B | Decision Variable | Default | Details |
|----------|----------|---------|-----------|------|
| Synchronous | Asynchronous | `[F4]` `[F1]` | Sync if within a few seconds | [→](tradeoffs-catalog/sync-vs-async.md) |
| Single Agent | Multi-Agent | `[F6]` `[F7]` | Single if sufficient | [→](tradeoffs-catalog/single-vs-multi-agent.md) |
| Centralized Orchestration | Choreography | `[F8]` `[F6]` | Centralized | [→](tradeoffs-catalog/orchestration-vs-choreography.md) |
| Workflow | Agent | `[F6]` `[F2]` | Workflow for routine tasks | [→](tradeoffs-catalog/workflow-vs-agent.md) |
| Plan (plan-first) | ReAct (step-by-step) | `[F2]` `[F6]` | Plan when side effects are significant | [→](tradeoffs-catalog/plan-vs-react.md) |

### Control & Knowledge Source

Either-or decisions about where and how the agent's behavior is controlled.

| Option A | Option B | Decision Variable | Default | Details |
|----------|----------|---------|-----------|------|
| Prompt Control | Code Control | `[F8]` `[F6]` | Code Control | [→](tradeoffs-catalog/prompt-vs-code.md) |
| RAG | Fine-Tuning | `[F7]` `[F4]` | RAG | [→](tradeoffs-catalog/rag-vs-finetuning.md) |
| Single Provider | Multi-Provider | `[F9]` `[F7]` | Start with single | [→](tradeoffs-catalog/single-vs-multi-provider.md) |
| LLM Reasoning | Tool Delegation | `[F2]` | Tools for arithmetic/search | [→](tradeoffs-catalog/llm-vs-tool.md) |

### Verification & Reliability

Either-or decisions about output verification methods and error behavior.

| Option A | Option B | Decision Variable | Default | Details |
|----------|----------|---------|-----------|------|
| Inline Verification | Post-hoc Verification | `[F4]` `[F2]` | Inline for high risk | [→](tradeoffs-catalog/inline-vs-post-verification.md) |
| Same-Model Verification | Different-Model Verification | `[F2]` `[F7]` | Same model; different for high risk | [→](tradeoffs-catalog/same-vs-different-model.md) |
| Fail-fast | Graceful Degradation | `[F9]` `[F3]` | Fail-fast for low value | [→](tradeoffs-catalog/fail-fast-vs-degradation.md) |

### Infrastructure & Data

Either-or decisions about communication, state management, and build strategy.

| Option A | Option B | Decision Variable | Default | Details |
|----------|----------|---------|-----------|------|
| Push | Pull | `[F4]` `[F7]` | Push | [→](tradeoffs-catalog/push-vs-pull.md) |
| In-Context State | External State | `[F4]` `[F8]` | In-context for short-term, external for persistent | [→](tradeoffs-catalog/in-context-vs-external.md) |
| Build | Buy | `[F8]` `[F7]` | Build for differentiation | [→](tradeoffs-catalog/build-vs-buy.md) |
| Structured Output | Free-Form Output | `[F8]` `[F6]` | Structured for downstream integration | [→](tradeoffs-catalog/structured-vs-freeform.md) |

## How to Use

1. When facing a design either-or, find the matching row in the tables above
2. Evaluate the forces listed in the "Decision Variable" column for your system
3. Starting from the "Default," consider whether the "Hybrid Approach" on each detail page is applicable
4. Record the selection rationale in [#32 Agent Trace](../glossary.md) or design documents

Tradeoff selection is not a one-time decision. When force ranges change — for example, due to regulatory tightening or scale increases — re-evaluation is necessary. See [Pattern Parameterization](parameterization.md).
