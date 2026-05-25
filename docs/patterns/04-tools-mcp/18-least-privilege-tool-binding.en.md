---
title: "Least-Privilege Tool Binding"
tags:
  - "Tools, MCP & External System Integration"
  - "F5 Input Trustworthiness"
  - "F2 Failure Cost"
---

# #18 Least-Privilege Tool Binding

!!! abstract "TL;DR"
    **Bind the tools available to an agent to the minimum necessary per session, task, and user**, preventing unnecessary privileges.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #18 Least-Privilege Tool Binding</summary>

| Field | Value |
|------|-----|
| **ID** | 18 |
| **Category** | 04-tools-mcp — Tools, MCP & External System Integration |
| **Forces** | `[F5]`, `[F2]` |
| **Dials** | exposed-tool-count |
| **Tradeoffs** | — |
| **Related Patterns** | #17, #43, #44 |
| **When to Use** | 10+ tools, multi-tenant, per-user permission differences |
| **When Not to Use** | 2–3 tools with uniform permissions for all users; exploratory discovery needed |
| **Element Technologies** | MCP tools/list filtering, RBAC/ABAC, OPA/Cedar |

</details>
<!-- END:GEN:meta -->

## Overview

If a support agent can see database deletion privileges and infrastructure change tools, a single prompt injection could execute an irreversible operation. As the number of tools grows, the risk of "tools that were never intended to be called getting called" increases.

This pattern dynamically narrows the available tool set at session start based on task type, user permissions, and context. From the agent's perspective, "tools that don't exist can't be called," structurally reducing the attack surface and blast radius of accidents.

!!! info "Position in Decision Framework"
    - **Driving Forces**: `[F5]` Input Trustworthiness, `[F2]` Failure Cost
    - **Related Decisions**: [Tuning Dials](../../decisions/tuning-dials.md) — Exposed Tool Count
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

At session start, the Binder evaluates the user's role, task type, and risk level, extracting only the tools permitted for that session from the tool catalog and injecting them into the agent. Adding tools mid-session requires a re-evaluation.

Permission granularity extends beyond per-tool to include parameter constraints within tools (e.g., prohibiting `delete` while allowing only `read`).

## Problem Solved

"Full tool exposure" causes the agent's selection options to explode, reducing tool selection accuracy while expanding the blast radius. This pattern structurally eliminates `[F5]` injection attack risks against high-privilege tools and limits `[F2]` damage from misuse.

## When to Use / When Not to Use

- **When to Use**: Suitable for systems with many tools (10+) and multi-tenant environments. Particularly effective when users with different permission levels share the same agent.
- **When Not to Use**: Excessive for simple configurations with 2–3 tools and uniform permissions for all users. Also not suited for exploratory tasks that require dynamically discovering tools as work progresses.

## Element Technologies

- MCP `tools/list` filtering
- Tool catalog + RBAC / ABAC engine
- Session-scoped tool set injection (LLM system prompt / tools parameter control)
- OPA / Cedar for policy evaluation

## Related Patterns

- [#17 Tool / MCP Gateway](17-tool-mcp-gateway.md) — The typical implementation location where the gateway enforces permission binding
- [#43 Confused-Deputy Damage Limitation](../09-security/43-confused-deputy-damage-limitation.md) — Limits blast radius when deceived. Least privilege is prevention; Confused-Deputy countermeasures are mitigation
- [#44 Dual-LLM Privilege Separation](../09-security/44-dual-llm-privilege-separation.md) — Stronger isolation that separates LLMs by privilege level

## References

- Principle of Least Privilege (Saltzer & Schroeder, 1975)
