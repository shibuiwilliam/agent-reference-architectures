# D. メモリ・コンテキスト

このドメインのパターン一覧です（frontmatter から自動生成）。

| ID | パターン | forces | driving_variables | status |
|---|---|---|---|---|
| D1 | [Tiered Memory｜階層化メモリ](d1-tiered-memory.md) | `[F4, F6]` | `[failure_cost]` | stable |
| D2 | [Context Budget Allocator｜コンテキスト予算配分](d2-context-budget-allocator.md) | `[F6, F11]` | `[cost_sensitivity]` | stable |
| D3 | [Memory Write Gate / Quarantine｜メモリ書込ゲート](d3-memory-write-gate.md) | `[F6, F4, F14]` | `[input_trust, failure_cost]` | stable |
| D4 | [Memory Decay & Versioned Truth｜記憶の減衰とバージョン管理](d4-memory-decay-versioned-truth.md) | `[F6]` | `[failure_cost]` | stable |
| D5 | [Prompt Registry / Prompt Artifact｜プロンプトの成果物化](d5-prompt-registry.md) | `[F9, F16]` | `[accountability]` | stable |
| D6 | [Semantic Cache with No-Cache Zones｜禁止領域付きキャッシュ](d6-semantic-cache-nocache-zones.md) | `[F2, F11]` | `[cost_sensitivity, failure_cost]` | stable |
