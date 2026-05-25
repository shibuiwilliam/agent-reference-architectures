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

## Start with the "5 Selection Questions"

If you are not sure where to begin, start by answering these five questions.

1. **What breaks when it fails?** --> If `[F2]` is high, consider [Side-Effect-First Architecture](reference-architectures/02-side-effect-first.md)
2. **Can you trust the input?** --> If `[F5]` is low, consider [Untrusted Input Architecture](reference-architectures/03-untrusted-input.md)
3. **What is the monthly cost cap?** --> If `[F7]` is high, consider [Cost-First Architecture](reference-architectures/05-cost-first.md)
4. **Are there audit/regulatory requirements?** --> If `[F8]` is high, consider [Continuous Improvement Operations Architecture](reference-architectures/06-continuous-improvement.md)
5. **Is it still a prototype?** --> If yes, start with the [MVP Architecture](reference-architectures/01-mvp.md)

--> See [Reference Architectures](reference-architectures/index.md) for details on the 5 questions

## How to Read (Start from Decision-Making)

1. Follow **[Decision-Making Flow](decisions/decision-flow.md)** -- 6 steps: force evaluation --> tradeoffs --> dials --> composition --> recording
2. Look up the vocabulary (patterns) you need from the **[Pattern Quick Reference](pattern-index.md)**
3. See **[Worked Examples](decisions/worked-examples.md)** for concrete walkthroughs

### Role of Each Page

| Section | Page | Role |
|---------|------|------|
| **Decision-Making** | [Decision-Making Flow](decisions/decision-flow.md) | The backbone of the site: a 6-step end-to-end workflow |
| | [Driving Variables (Forces)](foundations/forces.md) | Definitions of F1--F9 that serve as inputs to decision-making |
| | [Degrees (Dials)](decisions/tuning-dials.md) | 20 dials that determine "to what degree" a pattern is applied |
| | [Tradeoffs (Binary Choices)](decisions/tradeoffs.md) | 16 binary choices for "A or B" decisions |
| | [Reverse Lookup by Force](decisions/by-force.md) | Look up related decisions and patterns from a force |
| | [Worked Examples](decisions/worked-examples.md) | End-to-end demonstrations with 3 systems |
| **Patterns** | [Pattern Quick Reference](pattern-index.md) | List of all 59 patterns (vocabulary) |
| **Composite Architectures** | [Reference Architectures](reference-architectures/index.md) | Examples of layered pattern compositions |
| | [Anti-Patterns](anti-patterns/index.md) | Design decisions to avoid |
| **Agent Integration** | [Coding Agent Guide](agent-guide.md) | Procedures and conventions for coding agents to read this catalog and make evidence-based design proposals |
| | [Architecture Proposal Template](agent-proposal-template.md) | Standard format for agent-generated proposals |
