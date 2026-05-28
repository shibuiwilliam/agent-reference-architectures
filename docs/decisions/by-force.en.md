---
title: Reverse Lookup by Force
---

# Reverse Lookup by Force

!!! abstract "TL;DR"
    Reverse-lookup related either-or decisions, dials, and patterns from forces (driving variables).

## How to Use

"Failure cost is high — which patterns should I consider?" — This reverse lookup is handy for exactly that kind of question. Starting from the variables rated "High" in your [force evaluation](../foundations/forces.md), you can look up related decisions and patterns. Both what to **pay special attention to** when a force is "high" and what can be **relaxed** when it is "low" are shown.

---

## `[F1]` Reversibility — Can Failures Be Undone?

| Type | Item | When F1 is **Low** (irreversible) |
|------|------|--------------------------|
| Either-Or | Sync vs. Async | Use async + checkpoints to enable rollback |
| Either-Or | Plan vs. ReAct | Use plan-first to get approval before side effects |
| Dial | Checkpoint frequency | Increase to every step |
| Dial | Autonomy level | Set low and require human approval |
| Pattern | [#4 Agent Saga](../decisions/dials/checkpoint-frequency.md) | Roll back with compensating transactions |
| Pattern | [#19 Dry-Run First](../foundations/forces/f1-reversibility.md) | Verify with simulated execution before executing |
| Pattern | [#31 Human Approval](../decisions/dials/autonomy-level.md) | Human approval before high-risk operations |

---

## `[F2]` Failure Cost — Financial/Legal/Safety Impact

| Type | Item | When F2 is **High** (failure is costly) |
|------|------|---------------------------------|
| Either-Or | Plan vs. ReAct | Plan-first (consider the whole picture upfront) |
| Either-Or | Inline vs. Post-hoc Verification | Inline verification (catch before shipping) |
| Either-Or | Same vs. Different-Model Verification | Different model (compensate for same-model blind spots) |
| Dial | Best-of-N | Raise to 3–5 |
| Dial | Guardrail strictness | Set high |
| Dial | HITL frequency | Full approval for high-risk operations |
| Pattern | [#8 Planner-Executor-Reviewer](../decisions/tradeoffs-catalog/plan-vs-react.md) | Separation of planning, execution, and review |
| Pattern | [#10 Agent Ensemble](../decisions/tradeoffs-catalog/same-vs-different-model.md) | Robustness through deliberation |
| Pattern | [#28 Verifier Agent](../decisions/tradeoffs-catalog/inline-vs-post-verification.md) | Independent verification |
| Pattern | [#57 Autonomy Ladder](../decisions/dials/autonomy-level.md) | Gradual autonomy promotion |

---

## `[F3]` Per-Request Value — Contribution to Revenue/Decision-Making

| Type | Item | When F3 is **High** (high-value requests) |
|------|------|----------------------------------|
| Dial | Best-of-N | Raise to 3–5 (cost is acceptable) |
| Dial | Budget cap | Raise to a level commensurate with request value |
| Dial | Model tier | Prefer larger models |
| Either-Or | Fail-fast vs. Degradation | Graceful degradation (don't drop high-value requests) |
| Pattern | [#10 Agent Ensemble](../decisions/tradeoffs-catalog/same-vs-different-model.md) | Quality improvement through deliberation |
| Pattern | [#37 Semantic Gateway](../decisions/dials/model-tier-routing.md) | Model selection based on value |

---

## `[F4]` Latency Budget — User Tolerance for Waiting

| Type | Item | When F4 is **Short** (immediate response expected) |
|------|------|------------------------------|
| Either-Or | Sync vs. Async | Sync (or [#58 Sync Facade](../decisions/tradeoffs-catalog/sync-vs-async.md)) |
| Either-Or | Inline vs. Post-hoc Verification | Post-hoc verification (latency priority) |
| Dial | Self-correction loop count | 0–1 times (time constraint) |
| Dial | Retrieval top-k | Lower (reduce search time) |
| Pattern | [#7 Streaming Progress](../decisions/tradeoffs-catalog/push-vs-pull.md) | Show progress while waiting |
| Pattern | [#38 Semantic Result Cache](../decisions/dials/cache-similarity.md) | Reduce latency with caching |
| Pattern | [#39 Prompt Cache](../foundations/forces/f7-cost-sensitivity.md) | Speed up with prefix sharing |

---

## `[F5]` Input Trustworthiness — Likelihood of Attack/Contamination

| Type | Item | When F5 is **Low** (untrusted input) |
|------|------|----------------------------------|
| Dial | Guardrail strictness | Set high |
| Dial | Exposed tool count | Minimize |
| Pattern | [#13 NL Boundary Adapter](../foundations/forces/f5-input-trust.md) | Structured input |
| Pattern | [#42 Data Boundary Firewall](../foundations/forces/f5-input-trust.md) | PII/injection inspection |
| Pattern | [#43 Confused-Deputy](../foundations/forces/f5-input-trust.md) | Blast radius limitation |
| Pattern | [#44 Dual-LLM](../foundations/forces/f5-input-trust.md) | Separation of quarantine LLM and privileged LLM |
| Pattern | [#18 Least-Privilege](../decisions/dials/exposed-tool-count.md) | Least privilege |

---

## `[F6]` Task Variability — Routine vs. Exploratory

| Type | Item | When F6 is **High** (exploratory) |
|------|------|--------------------------|
| Either-Or | Workflow vs. Agent | Agent (autonomous exploration) |
| Either-Or | Single vs. Multi-Agent | Multi if expertise can be separated |
| Dial | Temperature | 0.5–0.8 (diversity-focused) |
| Pattern | [#59 Spectrum Selector](../decisions/tradeoffs-catalog/workflow-vs-agent.md) | Decide per subtask |
| Pattern | [#12 Blackboard](../decisions/tradeoffs-catalog/orchestration-vs-choreography.md) | Loosely-coupled coordination |

When F6 is **Low** (routine) → Prefer workflow, [#3 Workflow Backbone](../decisions/tradeoffs-catalog/workflow-vs-agent.md), [#11 Deterministic Core](../decisions/tradeoffs-catalog/prompt-vs-code.md).

---

## `[F7]` Cost Sensitivity / Scale — QPS, Monthly Cost Ceiling

| Type | Item | When F7 is **High** (tight cost constraints) |
|------|------|----------------------------------|
| Either-Or | Single vs. Multi-Provider | Multi for cost comparison |
| Dial | Model tier threshold | Raise to increase smaller model usage |
| Dial | Cache similarity threshold | Slightly relax to improve hit rate |
| Dial | Trace sampling rate | Limit to 1–5% |
| Pattern | [#37 Semantic Gateway](../decisions/dials/model-tier-routing.md) | Difficulty-based routing |
| Pattern | [#38 Semantic Result Cache](../decisions/dials/cache-similarity.md) | Result reuse |
| Pattern | [#56 Adaptive Effort](../foundations/forces/f7-cost-sensitivity.md) | Dynamic computation adjustment |
| Pattern | [#5 Time-Budgeted](../decisions/dials/budget-cap.md) | Budget ceiling |

---

## `[F8]` Accountability / Regulation — Audit & Compliance Requirements

| Type | Item | When F8 is **High** (regulated industry) |
|------|------|----------------------------|
| Dial | Trace sampling rate | 100% (full recording required) |
| Dial | Log retention period | 1–7 years (regulatory compliance) |
| Dial | Prompt storage granularity | All versions Git-managed |
| Either-Or | Prompt vs. Code Control | Code control (testable and auditable) |
| Either-Or | Structured vs. Free-form Output | Structured (easier to audit) |
| Pattern | [#32 Agent Trace](../decisions/dials/trace-sampling-rate.md) | Complete audit trail |
| Pattern | [#30 Policy-as-Code](../decisions/tradeoffs-catalog/prompt-vs-code.md) | Codified constraints |
| Pattern | [#33 Version Pinning](../decisions/dials/prompt-storage.md) | Reproducibility |
| Pattern | [#52 Agent Constitution](../foundations/forces/f8-accountability.md) | Systematized behavioral principles |

---

## `[F9]` Provider Reliability — External LLM Availability

| Type | Item | When F9 is **Low** (availability concerns) |
|------|------|-------------------------------|
| Either-Or | Single vs. Multi-Provider | Multi-provider |
| Either-Or | Fail-fast vs. Degradation | Graceful degradation |
| Dial | Retry count | 2–3 times + exponential backoff |
| Pattern | [#40 Fallback](../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) | Staged degradation |
| Pattern | [#45 Runtime Abstraction](../decisions/tradeoffs-catalog/build-vs-buy.md) | Provider swappability |
| Pattern | [#46 Compatibility Layer](../decisions/tradeoffs-catalog/single-vs-multi-provider.md) | Model difference absorption |

---

## Related Pages

- [Driving Variables (Forces) F1–F9](../foundations/forces.md) — Force definitions
- [Decision-Making Process](decision-flow.md) — Workflow starting from force evaluation
- [Worked Examples](worked-examples.md) — Concrete examples of force evaluation
