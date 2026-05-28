# VII. 観測性・監査・評価


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F8]` 説明責任、`[F7]` コスト感度、`[F9]` プロバイダ信頼度
    - **主なダイヤル**: トレースサンプリング率、ログ保持期間、プロンプト保存粒度 → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

エージェントが本番で誤った回答を返したとき、「なぜそうなったのか」を追えなければ改善は手探りになります。モデルを更新したら品質が下がった、という事態にも気づけません。非決定論的な挙動を観測・再現・回帰検知できるようにし、デプロイに伴う挙動変更を規律立てて管理するためのパターン群です。

- [#32 Agent Trace｜エージェントトレース](32-agent-trace.md) — 全ステップを追記専用ログとして記録し、再生可能にする
- [#54 Tiered (Hot/Cold) Observability｜二層観測](54-tiered-observability.md) — 観測データを高速層と安価層に分けて管理する
- [#33 Prompt/Model/Tool Version Pinning｜バージョン固定](33-version-pinning.md) — プロンプト・モデル・ツールのバージョンを固定する
- [#34 Evaluation CI/CD｜評価CI/CD](34-evaluation-ci-cd.md) — 変更のたびに自動評価を実行して回帰を検知する
- [#35 Production Replay｜本番リプレイ](35-production-replay.md) — 本番ログを再生して新旧バージョンの差分を比較する
- [#36 Shadow / Canary Deployment｜シャドー／カナリア](36-shadow-canary-deployment.md) — 段階的に投入し、問題があれば自動ロールバックする
