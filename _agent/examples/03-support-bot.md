# Example Proposal: High-Volume Customer Support Bot

> Source: `docs/decisions/worked-examples.md` Example 3
> This demonstrates the `_agent/proposal-template.md` format.

## Architecture Proposal

**Catalog Version**: v1.1.0
**Target System**: Customer support chatbot (100K queries/month)

### 1. Requirements Summary

Customer support chatbot handling 100K monthly inquiries. Covers FAQ answers, order status lookups, and return procedure guidance. End-users interact directly. Mix of routine FAQs and non-routine consultations.

### 2. Force Evaluation

| Force | Rating | Rationale |
|-------|--------|-----------|
| F1 Reversibility | **mid** | FAQ answers are reversible; return procedures are partially irreversible |
| F2 Failure Cost | **mid** | Wrong guidance causes complaints but isn't catastrophic |
| F3 Request Value | **low** | High volume of routine inquiries |
| F4 Latency Budget | **low** | First response within 3 seconds |
| F5 Input Trust | **low** | Unidentified end-users with free-form text |
| F6 Task Variability | **mid** | Mix of routine FAQ and non-routine consultation |
| F7 Cost Sensitivity | **high** | 100K/month scale requires cost control |
| F8 Accountability | **mid** | Customer interaction records should be retained |
| F9 Provider Reliability | **mid** | Downtime directly impacts customer experience |

### 3. Tradeoff Decisions

| Tradeoff | Choice | Driving Force | Why not the other side |
|----------|--------|---------------|----------------------|
| Sync ↔ Async | **Sync** (with streaming) | F4=low | 3s response requirement |
| Single ↔ Multi-Agent | **Single** + routing | F7=high | Multi-agent overhead too expensive at scale |
| RAG ↔ Fine-Tuning | **RAG** | — | FAQ content updates frequently |
| Fail-fast ↔ Degradation | **Degradation** | F9=mid | Must keep serving customers |
| Structured ↔ Free-form Output | **Hybrid** | F5=low | Internal structured, user-facing free-form |

### 4. Selected Patterns

| # | Pattern | Reason (driving force) |
|---|---------|----------------------|
| 37 | Semantic Gateway & Cost-Aware Router | [F7]=high: route easy queries to cheaper models |
| 38 | Semantic Result Cache | [F7]=high: reuse FAQ answers for similar queries |
| 56 | Adaptive Effort | [F7]=high: scale compute to difficulty |
| 40 | Fallback & Graceful Degradation | [F9]=mid: keep serving during outages |
| 13 | NL Boundary Adapter | [F5]=low: structure untrusted user input |
| 42 | Data Boundary Firewall | [F5]=low: inspect/mask PII |
| 29 | Guardrail Sidecar + Self-Correction | [F5]=low: validate outputs |
| 7 | Streaming Progress | [F4]=low: stream partial responses for perceived speed |

### 5. Dial Settings

| Dial | Initial Value | Driving Force | Adjustment Policy |
|------|--------------|---------------|-------------------|
| Timeout | sync 5s | F4=low | Hard limit; affects user experience |
| Model tier threshold | confidence ≥ 0.85 → small model | F7=high | Monitor quality metrics per tier |
| Cache similarity threshold | 0.93 | F7=high | Prioritize hit rate; check answer quality weekly |
| Guardrail strictness | mid–high | F5=low | Balance false positive rate with safety |
| Trace sampling rate | 5% | F7=high, F8=mid | Cost-aware sampling |
| Retrieval top-k | 5 | F4=low | Speed-first; fewer chunks for faster response |

### 6. Composite Architecture

**Base**: [Cost-First](docs/reference-architectures/05-cost-first.md) + [Untrusted-Input](docs/reference-architectures/03-untrusted-input.md)

```
User → NL Boundary (#13) → Guardrail (#29) → Semantic Gateway (#37)
                                                 ├→ Cache hit (#38) → Response
                                                 ├→ Small model (easy) → Response
                                                 └→ Large model (hard) → Response
                                               Data Firewall (#42) on input/output
                                               Streaming (#7) for all responses
                                               Fallback (#40) on provider failure
```

### 7. Risks and Mitigations

| Risk | Related Anti-Pattern | Mitigation |
|------|---------------------|------------|
| Cache serving outdated FAQ answers | — | TTL + invalidation on FAQ content update |
| Model routing misclassifying hard queries | ap-03 (Strongest Model Only) | Monitor per-tier quality; tune threshold |
| Guardrail blocking legitimate queries | ap-02 (Excessive Guardrails) | Track false positive rate; tune quarterly |

### 8. Alternatives

| Alternative | Advantages | Why Not Chosen |
|-------------|-----------|----------------|
| Single large model for all queries | Simpler, higher quality | F7=high: cost prohibitive at 100K/month |
| Async processing | Handles complex queries better | F4=low: 3s requirement makes async impractical |

### 9. Unresolved Questions

- [ ] Re-evaluate if F2 rises to high (adding automated return processing) → add Agent Saga #4, Human Approval #31
- [ ] Re-evaluate if F8 rises to high (regulatory compliance) → 100% tracing, add Policy-as-Code #30
