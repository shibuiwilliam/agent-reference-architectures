---
title: AI Agent Characteristics
---

# AI Agent Characteristics

!!! abstract "Summary"
    Identify how AI agents differ from traditional software, clarifying what each pattern is a safeguard against.

## Why Catalog Characteristics

If you deploy AI agents to production with the same assumptions as traditional software, they will break in unexpected ways. Outputs change every time, processing duration is unpredictable, external APIs get called autonomously -- without understanding these characteristics beforehand, you cannot choose the right safeguards (patterns).

Patterns are "solutions to problems." Therefore, to understand AI agent architecture patterns, you first need to grasp what **new failure modes** AI agents introduce to production environments.

## Approach

Characteristics are **prerequisites** for pattern selection. They serve as the rationale for "why this pattern is needed." Applying patterns without understanding characteristics risks either erecting unnecessary safeguards that add only complexity, or overlooking essential safeguards and inviting production incidents.

The risk severity of each characteristic is determined by the system's context -- namely, the [Driving Variables (Forces)](forces.md). Even for the same characteristic, the priority of countermeasures differs as force values change.

## Classification of Characteristics

The 9 characteristics can be grouped into three categories.

### Output Uncertainty

Ways in which AI agent output fundamentally differs from traditional software. Affects testing, verification, and quality assurance.

| # | Characteristic | Failure Mode | Details |
|---|---------------|--------------|---------|
| C1 | **Non-Deterministic Output** | Testing, reproduction, and comparison are difficult with conventional methods | [-->](characteristics/c1-non-determinism.md) |
| C4 | **Hallucination** | Confidently generates information that contradicts facts | [-->](characteristics/c4-hallucination.md) |
| C9 | **Behavior Change = Model Update** | Behavior changes with model updates without any code changes | [-->](characteristics/c9-model-update-drift.md) |

### Execution Unpredictability

Processing time, side effects, and resource consumption are unpredictable. Affects operations, scaling, and safety.

| # | Characteristic | Failure Mode | Details |
|---|---------------|--------------|---------|
| C2 | **Long and Variable Duration Execution** | HTTP timeouts and resource hogging | [-->](characteristics/c2-variable-duration.md) |
| C3 | **Side Effects on the External World** | Unintended execution of irreversible operations | [-->](characteristics/c3-side-effects.md) |
| C5 | **Finite Context Window** | Cannot handle long conversations or large documents at once | [-->](characteristics/c5-context-window.md) |

### External Dependencies and Cost

Dependencies on external services and the associated cost, security, and availability challenges.

| # | Characteristic | Failure Mode | Details |
|---|---------------|--------------|---------|
| C6 | **Dependency on External LLMs** | Latency, availability, and pricing are outside your control | [-->](characteristics/c6-external-llm-dependency.md) |
| C7 | **Natural Language Interface = Attack Surface** | New attack vectors such as prompt injection | [-->](characteristics/c7-attack-surface.md) |
| C8 | **Cost Proportional to Input/Output Volume** | Costs can vary by orders of magnitude depending on usage | [-->](characteristics/c8-token-cost.md) |

## Relationship Between Characteristics and Driving Variables

How much risk each characteristic poses depends on the system's context -- namely, the [Driving Variables (Forces)](forces.md). For example, "Non-Deterministic Output" (C1) can be critical in healthcare or finance where failure cost `[F2]` is high, but is acceptable in recommendation scenarios where `[F2]` is low.

Patterns are generic safeguards against characteristics, but which patterns to apply and to what degree is determined by the driving variables. The [Decision Layer](../decisions/tuning-dials.md) helps make these judgments.
