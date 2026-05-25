# V. Memory & Context Management


!!! tip "Key decisions for this concern"
    - **Primary Forces**: `[F8]` Accountability, `[F4]` Latency Budget, `[F7]` Cost Sensitivity
    - **Primary Dials**: Memory TTL, Memory Write Eagerness, Summarization Timing, Retrieval top-k → [Tuning Dials](../../decisions/tuning-dials.md)
    - **Primary Tradeoffs**: In-context ↔ External State, RAG ↔ FT ↔ Long Context → [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

During extended chatbot interactions, it is not uncommon for earlier discussion content to be "forgotten," or conversely for token waste on irrelevant information. This category addresses the finite nature of context windows and state passing between agents.

- [#23 Layered Memory](23-layered-memory.md) — Separate memory into short-term, long-term, and shared layers
- [#24 Context Pack / Assembly](24-context-pack-assembly.md) — Retrieve, select, and assemble the necessary context to ground answers
- [#25 Memory Write Gate](25-memory-write-gate.md) — Gate long-term memory writes with approval to protect memory quality
- [#26 Forgetting and Expiration](26-forgetting-and-expiration.md) — Give memories expiration dates and freshness to appropriately forget old information
