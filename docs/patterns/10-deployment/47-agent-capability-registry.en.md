---
title: "Agent Capability Registry"
tags:
  - "Deployment, Vendor Abstraction & Migration"
  - "F8 Accountability & Regulation"
---

# #47 Agent Capability Registry

!!! abstract "TL;DR"
    Centrally manage each agent's capabilities, permissions, costs, and status in a registry.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #47 Agent Capability Registry</summary>

| Field | Value |
|------|-----|
| **ID** | 47 |
| **Category** | 10-deployment — Deployment, Vendor Abstraction & Migration |
| **Forces** | `[F8]` |
| **Dials** | — |
| **Tradeoffs** | — |
| **Related Patterns** | #45, #9, #37 |
| **When to Use** | 10+ agents in operation, audit/compliance requirements, agent cost/SLA visibility |
| **When Not to Use** | 1-3 agents where config files suffice; no discovery needed |
| **Element Technologies** | PostgreSQL/DynamoDB, etcd/Consul, gRPC/REST, management dashboard |

</details>
<!-- END:GEN:meta -->

## Overview

Once an organization exceeds about 10 agents, situations arise where no one knows "which agent should handle this question" or "what permissions does that agent have." When you need to determine the impact scope during an incident, relying on tribal knowledge delays the response.

This pattern registers structured metadata per agent -- capability descriptions, available tools, permission scopes, cost actuals, health status -- in a registry, using it for discovery, routing, and auditing. Think of it as the agent equivalent of a service registry in a service mesh.

!!! info "Position in decision-making"
    - **Driving force**: `[F8]` Accountability & Regulation
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

Each agent registers its capabilities to the registry at startup or deploy time. The registry holds the following fields:

- `agent_id`: Unique identifier
- `capabilities`: List of supported task types
- `tools`: Bound tool list and permission scopes
- `cost_profile`: Average token consumption and API call unit costs
- `status`: active / degraded / offline
- `version`: Prompt, model, and tool versions

Orchestrators and routers reference the registry to route tasks to appropriate agents. During audits, registry snapshots can reconstruct "who could do what."

## Problems Solved

Beyond 10 agents, issues like capability overlap, excessive permissions, and cost overruns become hard to grasp `[F8]`. When "what can that agent do" becomes tribal knowledge, identifying the impact scope during incidents is delayed. Registry-based visibility and search solve these challenges.

## When to Use / When Not to Use

- **When to Use**: Multi-agent environments, organizations where agent count is growing. Cases with audit or compliance requirements.
- **When Not to Use**: Small-scale environments with just 1-2 agents -- becomes over-engineering. If configuration files suffice for management at the current stage, there is no rush to adopt.

## Element Technologies

- Storage: PostgreSQL / DynamoDB (structured metadata), etcd / Consul (health management)
- Schema: JSON Schema / OpenAPI extensions for describing agent capabilities
- Discovery: gRPC / REST for router-to-registry lookups
- Visualization: Management dashboard displaying agent list, costs, and status

## Related Patterns

- [#45 Agent Runtime Abstraction](45-agent-runtime-abstraction.md) — Record capabilities of abstracted runtimes in the registry
- [#9 Supervisor & Specialist Agents](../02-composition/09-supervisor-specialist-agents.md) — Supervisor references the registry to route to specialist agents
- [#37 Semantic Gateway & Cost-Aware Router](../08-cost-scaling/37-semantic-gateway-cost-aware-router.md) — Use registry cost information for dynamic routing

## References

- Service Registry pattern in microservices (Consul, Eureka)
