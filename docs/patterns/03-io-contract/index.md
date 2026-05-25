# III. 入出力・契約化


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F5]` 入力の信頼度、`[F8]` 説明責任、`[F2]` 失敗コスト
    - **主な二者択一**: 構造化↔自由出力、LLM推論↔ツール委譲 → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

LLMの入力はあいまいな自然言語であり、出力は毎回微妙に異なる確率的なテキストである。これらを既存のソフトウェアが安全に受け渡しできる「契約」に変換する境界を担うパターン群である。

- [#13 Natural Language Boundary Adapter｜自然言語境界](13-natural-language-boundary-adapter.md) — 自然言語を構造化された意図表現へ変換する
- [#14 Structured Output Contract｜構造化出力契約](14-structured-output-contract.md) — LLMの出力をスキーマで契約化する
- [#15 Inverted Structured Output｜反転構造化出力](15-inverted-structured-output.md) — 最終実行ではなく中間の判断を構造化出力させる
- [#16 Ambiguity Negotiation｜曖昧性交渉](16-ambiguity-negotiation.md) — 入力が曖昧なら確認してから実行する
