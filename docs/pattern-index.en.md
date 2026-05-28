---
title: Pattern Quick Reference
---

# Pattern Quick Reference (59 Patterns)

<!-- BEGIN:GEN:pattern-index -->
| # | Pattern | Category | Summary |
|---|---------|----------|---------|
| 1 | [Request-to-Job Gateway](glossary.md) | I. Execution | Accept a request as an asynchronous job |
| 2 | [Durable Agent Session](glossary.md) | I. Execution | Persist state to survive interruptions and resumptions |
| 3 | [Workflow Backbone + Agent Node](glossary.md) | I. Execution | Deterministic backbone, delegate only decisions |
| 4 | [Agent Saga](glossary.md) | I. Execution | Roll back side-effect chains with compensations |
| 5 | [Time-Budgeted Agent Loop](glossary.md) | I. Execution | Budget time, iterations, and cost to prevent runaway |
| 6 | [Interruptible Agent](glossary.md) | I. Execution | Allow mid-execution stops and course corrections |
| 7 | [Streaming Progress](glossary.md) | I. Execution | Stream auditable summaries of progress incrementally |
| 8 | [Planner-Executor-Reviewer](glossary.md) | II. Composition | Separate planning, execution, and review into distinct roles |
| 9 | [Supervisor & Specialist Agents](glossary.md) | II. Composition | A supervisor delegates to specialist agents |
| 10 | [Agent Ensemble & Debate](glossary.md) | II. Composition | Multiple agents solve and debate for robustness |
| 11 | [Deterministic Core, Probabilistic Edge](glossary.md) | II. Composition | Keep the core deterministic, use AI only at the edges |
| 12 | [Blackboard](glossary.md) | II. Composition | Loosely coupled coordination via a shared blackboard |
| 13 | [Natural Language Boundary Adapter](glossary.md) | III. Contract | Convert natural language to structured intent |
| 14 | [Structured Output Contract](glossary.md) | III. Contract | Enforce output via schema contracts |
| 15 | [Inverted Structured Output](glossary.md) | III. Contract | Extract intermediate decisions, not final execution |
| 16 | [Ambiguity Negotiation](glossary.md) | III. Contract | Clarify before executing when ambiguous |
| 17 | [Tool / MCP Gateway](glossary.md) | IV. Tools | Aggregate tool connections with authorization and audit |
| 18 | [Least-Privilege Tool Binding](glossary.md) | IV. Tools | Bind minimum privileges per session |
| 19 | [Dry-Run First Tool Execution](glossary.md) | IV. Tools | Simulate side effects first, then approve |
| 20 | [Sandboxed Tool Runtime](glossary.md) | IV. Tools | Execute code/operations in an isolated environment |
| 21 | [MCP Adapter Isolation](glossary.md) | IV. Tools | Isolate MCP adapters per trust boundary |
| 22 | [Anti-Corruption Layer](glossary.md) | IV. Tools | A translation layer to prevent concept pollution from legacy systems |
| 23 | [Layered Memory](glossary.md) | V. Memory | Organize memory into short-term, long-term, and shared layers |
| 24 | [Context Pack / Assembly](glossary.md) | V. Memory | Assemble context for grounding |
| 25 | [Memory Write Gate](glossary.md) | V. Memory | Require approval for long-term memory writes |
| 26 | [Forgetting and Expiration](glossary.md) | V. Memory | Add expiration and freshness to memories |
| 27 | [Evidence-First Answer](glossary.md) | VI. Reliability | Retrieve and cite evidence before answering |
| 28 | [Verifier Agent / Critic](glossary.md) | VI. Reliability | Independent verifier for pre-shipment inspection |
| 29 | [Guardrail Sidecar + Self-Correction](glossary.md) | VI. Reliability | Inspect I/O and self-correct errors |
| 30 | [Policy-as-Code Guardrail](glossary.md) | VI. Reliability | Codify constraints for separate evaluation |
| 31 | [Human Approval Checkpoint](glossary.md) | VI. Reliability | Require human approval before high-risk actions |
| 32 | [Agent Trace](glossary.md) | VII. Observability | Log every step as an append-only record for replay |
| 33 | [Prompt/Model/Tool Version Pinning](glossary.md) | VII. Observability | Pin prompt, model, and tool versions |
| 34 | [Evaluation CI/CD](glossary.md) | VII. Observability | Automated evaluation per change to detect regressions |
| 35 | [Production Replay](glossary.md) | VII. Observability | Replay production logs to compare old and new |
| 36 | [Shadow / Canary Deployment](glossary.md) | VII. Observability | Gradual rollout with automatic rollback |
| 37 | [Semantic Gateway & Cost-Aware Router](glossary.md) | VIII. Cost | Dynamically select models by difficulty |
| 38 | [Semantic Result Cache](glossary.md) | VIII. Cost | Reuse semantically similar past results |
| 39 | [Prompt Cache Optimized Context](glossary.md) | VIII. Cost | Leverage cache via common prefixes |
| 40 | [Fallback & Graceful Degradation](glossary.md) | VIII. Cost | Continue with staged degradation on failure |
| 41 | [Tenant-Isolated Agent Runtime](glossary.md) | IX. Security | Isolate execution and memory per tenant |
| 42 | [Data Boundary Firewall](glossary.md) | IX. Security | Inspect and mask PII/secrets at I/O boundaries |
| 43 | [Confused-Deputy Damage Limitation](glossary.md) | IX. Security | Limit blast radius even when tricked |
| 44 | [Dual-LLM Privilege Separation](glossary.md) | IX. Security | Separate quarantined LLM and privileged LLM |
| 45 | [Agent Runtime Abstraction](glossary.md) | X. Deployment | Make the execution platform swappable |
| 46 | [Model Behavior Compatibility Layer](glossary.md) | X. Deployment | A compatibility layer to absorb model differences |
| 47 | [Agent Capability Registry](glossary.md) | X. Deployment | Manage capabilities, permissions, and costs in a registry |
| 48 | [Strangler Fig](glossary.md) | X. Deployment | Gradually replace existing processing |
| 49 | [Agent Workbench](glossary.md) | XI. UX | Manage plans, progress, and approvals in a single view |
| 50 | [Editable Plan](glossary.md) | XI. UX | Let humans edit the plan before execution |
| 51 | [Agent-to-Human Escalation](glossary.md) | XI. UX | Escalate to humans when confidence or authority is insufficient |
| 52 | [Agent Constitution](glossary.md) | XII. Governance | Systematically deploy behavioral principles |
| 53 | [Agent Change Management](glossary.md) | XII. Governance | Subject changes to strict CI/canary processes |
| 54 | [Tiered (Hot/Cold) Observability](glossary.md) | VII. Observability | Split observability into hot (fast) and cold (cheap) tiers |
| 55 | [Deadline & Budget Cascade](glossary.md) | I. Execution | Propagate deadlines and budgets down the call tree |
| 56 | [Adaptive Effort](glossary.md) | VIII. Cost | Scale compute effort up or down by difficulty |
| 57 | [Autonomy Ladder](glossary.md) | VI. Reliability | Gradually promote autonomy based on track record |
| 58 | [Sync Facade over Async Core](glossary.md) | I. Execution | Respond synchronously if fast enough, promote to async otherwise |
| 59 | [Workflow--Agent Spectrum Selector](glossary.md) | I. Execution | Select determinism vs. autonomy per subtask |
<!-- END:GEN:pattern-index -->
