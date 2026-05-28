---
title: パターン早見表
---

# パターン早見表（59パターン）

<!-- BEGIN:GEN:pattern-index -->
| # | パターン | カテゴリ | 一言 |
|---|---------|---------|------|
| 1 | [Request-to-Job Gateway](glossary.md) | I. 実行 | 1リクエストを非同期ジョブとして受け付ける |
| 2 | [Durable Agent Session](glossary.md) | I. 実行 | 状態を永続化し中断・再開に耐える |
| 3 | [Workflow Backbone + Agent Node](glossary.md) | I. 実行 | 骨格は決定論、判断だけ委譲 |
| 4 | [Agent Saga](glossary.md) | I. 実行 | 副作用連鎖を補償で巻き戻す |
| 5 | [Time-Budgeted Agent Loop](glossary.md) | I. 実行 | 時間・回数・コストを予算化し暴走を止める |
| 6 | [Interruptible Agent](glossary.md) | I. 実行 | 途中で停止・方針修正できる |
| 7 | [Streaming Progress](glossary.md) | I. 実行 | 過程を監査可能な要約で逐次表示 |
| 8 | [Planner-Executor-Reviewer](glossary.md) | II. 構成 | 計画/実行/検証を別ロールに分ける |
| 9 | [Supervisor & Specialist Agents](glossary.md) | II. 構成 | 統括役が専門役へ委譲する |
| 10 | [Agent Ensemble & Debate](glossary.md) | II. 構成 | 複数で解き合議・討論で頑健化 |
| 11 | [Deterministic Core, Probabilistic Edge](glossary.md) | II. 構成 | 中核は決定論、周辺だけAI |
| 12 | [Blackboard](glossary.md) | II. 構成 | 共有黒板で疎結合に協調 |
| 13 | [Natural Language Boundary Adapter](glossary.md) | III. 契約 | 自然言語を構造化意図へ変換 |
| 14 | [Structured Output Contract](glossary.md) | III. 契約 | 出力をスキーマで契約化 |
| 15 | [Inverted Structured Output](glossary.md) | III. 契約 | 最終実行でなく中間判断を出させる |
| 16 | [Ambiguity Negotiation](glossary.md) | III. 契約 | 曖昧なら確認してから実行 |
| 17 | [Tool / MCP Gateway](glossary.md) | IV. ツール | ツール接続を集約し認可・監査 |
| 18 | [Least-Privilege Tool Binding](glossary.md) | IV. ツール | セッション毎に最小権限を束縛 |
| 19 | [Dry-Run First Tool Execution](glossary.md) | IV. ツール | 副作用はまず模擬実行→承認 |
| 20 | [Sandboxed Tool Runtime](glossary.md) | IV. ツール | コード/操作を隔離環境で実行 |
| 21 | [MCP Adapter Isolation](glossary.md) | IV. ツール | MCPを信頼境界ごとに分離 |
| 22 | [Anti-Corruption Layer](glossary.md) | IV. ツール | レガシーとの概念汚染を防ぐ翻訳層 |
| 23 | [Layered Memory](glossary.md) | V. メモリ | 短期/長期/共有に記憶を階層化 |
| 24 | [Context Pack / Assembly](glossary.md) | V. メモリ | 文脈を組み立てグラウンディング |
| 25 | [Memory Write Gate](glossary.md) | V. メモリ | 長期保存を承認制にする |
| 26 | [Forgetting and Expiration](glossary.md) | V. メモリ | 記憶に失効・鮮度を持たせる |
| 27 | [Evidence-First Answer](glossary.md) | VI. 信頼性 | 回答前に根拠を取得・引用 |
| 28 | [Verifier Agent / Critic](glossary.md) | VI. 信頼性 | 独立した検証器で出荷前検査 |
| 29 | [Guardrail Sidecar + Self-Correction](glossary.md) | VI. 信頼性 | 入出力検査し誤りを自己修正 |
| 30 | [Policy-as-Code Guardrail](glossary.md) | VI. 信頼性 | 制約をコード化し別途判定 |
| 31 | [Human Approval Checkpoint](glossary.md) | VI. 信頼性 | 高リスク前に人間承認 |
| 32 | [Agent Trace](glossary.md) | VII. 観測 | 全ステップを追記ログ化・再生 |
| 33 | [Prompt/Model/Tool Version Pinning](glossary.md) | VII. 観測 | プロンプト/モデル/ツールを固定 |
| 34 | [Evaluation CI/CD](glossary.md) | VII. 観測 | 変更毎に自動評価で回帰検知 |
| 35 | [Production Replay](glossary.md) | VII. 観測 | 本番ログを再生し新旧比較 |
| 36 | [Shadow / Canary Deployment](glossary.md) | VII. 観測 | 段階投入と自動ロールバック |
| 37 | [Semantic Gateway & Cost-Aware Router](glossary.md) | VIII. コスト | 難易度でモデルを動的選択 |
| 38 | [Semantic Result Cache](glossary.md) | VIII. コスト | 意味的に近い結果を再利用 |
| 39 | [Prompt Cache Optimized Context](glossary.md) | VIII. コスト | 共通prefixでキャッシュを効かせる |
| 40 | [Fallback & Graceful Degradation](glossary.md) | VIII. コスト | 障害時に段階縮退で継続 |
| 41 | [Tenant-Isolated Agent Runtime](glossary.md) | IX. セキュリティ | テナント毎に実行・記憶を分離 |
| 42 | [Data Boundary Firewall](glossary.md) | IX. セキュリティ | 入出力でPII/機密を検査・マスク |
| 43 | [Confused-Deputy Damage Limitation](glossary.md) | IX. セキュリティ | 騙されても被害半径を制限 |
| 44 | [Dual-LLM Privilege Separation](glossary.md) | IX. セキュリティ | 隔離LLMと特権LLMを分離 |
| 45 | [Agent Runtime Abstraction](glossary.md) | X. デプロイ | 実行基盤を差替可能に |
| 46 | [Model Behavior Compatibility Layer](glossary.md) | X. デプロイ | モデル差を吸収する互換層 |
| 47 | [Agent Capability Registry](glossary.md) | X. デプロイ | 能力・権限・コストを台帳管理 |
| 48 | [Strangler Fig](glossary.md) | X. デプロイ | 既存処理を段階的に置換 |
| 49 | [Agent Workbench](glossary.md) | XI. UX | 計画/進捗/承認を一画面管理 |
| 50 | [Editable Plan](glossary.md) | XI. UX | 実行前に計画を人が編集 |
| 51 | [Agent-to-Human Escalation](glossary.md) | XI. UX | 自信/権限不足で人間へ引き継ぎ |
| 52 | [Agent Constitution](glossary.md) | XII. ガバナンス | 行動原則を体系的に展開 |
| 53 | [Agent Change Management](glossary.md) | XII. ガバナンス | 変更を厳格なCI/カナリア対象に |
| 54 | [Tiered (Hot/Cold) Observability](glossary.md) | VII. 観測 | 観測を高速層と安価層に二分 |
| 55 | [Deadline & Budget Cascade](glossary.md) | I. 実行 | 期限・予算を呼出ツリーへ伝播 |
| 56 | [Adaptive Effort](glossary.md) | VIII. コスト | 難易度で投入計算量を増減 |
| 57 | [Autonomy Ladder](glossary.md) | VI. 信頼性 | 実績に応じ自律性を段階的に昇格 |
| 58 | [Sync Facade over Async Core](glossary.md) | I. 実行 | 短ければ同期、超えたら非同期へ昇格 |
| 59 | [Workflow–Agent Spectrum Selector](glossary.md) | I. 実行 | サブタスク毎に決定論↔自律を選定 |
<!-- END:GEN:pattern-index -->
