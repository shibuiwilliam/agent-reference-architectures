# X. デプロイ・ベンダー抽象化・移行


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F9]` プロバイダ信頼度、`[F8]` 説明責任、`[F2]` 失敗コスト
    - **主な二者択一**: ビルド↔バイ、単一↔マルチプロバイダ → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

特定SDK/モデルへのロックインを避け、既存システムへ漸進導入する。

- [#45 Agent Runtime Abstraction｜ランタイム抽象化](45-agent-runtime-abstraction.md) — 実行基盤を差替可能に
- [#46 Model Behavior Compatibility Layer｜互換レイヤー](46-model-behavior-compatibility-layer.md) — モデル差を吸収する互換層
- [#47 Agent Capability Registry｜能力レジストリ](47-agent-capability-registry.md) — 能力・権限・コストを台帳管理
- [#48 Strangler Fig｜段階的置換](48-strangler-fig.md) — 既存処理を段階的に置換
