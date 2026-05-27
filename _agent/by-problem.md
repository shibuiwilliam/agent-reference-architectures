# Pattern Index by Problem

> Shortcut: if you're diagnosing a specific problem, start here.
> For the complete procedure, see `_agent/README.md`.

## 1. Cost Explosion / Budget Overrun

**Symptoms**: LLM costs exceeding budget, linear cost scaling with request count, no cost control mechanisms
**Related anti-patterns**: ap-01 (Infinite Timeout), ap-03 (Strongest Model Only)
**Remedy patterns**:
- #5 Time-Budgeted Agent Loop — enforce time/cost budgets per request
- #37 Semantic Gateway & Cost-Aware Router — route by difficulty to cheaper models
- #38 Semantic Result Cache — reuse similar results
- #55 Deadline & Budget Cascade — propagate budgets to child agents
- #56 Adaptive Effort — scale compute to task difficulty
**Related dials**: budget-cap, timeout, model-tier-routing

## 2. Hallucination / Factual Errors

**Symptoms**: Agent generates unsupported claims, mixes up facts, confidently states falsehoods
**Related anti-patterns**: ap-05 (Context Stuffing)
**Remedy patterns**:
- #27 Evidence-First Answer — require evidence before answering
- #28 Verifier Agent / Critic — independent verification
- #24 Context Pack / Assembly — proper grounding via RAG
**Related dials**: retrieval-top-k, temperature

## 3. Timeout / Runaway / Unresponsive Agent

**Symptoms**: P99 latency pinned to timeout, connection pool exhaustion, infinite self-correction loops
**Related anti-patterns**: ap-01 (Infinite Timeout)
**Remedy patterns**:
- #5 Time-Budgeted Agent Loop — hard budget limits
- #55 Deadline & Budget Cascade — propagate deadlines to children
- #6 Interruptible Agent — allow mid-execution stop
- #1 Request-to-Job Gateway — decouple from HTTP lifecycle
**Related dials**: timeout, self-correction-loops, budget-cap

## 4. Guardrail False Positives (Legitimate Requests Blocked)

**Symptoms**: >10% false positive rate, users rephrasing to bypass, growing exception lists
**Related anti-patterns**: ap-02 (Excessive Guardrails)
**Remedy patterns**:
- #29 Guardrail Sidecar + Self-Correction — tune thresholds
- #57 Autonomy Ladder — escalate autonomy with track record
- #30 Policy-as-Code Guardrail — explicit, auditable policies
**Related dials**: guardrail-strictness, autonomy-level

## 5. Observability Cost Bloat

**Symptoms**: Observability costs >50% of LLM costs, log storage bloat, alert fatigue
**Related anti-patterns**: ap-04 (Full Observability)
**Remedy patterns**:
- #54 Tiered (Hot/Cold) Observability — split into fast/cheap tiers
- #32 Agent Trace — sample instead of recording everything
**Related dials**: trace-sampling-rate, log-retention

## 6. Security Breach / Prompt Injection

**Symptoms**: Unauthorized data access, prompt injection exploits, agent performing unintended actions
**Related anti-patterns**: (none specific — this is a cross-cutting concern)
**Remedy patterns**:
- #44 Dual-LLM Privilege Separation — isolate untrusted from privileged
- #42 Data Boundary Firewall — inspect/mask PII at boundaries
- #20 Sandboxed Tool Runtime — isolate code execution
- #18 Least-Privilege Tool Binding — minimal permissions per session
- #43 Confused-Deputy Damage Limitation — limit blast radius
**Related dials**: guardrail-strictness, exposed-tool-count

## 7. Side-Effect Inconsistency / Data Corruption

**Symptoms**: Partial updates across systems, no rollback capability, inconsistent state after failures
**Related anti-patterns**: (none specific — prevented by design patterns)
**Remedy patterns**:
- #4 Agent Saga — compensating transactions for rollback
- #19 Dry-Run First Tool Execution — simulate before executing
- #31 Human Approval Checkpoint — human gate before risky actions
- #2 Durable Agent Session — checkpoint state for recovery
**Related dials**: checkpoint-frequency, autonomy-level

## 8. Regression on Model Change

**Symptoms**: Quality drops after model update, outputs change unpredictably, no baseline comparison
**Related anti-patterns**: ap-06 (related)
**Remedy patterns**:
- #33 Prompt/Model/Tool Version Pinning — lock versions
- #34 Evaluation CI/CD — automated regression testing
- #35 Production Replay — replay production logs against new version
- #46 Model Behavior Compatibility Layer — absorb model differences
**Related dials**: prompt-storage

## 9. Scalability Wall (QPS Ceiling)

**Symptoms**: Request queue growing, latency increasing with load, capacity limits reached
**Related anti-patterns**: (infrastructure-level concern)
**Remedy patterns**:
- #1 Request-to-Job Gateway — decouple and scale independently
- #37 Semantic Gateway & Cost-Aware Router — distribute load across models
- #38 Semantic Result Cache — reduce redundant LLM calls
- #39 Prompt Cache Optimized Context — leverage prompt caching
**Related dials**: cache-similarity, model-tier-routing

## 10. Vendor Lock-In

**Symptoms**: Single provider dependency, no migration path, API-specific code throughout
**Related anti-patterns**: (strategic concern)
**Remedy patterns**:
- #45 Agent Runtime Abstraction — abstract execution platform
- #46 Model Behavior Compatibility Layer — absorb model API differences
- #40 Fallback & Graceful Degradation — multi-provider fallback
**Related dials**: (architecture-level decision, no specific dials)
