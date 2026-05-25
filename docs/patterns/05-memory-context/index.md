# V. メモリ・コンテキスト管理


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F8]` 説明責任、`[F4]` レイテンシ予算、`[F7]` コスト感度
    - **主なダイヤル**: メモリ TTL、メモリ書き込み積極度、要約タイミング、検索 top-k → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **主な二者択一**: 文脈内↔外部状態、RAG↔FT↔ロングコンテキスト → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

コンテキストウィンドウの有限性と、エージェント間での状態の受け渡しを扱うカテゴリである。

- [#23 Layered Memory｜階層化メモリ](23-layered-memory.md) — 短期・長期・共有の3層に記憶を分けて管理する
- [#24 Context Pack / Assembly｜コンテキスト組立・RAG](24-context-pack-assembly.md) — 必要な文脈を検索・組み立てて、回答の根拠を確保する
- [#25 Memory Write Gate｜メモリ書き込みゲート](25-memory-write-gate.md) — 長期メモリへの保存を承認制にして記憶の品質を守る
- [#26 Forgetting and Expiration｜忘却・失効](26-forgetting-and-expiration.md) — 記憶に有効期限と鮮度を持たせ、古い情報を適切に忘れる
