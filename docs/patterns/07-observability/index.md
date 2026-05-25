# VII. 観測性・監査・評価


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F8]` 説明責任、`[F7]` コスト感度、`[F9]` プロバイダ信頼度
    - **主なダイヤル**: トレースサンプリング率、ログ保持期間、プロンプト保存粒度 → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

非決定論を観測・再現・回帰検知可能にし、デプロイ＝挙動変更を規律化する。

- [#32 Agent Trace｜エージェントトレース](32-agent-trace.md) — 全ステップを追記ログ化・再生
- [#54 Tiered (Hot/Cold) Observability｜二層観測](54-tiered-observability.md) — 観測を高速層と安価層に二分
- [#33 Prompt/Model/Tool Version Pinning｜バージョン固定](33-version-pinning.md) — プロンプト/モデル/ツールを固定
- [#34 Evaluation CI/CD｜評価CI/CD](34-evaluation-ci-cd.md) — 変更毎に自動評価で回帰検知
- [#35 Production Replay｜本番リプレイ](35-production-replay.md) — 本番ログを再生し新旧比較
- [#36 Shadow / Canary Deployment｜シャドー／カナリア](36-shadow-canary-deployment.md) — 段階投入と自動ロールバック
