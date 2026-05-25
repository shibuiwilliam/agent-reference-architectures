# X. デプロイ・ベンダー抽象化・移行


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F9]` プロバイダ信頼度、`[F8]` 説明責任、`[F2]` 失敗コスト
    - **主な二者択一**: ビルド↔バイ、単一↔マルチプロバイダ → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

特定のSDKやモデルへのロックインを避け、既存システムへ段階的に導入するためのパターン群である。

- [#45 Agent Runtime Abstraction｜ランタイム抽象化](45-agent-runtime-abstraction.md) — 実行基盤を差し替え可能にする
- [#46 Model Behavior Compatibility Layer｜互換レイヤー](46-model-behavior-compatibility-layer.md) — モデル間の差異を吸収する互換層を設ける
- [#47 Agent Capability Registry｜能力レジストリ](47-agent-capability-registry.md) — 能力・権限・コストを台帳で一元管理する
- [#48 Strangler Fig｜段階的置換](48-strangler-fig.md) — 既存の処理を段階的にエージェントへ置換する
