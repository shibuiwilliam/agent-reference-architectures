# III. 入出力・契約化


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F5]` 入力の信頼度、`[F8]` 説明責任、`[F2]` 失敗コスト
    - **主な二者択一**: 構造化↔自由出力、LLM推論↔ツール委譲 → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

自然言語と確率的出力を、通常ソフトが安全に扱える「契約」に変換する境界。

- [#13 Natural Language Boundary Adapter｜自然言語境界](13-natural-language-boundary-adapter.md) — 自然言語を構造化意図へ変換
- [#14 Structured Output Contract｜構造化出力契約](14-structured-output-contract.md) — 出力をスキーマで契約化
- [#15 Inverted Structured Output｜反転構造化出力](15-inverted-structured-output.md) — 最終実行でなく中間判断を出させる
- [#16 Ambiguity Negotiation｜曖昧性交渉](16-ambiguity-negotiation.md) — 曖昧なら確認してから実行
