---
title: Introduction
---

# AI Agent Production Architecture Patterns

!!! abstract "Core Principle"
    **Surround a probabilistic core with a deterministic shell -- contracts, verification, budgets, permissions, observability -- and adjust the shell's dials according to context (forces).**

## About This Site

AI agents work fine as prototypes, but the moment you put them into production, problems like timeouts, cost explosions, and hallucinations erupt -- sound familiar? This site is a collection of architecture patterns designed to prevent such "breaking in production" scenarios.

It covers 12 categories and 59 patterns, explaining design intent, when to use and when not to, element technologies, and tuning considerations. Rather than a mere catalog of patterns, the site is organized around **decision-making (forces, degrees, and tradeoffs)**. Patterns are vocabulary, degrees and tradeoffs are grammar, forces are meaning -- this site builds design decisions in that order.

## Target Audience

This site is intended for architects and engineers who operate AI agents in production environments. It addresses the "failure modes" encountered when transitioning from prototype to production -- "it worked in the demo but fails in production," "costs are unpredictable," "how do we prevent hallucinations" -- and the patterns that serve as safeguards against them.

## How to Read (Start from Decision-Making)

1. Follow **[Decision-Making Flow](decisions/decision-flow.md)** -- 6 steps: force evaluation --> tradeoffs --> dials --> composition --> recording
2. Look up the vocabulary (patterns) you need from the **[Pattern Quick Reference](pattern-index.md)**
3. See **[Worked Examples](decisions/worked-examples.md)** for concrete walkthroughs

