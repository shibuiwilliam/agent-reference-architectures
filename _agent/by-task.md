# Pattern Index by Task Type

> Shortcut: if you know what you're building, start here instead of the full decision algorithm.
> For the complete procedure, see `_agent/README.md`.

## 1. Internal Chatbot / Conversational AI

**Typical forces**: F1=high, F2=low, F5=high, F6=low, F7=mid

- **Required**: #14 Structured Output Contract, #24 Context Pack / Assembly
- **Recommended**: #38 Semantic Result Cache, #58 Sync Facade over Async Core
- **If F5=low** (untrusted input): add #13 NL Boundary Adapter, #29 Guardrail Sidecar, #42 Data Boundary Firewall
- **If F7=high** (cost pressure): add #37 Semantic Gateway, #56 Adaptive Effort

**Reference architecture**: [MVP](docs/reference-architectures/01-mvp.md) + cache layer

## 2. End-User Chatbot / Conversational AI

**Typical forces**: F1=high, F2=mid, F5=low, F7=high

- **Required**: #13 NL Boundary Adapter, #14 Structured Output Contract, #24 Context Pack, #29 Guardrail Sidecar
- **Recommended**: #37 Semantic Gateway, #38 Semantic Result Cache, #42 Data Boundary Firewall
- **If F8=high** (audit/compliance): add #32 Agent Trace, #30 Policy-as-Code Guardrail

**Reference architecture**: [Cost-First](docs/reference-architectures/05-cost-first.md) + [Untrusted-Input](docs/reference-architectures/03-untrusted-input.md)

## 3. Code Generation / Coding Agent

**Typical forces**: F1=low, F2=high, F6=high

- **Required**: #20 Sandboxed Tool Runtime, #28 Verifier Agent, #8 Planner-Executor-Reviewer
- **Recommended**: #34 Evaluation CI/CD, #18 Least-Privilege Tool Binding
- **If F2=high** (high failure cost): add #19 Dry-Run First, #31 Human Approval Checkpoint

**Reference architecture**: [Side-Effect-First](docs/reference-architectures/02-side-effect-first.md)

## 4. Data Processing / Analysis Pipeline

**Typical forces**: F4=high, F6=low, F8=mid–high

- **Required**: #1 Request-to-Job Gateway, #3 Workflow Backbone + Agent Node
- **Recommended**: #5 Time-Budgeted Agent Loop, #32 Agent Trace, #55 Deadline & Budget Cascade
- **If F1=low** (irreversible operations): add #4 Agent Saga, #2 Durable Agent Session

**Reference architecture**: [MVP](docs/reference-architectures/01-mvp.md) with workflow backbone

## 5. RAG / Knowledge Search System

**Typical forces**: F2=mid, F4=mid, F7=mid–high

- **Required**: #24 Context Pack / Assembly, #27 Evidence-First Answer
- **Recommended**: #38 Semantic Result Cache, #39 Prompt Cache Optimized Context
- **If F2=high** (high accuracy required): add #28 Verifier Agent, #10 Agent Ensemble & Debate

**Reference architecture**: [MVP](docs/reference-architectures/01-mvp.md) + evidence layer

## 6. Side-Effect Agent (Payment / Booking / External API)

**Typical forces**: F1=low, F2=high, F8=high

- **Required**: #4 Agent Saga, #19 Dry-Run First, #31 Human Approval Checkpoint, #32 Agent Trace
- **Recommended**: #3 Workflow Backbone, #15 Inverted Structured Output, #33 Version Pinning
- **If F9=low** (unreliable provider): add #40 Fallback & Graceful Degradation

**Reference architecture**: [Side-Effect-First](docs/reference-architectures/02-side-effect-first.md)

## 7. Multi-Agent / Complex Task Decomposition

**Typical forces**: F6=high, F3=high

- **Required**: #9 Supervisor & Specialist Agents, #55 Deadline & Budget Cascade
- **Recommended**: #12 Blackboard, #5 Time-Budgeted Agent Loop, #32 Agent Trace
- **If F2=high** (high failure cost): add #8 Planner-Executor-Reviewer, #10 Agent Ensemble & Debate

**Reference architecture**: depends on force profile; often [Side-Effect-First](docs/reference-architectures/02-side-effect-first.md) or [Continuous-Improvement](docs/reference-architectures/06-continuous-improvement.md)

## 8. Customer Support / Helpdesk

**Typical forces**: F4=low, F5=low, F7=high

- **Required**: #37 Semantic Gateway, #13 NL Boundary Adapter, #29 Guardrail Sidecar
- **Recommended**: #38 Semantic Result Cache, #7 Streaming Progress, #40 Fallback & Graceful Degradation
- **If F2=mid+** (actions with consequences): add #51 Agent-to-Human Escalation

**Reference architecture**: [Cost-First](docs/reference-architectures/05-cost-first.md) + [Untrusted-Input](docs/reference-architectures/03-untrusted-input.md)
