---
title: "Agent Constitution"
tags:
  - "Organization, Governance & Lifecycle"
  - "F8 Accountability & Regulation"
  - "F2 Failure Cost"
---

# #52 Agent Constitution

!!! abstract "TL;DR"
    Systematically define agent behavioral principles, prohibitions, and priorities, and deploy them consistently across all agents.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #52 Agent Constitution</summary>

| Field | Value |
|------|-----|
| **ID** | 52 |
| **Category** | 12-governance — Organization, Governance & Lifecycle |
| **Forces** | `[F8]`, `[F2]` |
| **Dials** | — |
| **Tradeoffs** | — |
| **Related Patterns** | #30, #53, #33 |
| **When to Use** | Multi-agent organizations, regulated industries, audit trails required, behavioral consistency critical |
| **When Not to Use** | Single-agent experiments; principles not yet formed (still in learning phase) |
| **Element Technologies** | YAML/JSON principle hierarchy, Git management, Jinja2 template engine, policy engine |

</details>
<!-- END:GEN:meta -->

## Overview

One agent returns responses containing personal information while another blocks the same question -- when system prompts contain ad-hoc "don't do this" and "be careful" instructions, behavioral standards vary across agents and such inconsistencies easily emerge.

Agent Constitution defines organization-level behavioral principles -- ethical guidelines, data handling policies, escalation conditions, prohibited operations -- as a structured document and automatically injects them into all agents' system prompts and guardrails.

!!! info "Position in decision-making"
    - **Driving force**: `[F8]` Accountability & Regulation, `[F2]` Failure Cost
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

The Constitution has a hierarchical structure:

1. **Organization level**: Principles common to all agents (data protection policies, ethical guidelines, legal compliance)
2. **Domain level**: Domain-specific rules (suitability principles for finance, diagnosis prohibition for healthcare, etc.)
3. **Agent level**: Individual agent behavioral constraints (operation scope, permission caps)

Principles at each level are managed in machine-readable formats such as YAML / JSON with version control. At deploy time, a template engine injects them into system prompts, and they are also deployed as rules for [#30 Policy-as-Code Guardrail](../06-reliability/30-policy-as-code-guardrail.md).

## Problems Solved

When an agent takes actions contrary to organizational policies, ambiguous accountability results if "who set which rules" is unclear `[F8]`. Accumulating ad-hoc prompt modifications tends to create contradictions and gaps. Systematically defining principles ensures consistency of behavioral standards and traceability of changes. The higher the failure cost of a domain, the greater the value of documented principles `[F2]`.

## When to Use / When Not to Use

- **When to Use**: Organizations operating multiple agents. Regulated industries (finance, healthcare, legal). Cases requiring audit trails for behavioral principles.
- **When Not to Use**: Too early in the single-agent experimental phase when principles are not yet solidified. It is better to go through a phase of learning by running first, then introduce.

## Element Technologies

- Principle definition: YAML / JSON / Markdown with version control (Git)
- Injection: Template engine (Jinja2, etc.) for synthesizing into system prompts
- Enforcement: Runtime verification with [#30 Policy-as-Code Guardrail](../06-reliability/30-policy-as-code-guardrail.md)
- Auditing: Record change history in Git logs + audit store

## Related Patterns

- [#30 Policy-as-Code Guardrail](../06-reliability/30-policy-as-code-guardrail.md) — Mechanism for enforcing Constitution principles at runtime
- [#53 Agent Change Management](53-agent-change-management.md) — Constitution changes are also subject to change management
- [#33 Prompt/Model/Tool Version Pinning](../07-observability/33-version-pinning.md) — Pin Constitution versions as well

## References

- Anthropic, "Constitutional AI" (2022) — The concept of principle-based AI behavioral control
