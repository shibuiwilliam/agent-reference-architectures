---
title: Pattern Quick Reference
---

# Pattern Quick Reference (59 Patterns)

<!-- BEGIN:GEN:pattern-index -->
| # | Pattern | Category | Summary |
|---|---------|----------|---------|
| 1 | [Request-to-Job Gateway](reference-architectures/index.md) | I. Execution | Accept a request as an asynchronous job |
| 2 | [Durable Agent Session](reference-architectures/index.md) | I. Execution | Persist state to survive interruptions and resumptions |
| 3 | [Workflow Backbone + Agent Node](reference-architectures/index.md) | I. Execution | Deterministic backbone, delegate only decisions |
| 4 | [Agent Saga](reference-architectures/index.md) | I. Execution | Roll back side-effect chains with compensations |
| 5 | [Time-Budgeted Agent Loop](reference-architectures/index.md) | I. Execution | Budget time, iterations, and cost to prevent runaway |
| 6 | [Interruptible Agent](reference-architectures/index.md) | I. Execution | Allow mid-execution stops and course corrections |
| 7 | [Streaming Progress](reference-architectures/index.md) | I. Execution | Stream auditable summaries of progress incrementally |
| 8 | [Planner-Executor-Reviewer](reference-architectures/index.md) | II. Composition | Separate planning, execution, and review into distinct roles |
| 9 | [Supervisor & Specialist Agents](reference-architectures/index.md) | II. Composition | A supervisor delegates to specialist agents |
| 10 | [Agent Ensemble & Debate](reference-architectures/index.md) | II. Composition | Multiple agents solve and debate for robustness |
| 11 | [Deterministic Core, Probabilistic Edge](reference-architectures/index.md) | II. Composition | Keep the core deterministic, use AI only at the edges |
| 12 | [Blackboard](reference-architectures/index.md) | II. Composition | Loosely coupled coordination via a shared blackboard |
| 13 | [Natural Language Boundary Adapter](reference-architectures/index.md) | III. Contract | Convert natural language to structured intent |
| 14 | [Structured Output Contract](reference-architectures/index.md) | III. Contract | Enforce output via schema contracts |
| 15 | [Inverted Structured Output](reference-architectures/index.md) | III. Contract | Extract intermediate decisions, not final execution |
| 16 | [Ambiguity Negotiation](reference-architectures/index.md) | III. Contract | Clarify before executing when ambiguous |
| 17 | [Tool / MCP Gateway](reference-architectures/index.md) | IV. Tools | Aggregate tool connections with authorization and audit |
| 18 | [Least-Privilege Tool Binding](reference-architectures/index.md) | IV. Tools | Bind minimum privileges per session |
| 19 | [Dry-Run First Tool Execution](reference-architectures/index.md) | IV. Tools | Simulate side effects first, then approve |
| 20 | [Sandboxed Tool Runtime](reference-architectures/index.md) | IV. Tools | Execute code/operations in an isolated environment |
| 21 | [MCP Adapter Isolation](reference-architectures/index.md) | IV. Tools | Isolate MCP adapters per trust boundary |
| 22 | [Anti-Corruption Layer](reference-architectures/index.md) | IV. Tools | A translation layer to prevent concept pollution from legacy systems |
| 23 | [Layered Memory](reference-architectures/index.md) | V. Memory | Organize memory into short-term, long-term, and shared layers |
| 24 | [Context Pack / Assembly](reference-architectures/index.md) | V. Memory | Assemble context for grounding |
| 25 | [Memory Write Gate](reference-architectures/index.md) | V. Memory | Require approval for long-term memory writes |
| 26 | [Forgetting and Expiration](reference-architectures/index.md) | V. Memory | Add expiration and freshness to memories |
| 27 | [Evidence-First Answer](reference-architectures/index.md) | VI. Reliability | Retrieve and cite evidence before answering |
| 28 | [Verifier Agent / Critic](reference-architectures/index.md) | VI. Reliability | Independent verifier for pre-shipment inspection |
| 29 | [Guardrail Sidecar + Self-Correction](reference-architectures/index.md) | VI. Reliability | Inspect I/O and self-correct errors |
| 30 | [Policy-as-Code Guardrail](reference-architectures/index.md) | VI. Reliability | Codify constraints for separate evaluation |
| 31 | [Human Approval Checkpoint](reference-architectures/index.md) | VI. Reliability | Require human approval before high-risk actions |
| 32 | [Agent Trace](reference-architectures/index.md) | VII. Observability | Log every step as an append-only record for replay |
| 33 | [Prompt/Model/Tool Version Pinning](reference-architectures/index.md) | VII. Observability | Pin prompt, model, and tool versions |
| 34 | [Evaluation CI/CD](reference-architectures/index.md) | VII. Observability | Automated evaluation per change to detect regressions |
| 35 | [Production Replay](reference-architectures/index.md) | VII. Observability | Replay production logs to compare old and new |
| 36 | [Shadow / Canary Deployment](reference-architectures/index.md) | VII. Observability | Gradual rollout with automatic rollback |
| 37 | [Semantic Gateway & Cost-Aware Router](reference-architectures/index.md) | VIII. Cost | Dynamically select models by difficulty |
| 38 | [Semantic Result Cache](reference-architectures/index.md) | VIII. Cost | Reuse semantically similar past results |
| 39 | [Prompt Cache Optimized Context](reference-architectures/index.md) | VIII. Cost | Leverage cache via common prefixes |
| 40 | [Fallback & Graceful Degradation](reference-architectures/index.md) | VIII. Cost | Continue with staged degradation on failure |
| 41 | [Tenant-Isolated Agent Runtime](reference-architectures/index.md) | IX. Security | Isolate execution and memory per tenant |
| 42 | [Data Boundary Firewall](reference-architectures/index.md) | IX. Security | Inspect and mask PII/secrets at I/O boundaries |
| 43 | [Confused-Deputy Damage Limitation](reference-architectures/index.md) | IX. Security | Limit blast radius even when tricked |
| 44 | [Dual-LLM Privilege Separation](reference-architectures/index.md) | IX. Security | Separate quarantined LLM and privileged LLM |
| 45 | [Agent Runtime Abstraction](reference-architectures/index.md) | X. Deployment | Make the execution platform swappable |
| 46 | [Model Behavior Compatibility Layer](reference-architectures/index.md) | X. Deployment | A compatibility layer to absorb model differences |
| 47 | [Agent Capability Registry](reference-architectures/index.md) | X. Deployment | Manage capabilities, permissions, and costs in a registry |
| 48 | [Strangler Fig](reference-architectures/index.md) | X. Deployment | Gradually replace existing processing |
| 49 | [Agent Workbench](reference-architectures/index.md) | XI. UX | Manage plans, progress, and approvals in a single view |
| 50 | [Editable Plan](reference-architectures/index.md) | XI. UX | Let humans edit the plan before execution |
| 51 | [Agent-to-Human Escalation](reference-architectures/index.md) | XI. UX | Escalate to humans when confidence or authority is insufficient |
| 52 | [Agent Constitution](reference-architectures/index.md) | XII. Governance | Systematically deploy behavioral principles |
| 53 | [Agent Change Management](reference-architectures/index.md) | XII. Governance | Subject changes to strict CI/canary processes |
| 54 | [Tiered (Hot/Cold) Observability](reference-architectures/index.md) | VII. Observability | Split observability into hot (fast) and cold (cheap) tiers |
| 55 | [Deadline & Budget Cascade](reference-architectures/index.md) | I. Execution | Propagate deadlines and budgets down the call tree |
| 56 | [Adaptive Effort](reference-architectures/index.md) | VIII. Cost | Scale compute effort up or down by difficulty |
| 57 | [Autonomy Ladder](reference-architectures/index.md) | VI. Reliability | Gradually promote autonomy based on track record |
| 58 | [Sync Facade over Async Core](reference-architectures/index.md) | I. Execution | Respond synchronously if fast enough, promote to async otherwise |
| 59 | [Workflow--Agent Spectrum Selector](reference-architectures/index.md) | I. Execution | Select determinism vs. autonomy per subtask |
<!-- END:GEN:pattern-index -->
