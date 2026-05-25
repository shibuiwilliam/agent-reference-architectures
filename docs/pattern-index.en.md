---
title: Pattern Quick Reference
---

# Pattern Quick Reference (59 Patterns)

<!-- BEGIN:GEN:pattern-index -->
| # | Pattern | Category | Summary |
|---|---------|----------|---------|
| 1 | [Request-to-Job Gateway](patterns/01-execution/01-request-to-job-gateway.md) | I. Execution | Accept a request as an asynchronous job |
| 2 | [Durable Agent Session](patterns/01-execution/02-durable-agent-session.md) | I. Execution | Persist state to survive interruptions and resumptions |
| 3 | [Workflow Backbone + Agent Node](patterns/01-execution/03-workflow-backbone-agent-node.md) | I. Execution | Deterministic backbone, delegate only decisions |
| 4 | [Agent Saga](patterns/01-execution/04-agent-saga.md) | I. Execution | Roll back side-effect chains with compensations |
| 5 | [Time-Budgeted Agent Loop](patterns/01-execution/05-time-budgeted-agent-loop.md) | I. Execution | Budget time, iterations, and cost to prevent runaway |
| 6 | [Interruptible Agent](patterns/01-execution/06-interruptible-agent.md) | I. Execution | Allow mid-execution stops and course corrections |
| 7 | [Streaming Progress](patterns/01-execution/07-streaming-progress.md) | I. Execution | Stream auditable summaries of progress incrementally |
| 8 | [Planner-Executor-Reviewer](patterns/02-composition/08-planner-executor-reviewer.md) | II. Composition | Separate planning, execution, and review into distinct roles |
| 9 | [Supervisor & Specialist Agents](patterns/02-composition/09-supervisor-specialist-agents.md) | II. Composition | A supervisor delegates to specialist agents |
| 10 | [Agent Ensemble & Debate](patterns/02-composition/10-agent-ensemble-debate.md) | II. Composition | Multiple agents solve and debate for robustness |
| 11 | [Deterministic Core, Probabilistic Edge](patterns/02-composition/11-deterministic-core-probabilistic-edge.md) | II. Composition | Keep the core deterministic, use AI only at the edges |
| 12 | [Blackboard](patterns/02-composition/12-blackboard.md) | II. Composition | Loosely coupled coordination via a shared blackboard |
| 13 | [Natural Language Boundary Adapter](patterns/03-io-contract/13-natural-language-boundary-adapter.md) | III. Contract | Convert natural language to structured intent |
| 14 | [Structured Output Contract](patterns/03-io-contract/14-structured-output-contract.md) | III. Contract | Enforce output via schema contracts |
| 15 | [Inverted Structured Output](patterns/03-io-contract/15-inverted-structured-output.md) | III. Contract | Extract intermediate decisions, not final execution |
| 16 | [Ambiguity Negotiation](patterns/03-io-contract/16-ambiguity-negotiation.md) | III. Contract | Clarify before executing when ambiguous |
| 17 | [Tool / MCP Gateway](patterns/04-tools-mcp/17-tool-mcp-gateway.md) | IV. Tools | Aggregate tool connections with authorization and audit |
| 18 | [Least-Privilege Tool Binding](patterns/04-tools-mcp/18-least-privilege-tool-binding.md) | IV. Tools | Bind minimum privileges per session |
| 19 | [Dry-Run First Tool Execution](patterns/04-tools-mcp/19-dry-run-first-tool-execution.md) | IV. Tools | Simulate side effects first, then approve |
| 20 | [Sandboxed Tool Runtime](patterns/04-tools-mcp/20-sandboxed-tool-runtime.md) | IV. Tools | Execute code/operations in an isolated environment |
| 21 | [MCP Adapter Isolation](patterns/04-tools-mcp/21-mcp-adapter-isolation.md) | IV. Tools | Isolate MCP adapters per trust boundary |
| 22 | [Anti-Corruption Layer](patterns/04-tools-mcp/22-anti-corruption-layer.md) | IV. Tools | A translation layer to prevent concept pollution from legacy systems |
| 23 | [Layered Memory](patterns/05-memory-context/23-layered-memory.md) | V. Memory | Organize memory into short-term, long-term, and shared layers |
| 24 | [Context Pack / Assembly](patterns/05-memory-context/24-context-pack-assembly.md) | V. Memory | Assemble context for grounding |
| 25 | [Memory Write Gate](patterns/05-memory-context/25-memory-write-gate.md) | V. Memory | Require approval for long-term memory writes |
| 26 | [Forgetting and Expiration](patterns/05-memory-context/26-forgetting-and-expiration.md) | V. Memory | Add expiration and freshness to memories |
| 27 | [Evidence-First Answer](patterns/06-reliability/27-evidence-first-answer.md) | VI. Reliability | Retrieve and cite evidence before answering |
| 28 | [Verifier Agent / Critic](patterns/06-reliability/28-verifier-agent-critic.md) | VI. Reliability | Independent verifier for pre-shipment inspection |
| 29 | [Guardrail Sidecar + Self-Correction](patterns/06-reliability/29-guardrail-sidecar-self-correction.md) | VI. Reliability | Inspect I/O and self-correct errors |
| 30 | [Policy-as-Code Guardrail](patterns/06-reliability/30-policy-as-code-guardrail.md) | VI. Reliability | Codify constraints for separate evaluation |
| 31 | [Human Approval Checkpoint](patterns/06-reliability/31-human-approval-checkpoint.md) | VI. Reliability | Require human approval before high-risk actions |
| 32 | [Agent Trace](patterns/07-observability/32-agent-trace.md) | VII. Observability | Log every step as an append-only record for replay |
| 33 | [Prompt/Model/Tool Version Pinning](patterns/07-observability/33-version-pinning.md) | VII. Observability | Pin prompt, model, and tool versions |
| 34 | [Evaluation CI/CD](patterns/07-observability/34-evaluation-ci-cd.md) | VII. Observability | Automated evaluation per change to detect regressions |
| 35 | [Production Replay](patterns/07-observability/35-production-replay.md) | VII. Observability | Replay production logs to compare old and new |
| 36 | [Shadow / Canary Deployment](patterns/07-observability/36-shadow-canary-deployment.md) | VII. Observability | Gradual rollout with automatic rollback |
| 37 | [Semantic Gateway & Cost-Aware Router](patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) | VIII. Cost | Dynamically select models by difficulty |
| 38 | [Semantic Result Cache](patterns/08-cost-scaling/38-semantic-result-cache.md) | VIII. Cost | Reuse semantically similar past results |
| 39 | [Prompt Cache Optimized Context](patterns/08-cost-scaling/39-prompt-cache-optimized-context.md) | VIII. Cost | Leverage cache via common prefixes |
| 40 | [Fallback & Graceful Degradation](patterns/08-cost-scaling/40-fallback-graceful-degradation.md) | VIII. Cost | Continue with staged degradation on failure |
| 41 | [Tenant-Isolated Agent Runtime](patterns/09-security/41-tenant-isolated-agent-runtime.md) | IX. Security | Isolate execution and memory per tenant |
| 42 | [Data Boundary Firewall](patterns/09-security/42-data-boundary-firewall.md) | IX. Security | Inspect and mask PII/secrets at I/O boundaries |
| 43 | [Confused-Deputy Damage Limitation](patterns/09-security/43-confused-deputy-damage-limitation.md) | IX. Security | Limit blast radius even when tricked |
| 44 | [Dual-LLM Privilege Separation](patterns/09-security/44-dual-llm-privilege-separation.md) | IX. Security | Separate quarantined LLM and privileged LLM |
| 45 | [Agent Runtime Abstraction](patterns/10-deployment/45-agent-runtime-abstraction.md) | X. Deployment | Make the execution platform swappable |
| 46 | [Model Behavior Compatibility Layer](patterns/10-deployment/46-model-behavior-compatibility-layer.md) | X. Deployment | A compatibility layer to absorb model differences |
| 47 | [Agent Capability Registry](patterns/10-deployment/47-agent-capability-registry.md) | X. Deployment | Manage capabilities, permissions, and costs in a registry |
| 48 | [Strangler Fig](patterns/10-deployment/48-strangler-fig.md) | X. Deployment | Gradually replace existing processing |
| 49 | [Agent Workbench](patterns/11-ux/49-agent-workbench.md) | XI. UX | Manage plans, progress, and approvals in a single view |
| 50 | [Editable Plan](patterns/11-ux/50-editable-plan.md) | XI. UX | Let humans edit the plan before execution |
| 51 | [Agent-to-Human Escalation](patterns/11-ux/51-agent-to-human-escalation.md) | XI. UX | Escalate to humans when confidence or authority is insufficient |
| 52 | [Agent Constitution](patterns/12-governance/52-agent-constitution.md) | XII. Governance | Systematically deploy behavioral principles |
| 53 | [Agent Change Management](patterns/12-governance/53-agent-change-management.md) | XII. Governance | Subject changes to strict CI/canary processes |
| 54 | [Tiered (Hot/Cold) Observability](patterns/07-observability/54-tiered-observability.md) | VII. Observability | Split observability into hot (fast) and cold (cheap) tiers |
| 55 | [Deadline & Budget Cascade](patterns/01-execution/55-deadline-budget-cascade.md) | I. Execution | Propagate deadlines and budgets down the call tree |
| 56 | [Adaptive Effort](patterns/08-cost-scaling/56-adaptive-effort.md) | VIII. Cost | Scale compute effort up or down by difficulty |
| 57 | [Autonomy Ladder](patterns/06-reliability/57-autonomy-ladder.md) | VI. Reliability | Gradually promote autonomy based on track record |
| 58 | [Sync Facade over Async Core](patterns/01-execution/58-sync-facade-over-async-core.md) | I. Execution | Respond synchronously if fast enough, promote to async otherwise |
| 59 | [Workflow--Agent Spectrum Selector](patterns/01-execution/59-workflow-agent-spectrum-selector.md) | I. Execution | Select determinism vs. autonomy per subtask |
<!-- END:GEN:pattern-index -->
