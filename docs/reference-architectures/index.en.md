---
title: Reference Architectures
---

# Reference Architectures

!!! abstract "TL;DR"
    Examples of **composite configurations that layer individual patterns**. Use them as starting points for "where to begin."

## How to Layer Patterns

Even if you understand patterns individually, it's hard to translate them into a design without seeing "how they combine in a real system." Here we present composite configurations that layer multiple patterns for typical use cases.

Each configuration includes "why this pattern is adopted" and "conditions under which it can be omitted." There is no need to adopt everything at once — start with a minimal configuration and add layers as [driving variables](../foundations/forces.md) change.

## 6 Configurations

| Configuration | Scenario | Key Forces |
|------|------|-------------|
| [1. Minimal Configuration (MVP)](01-mvp.md) | Internal tools / prototypes | `[F2]` low, `[F8]` low |
| [2. Side-Effect-First Configuration](02-side-effect-first.md) | Includes irreversible operations | `[F1]` low, `[F2]` high |
| [3. Untrusted Input Configuration](03-untrusted-input.md) | Untrusted user input | `[F5]` low |
| [4. Factuality-First Configuration](04-factuality-first.md) | Hallucination intolerable | `[F2]` high, `[F8]` high |
| [5. Cost-First Configuration](05-cost-first.md) | High volume / low cost | `[F7]` high |
| [6. Continuous Improvement Configuration](06-continuous-improvement.md) | Quality maintenance / improvement | `[F8]` high |

## 5 Selection Questions

If you're unsure which configuration to start with, answer these 5 questions:

1. **What breaks when it fails?** -> If `[F2]` is high, [Side-Effect-First](02-side-effect-first.md) or [Factuality-First](04-factuality-first.md)
2. **Can the input be trusted?** -> If `[F5]` is low, layer [Untrusted Input Configuration](03-untrusted-input.md)
3. **What's the monthly cost cap?** -> If `[F7]` is high, prioritize [Cost-First Configuration](05-cost-first.md)
4. **Are there audit/regulatory requirements?** -> If `[F8]` is high, adopt [Continuous Improvement Configuration](06-continuous-improvement.md) early
5. **Is this still a prototype?** -> If yes, start with [Minimal Configuration](01-mvp.md) and add layers as it moves to production

Configurations are not mutually exclusive. For example, it's common to layer multiple configurations like side-effect-first and cost-first together. What matters is being able to explain "why this layer is needed" based on [driving variables](../foundations/forces.md).
