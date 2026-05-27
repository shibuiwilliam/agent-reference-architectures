# Example Proposal: Internal Document RAG Chatbot

> Source: `docs/decisions/worked-examples.md` Example 1
> This demonstrates the `_agent/proposal-template.md` format.

## Architecture Proposal

**Catalog Version**: v1.1.0
**Target System**: Internal document RAG chatbot

### 1. Requirements Summary

Internal chatbot that searches company documents (Confluence/Notion) and answers employee questions. Approximately 500 internal users, several thousand queries per month. Read-only — no side effects.

### 2. Force Evaluation

| Force | Rating | Rationale |
|-------|--------|-----------|
| F1 Reversibility | **high** | Read-only. No side effects |
| F2 Failure Cost | **low** | Wrong answers are inconvenient but not critical |
| F3 Request Value | **low** | High volume of lightweight questions |
| F4 Latency Budget | **mid** | Want responses in 5–10 seconds |
| F5 Input Trust | **high** | Internal users only |
| F6 Task Variability | **low** | Search + summarize is a fixed pattern |
| F7 Cost Sensitivity | **mid** | Monthly budget exists |
| F8 Accountability | **low** | Internal tool |
| F9 Provider Reliability | **mid** | Single provider to start |

### 3. Tradeoff Decisions

| Tradeoff | Choice | Driving Force | Why not the other side |
|----------|--------|---------------|----------------------|
| Sync ↔ Async | **Sync** (Sync Facade, async fallback) | F4=mid | Most queries complete within 8s |
| Workflow ↔ Agent | **Workflow** | F6=low | Fixed search+summarize pattern |
| RAG ↔ Fine-Tuning | **RAG** | — | Document update frequency is high |
| Single ↔ Multi-Provider | **Single** | F9=mid | No issues yet |
| Inline ↔ Post-hoc Verification | **Post-hoc** | F2=low | Low risk doesn't justify inline cost |

### 4. Selected Patterns

| # | Pattern | Reason (driving force) |
|---|---------|----------------------|
| 58 | Sync Facade over Async Core | [F4]=mid: sync for fast queries, async fallback for slow ones |
| 24 | Context Pack / Assembly | Core RAG pattern for document grounding |
| 14 | Structured Output Contract | Ensure consistent response format |
| 38 | Semantic Result Cache | [F7]=mid: reuse similar query results to reduce cost |
| 32 | Agent Trace | Minimum observability for debugging |

### 5. Dial Settings

| Dial | Initial Value | Driving Force | Adjustment Policy |
|------|--------------|---------------|-------------------|
| Timeout | sync 8s / async 2min | F4=mid | Monitor P95; lower if users complain |
| Retrieval top-k | 10 | — | Balance precision vs latency |
| Cache similarity threshold | 0.95 | F7=mid | Lower to increase hit rate if quality holds |
| Trace sampling rate | 10% | F8=low | Increase if debugging specific issues |

### 6. Composite Architecture

**Base**: [MVP](docs/reference-architectures/01-mvp.md) + cache layer

```
User → Sync Facade (#58) → Context Pack/RAG (#24) → LLM → Structured Output (#14) → User
                                                          ↓
                                                   Result Cache (#38)
                                                          ↓
                                                   Agent Trace (#32, sampled)
```

### 7. Risks and Mitigations

| Risk | Related Anti-Pattern | Mitigation |
|------|---------------------|------------|
| Cache serving stale answers | — | TTL on cache entries; invalidate on document update |
| RAG retrieving irrelevant documents | ap-05 (Context Stuffing) | Tune top-k and similarity threshold |

### 8. Alternatives

| Alternative | Advantages | Why Not Chosen |
|-------------|-----------|----------------|
| Full async (#1 Request-to-Job) | Handles long queries better | F4=mid: most queries are fast enough for sync |
| Fine-tuning instead of RAG | Lower latency | Documents change frequently; RAG is more flexible |

### 9. Unresolved Questions

- [ ] Re-evaluate if F7 rises to high (QPS 10x increase) → add model routing #37
- [ ] Re-evaluate if F8 rises to high (audit requirements added) → 100% tracing, add Version Pinning #33
