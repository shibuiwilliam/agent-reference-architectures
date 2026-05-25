---
title: "Confused-Deputy Damage Limitation"
tags:
  - "Security & Multi-tenancy"
  - "F5 Input Trustworthiness"
---

# #43 Confused-Deputy Damage Limitation

!!! abstract "TL;DR"
    Even if the agent is deceived by prompt injection, structurally limit the scope of damage.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #43 Confused-Deputy Damage Limitation</summary>

| Field | Value |
|------|-----|
| **ID** | 43 |
| **Category** | 09-security — Security & Multi-tenancy |
| **Forces** | `[F5]` |
| **Dials** | — |
| **Tradeoffs** | — |
| **Related Patterns** | #44, #41, #18, #4 |
| **When to Use** | External data processing (email, web, user input), high-impact tool access |
| **When Not to Use** | Read-only with no side effects; clear trust boundary (all internal) |
| **Element Technologies** | Least privilege, rate limiter/monetary caps, approval queue, container isolation/RLS |

</details>
<!-- END:GEN:meta -->

## Overview

A malicious instruction embedded in an email body causes the agent to send customer data externally -- preventing such "deceptions" via prompt injection with 100% reliability is extremely difficult with current LLMs.

The Confused Deputy problem refers to a situation where an authorized entity is tricked by a third party into using its authority for unintended operations. LLM agents process natural language input without trust boundaries, creating a constant risk of being "deceived" by indirect prompt injection. This pattern starts from the premise that "deception itself cannot be prevented" and adopts a design that minimizes the blast radius even when the agent is compromised.

!!! info "Position in decision-making"
    - **Driving force**: `[F5]` Input Trustworthiness
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

Damage limitation is achieved not through a single component but through combining multiple constraints:

1. **Least privilege**: Bind tool and data access to the minimum necessary per session
2. **Operation caps**: Set limits on writes, monetary amounts, and impact scope per session
3. **Irreversible operation delays**: Do not execute deletions, transfers, or publications immediately -- queue them for approval
4. **Impact scope isolation**: Limit the scope of resources a single agent can access

By layering these, even if a single defense is breached, damage does not propagate to the entire system.

## Problems Solved

Granting broad permissions to an agent means a single prompt injection can cause large-scale damage `[F5]`. When operations with side effects -- email sending, data deletion, code execution, payments -- chain together, damage scales exponentially. Betting defenses on "preventing injection 100%" is unrealistic; designing for "limiting pain even when breached" is essential.

## When to Use / When Not to Use

- **When to Use**: Any agent that processes external data (email bodies, web pages, user input). Agents with access to side-effect-bearing tools.
- **When Not to Use**: Read-only agents with no side effects at all (blast radius is inherently small). However, information leakage is also damage, so truly unnecessary cases are rare.

## Element Technologies

- Permission control: Per-session application of [#18 Least-Privilege Tool Binding](../04-tools-mcp/18-least-privilege-tool-binding.md)
- Operation limits: Rate limiter, monetary caps, affected row caps
- Approval queue: Combine with [#31 Human Approval Checkpoint](../06-reliability/31-human-approval-checkpoint.md)
- Impact isolation: Container isolation, database Row-Level Security

## Related Patterns

- [#44 Dual-LLM Privilege Separation](44-dual-llm-privilege-separation.md) — A concrete implementation of damage limitation through privilege separation
- [#41 Tenant-Isolated Agent Runtime](41-tenant-isolated-agent-runtime.md) — Limit blast radius via tenant-level isolation
- [#18 Least-Privilege Tool Binding](../04-tools-mcp/18-least-privilege-tool-binding.md) — Apply the principle of least privilege to tools
- [#4 Agent Saga](../01-execution/04-agent-saga.md) — Roll back via compensating transactions when damage occurs

## References

- Simon Willison, "Prompt injection and the confused deputy problem" (2023)
