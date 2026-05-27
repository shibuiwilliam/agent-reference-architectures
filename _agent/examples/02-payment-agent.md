# Example Proposal: Payment Processing Agent

> Source: `docs/decisions/worked-examples.md` Example 2
> This demonstrates the `_agent/proposal-template.md` format.

## Architecture Proposal

**Catalog Version**: v1.1.0
**Target System**: E-commerce payment processing agent

### 1. Requirements Summary

Agent assisting payment processing for an e-commerce site. Handles order confirmation, inventory checks, payment API calls, and confirmation emails. Irreversible operations (payment, email) with high failure cost.

### 2. Force Evaluation

| Force | Rating | Rationale |
|-------|--------|-----------|
| F1 Reversibility | **low** | Payment and email are irreversible |
| F2 Failure Cost | **high** | Incorrect charges require refunds, damage trust |
| F3 Request Value | **high** | Each transaction is thousands of yen |
| F4 Latency Budget | **mid** | ~30 seconds acceptable |
| F5 Input Trust | **mid** | Authenticated users, but natural language input |
| F6 Task Variability | **low** | Fixed flow: order → confirm → pay → notify |
| F7 Cost Sensitivity | **low** | LLM cost is tiny relative to transaction value |
| F8 Accountability | **high** | Payment record retention obligations |
| F9 Provider Reliability | **mid** | Availability matters; human fallback available |

### 3. Tradeoff Decisions

| Tradeoff | Choice | Driving Force | Why not the other side |
|----------|--------|---------------|----------------------|
| Sync ↔ Async | **Async** | F4=mid | Some steps may exceed 30s |
| Plan ↔ ReAct | **Plan-first** | F1=low, F2=high | Must preview before irreversible action |
| Workflow ↔ Agent | **Workflow** | F6=low | Fixed payment flow |
| Inline ↔ Post-hoc Verification | **Inline** | F2=high | Must catch errors before payment |
| Same ↔ Different Model Verification | **Different** | F2=high | Independent verification reduces correlated errors |

### 4. Selected Patterns

| # | Pattern | Reason (driving force) |
|---|---------|----------------------|
| 1 | Request-to-Job Gateway | [F4]=mid: async processing for multi-step flow |
| 3 | Workflow Backbone + Agent Node | [F6]=low: deterministic flow with AI at judgment points |
| 4 | Agent Saga | [F1]=low: compensating transactions for rollback |
| 15 | Inverted Structured Output | [F2]=high: LLM outputs decisions, not actions |
| 19 | Dry-Run First Tool Execution | [F1]=low, [F2]=high: simulate before executing |
| 28 | Verifier Agent / Critic | [F2]=high: independent verification before payment |
| 31 | Human Approval Checkpoint | [F2]=high: human gate before payment execution |
| 32 | Agent Trace | [F8]=high: full audit trail |
| 33 | Version Pinning | [F8]=high: reproducible behavior for audits |

### 5. Dial Settings

| Dial | Initial Value | Driving Force | Adjustment Policy |
|------|--------------|---------------|-------------------|
| Checkpoint frequency | Every step | F1=low | Non-negotiable for irreversible operations |
| Autonomy level | Low (human approval before payment) | F2=high | May escalate with track record via #57 |
| Trace sampling rate | 100% | F8=high | Required by payment record obligations |
| Guardrail strictness | High (amount anomaly detection) | F2=high | Tune false positive rate quarterly |

### 6. Composite Architecture

**Base**: [Side-Effect-First](docs/reference-architectures/02-side-effect-first.md)

```
User → Request-to-Job (#1) → Workflow Backbone (#3)
                                ├→ Inventory Check (agent node)
                                ├→ Dry-Run (#19) → Human Approval (#31) → Payment (#4 Saga)
                                ├→ Verifier (#28) — separate model
                                └→ Confirmation Email
                              Agent Trace (#32) + Version Pinning (#33) throughout
```

### 7. Risks and Mitigations

| Risk | Related Anti-Pattern | Mitigation |
|------|---------------------|------------|
| Double-charge on retry | — | Idempotency keys on all payment API calls |
| Approval fatigue (too many HITL prompts) | ap-02 | Start strict, relax with #57 Autonomy Ladder |
| Saga compensation failure | — | Dead letter queue + manual remediation dashboard |

### 8. Alternatives

| Alternative | Advantages | Why Not Chosen |
|-------------|-----------|----------------|
| ReAct (no plan-first) | Faster for simple cases | F1=low, F2=high: cannot afford unplanned side effects |
| Sync processing | Simpler architecture | Some steps may exceed 30s timeout |

### 9. Unresolved Questions

- [ ] Re-evaluate if F7 rises to high (transaction volume surge) → add routing #37 and cache #38
- [ ] Re-evaluate if F9 drops to low → add Fallback #40
