# V. メモリ・コンテキスト管理


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F8]` 説明責任、`[F4]` レイテンシ予算、`[F7]` コスト感度
    - **主なダイヤル**: メモリ TTL、メモリ書き込み積極度、要約タイミング、検索 top-k → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **主な二者択一**: 文脈内↔外部状態、RAG↔FT↔ロングコンテキスト → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

コンテキスト窓の有限性と、主体を跨ぐ状態受け渡しを扱う。

- [#23 Layered Memory｜階層化メモリ](23-layered-memory.md) — 短期/長期/共有に記憶を階層化
- [#24 Context Pack / Assembly｜コンテキスト組立・RAG](24-context-pack-assembly.md) — 文脈を組み立てグラウンディング
- [#25 Memory Write Gate｜メモリ書き込みゲート](25-memory-write-gate.md) — 長期保存を承認制にする
- [#26 Forgetting and Expiration｜忘却・失効](26-forgetting-and-expiration.md) — 記憶に失効・鮮度を持たせる
