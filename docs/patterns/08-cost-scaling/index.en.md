# VIII. Cost, Performance & Scaling


!!! tip "Key decisions for this concern"
    - **Primary forces**: `[F7]` Cost Sensitivity, `[F3]` Request Value, `[F9]` Provider Reliability
    - **Key dials**: Model tier threshold, Cache similarity threshold, Retry count → [Tuning Dials](../../decisions/tuning-dials.md)
    - **Key tradeoffs**: Single vs. multi-provider, Fail-fast vs. degradation → [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

As agent request volume grows, LLM API costs can exceed expectations. Furthermore, external provider outages or rate limits can suddenly leave you without responses. These patterns treat LLM usage as a resource to be managed and absorb the instability of external LLMs.

- [#37 Semantic Gateway & Cost-Aware Router](37-semantic-gateway-cost-aware-router.md) — Dynamically select models based on difficulty
- [#38 Semantic Result Cache](38-semantic-result-cache.md) — Reuse past results for semantically similar queries
- [#39 Prompt Cache Optimized Context](39-prompt-cache-optimized-context.md) — Leverage common prefixes for cache efficiency
- [#40 Fallback & Graceful Degradation](40-fallback-graceful-degradation.md) — Gradually degrade during failures to maintain service
- [#56 Adaptive Effort](56-adaptive-effort.md) — Scale compute investment up or down based on difficulty
