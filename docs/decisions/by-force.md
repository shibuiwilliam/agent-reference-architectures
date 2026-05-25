---
title: フォース別逆引き
---

# フォース別逆引き

!!! abstract "一言"
    フォース（駆動変数）から、関連する二者択一・ダイヤル・パターンを逆引きする。

## 使い方

「失敗コストが高いのだが、どのパターンを検討すればよいか」——そんなときに便利なのがこの逆引きである。自システムの [フォース評価](../foundations/forces.md) で「高」と判定した変数を起点に、関連する意思決定とパターンを引くことができる。「高い」ときに**特に注意すべき**ものと、「低い」ときに**緩和できる**ものの両面を示している。

---

## `[F1]` 可逆性 — 失敗をやり直せるか

| 種別 | 項目 | F1が**低い**（不可逆）とき |
|------|------|--------------------------|
| 二者択一 | 同期↔非同期 | 非同期＋チェックポイントで巻き戻し可能にする |
| 二者択一 | Plan↔ReAct | Plan先行で副作用前に承認を取る |
| ダイヤル | チェックポイント頻度 | 毎ステップに上げる |
| ダイヤル | 自律性レベル | 低く設定し人間承認を挟む |
| パターン | [#4 Agent Saga](../patterns/01-execution/04-agent-saga.md) | 補償トランザクションで巻き戻す |
| パターン | [#19 Dry-Run First](../patterns/04-tools-mcp/19-dry-run-first-tool-execution.md) | 模擬実行で確認してから実行 |
| パターン | [#31 Human Approval](../patterns/06-reliability/31-human-approval-checkpoint.md) | 高リスク操作前に人間承認 |

---

## `[F2]` 失敗コスト — 金銭/法務/安全の痛み

| 種別 | 項目 | F2が**高い**（失敗が高コスト）とき |
|------|------|---------------------------------|
| 二者択一 | Plan↔ReAct | Plan先行（事前に全体を検討） |
| 二者択一 | インライン↔事後検証 | インライン検証（出荷前に止める） |
| 二者択一 | 同一↔別モデル検証 | 別モデル（同一モデルの盲点を補う） |
| ダイヤル | Best-of-N | 3–5に引き上げ |
| ダイヤル | ガードレール厳しさ | 高めに設定 |
| ダイヤル | HITL頻度 | 高リスク操作は全件承認 |
| パターン | [#8 Planner-Executor-Reviewer](../patterns/02-composition/08-planner-executor-reviewer.md) | 計画・実行・検証の分離 |
| パターン | [#10 Agent Ensemble](../patterns/02-composition/10-agent-ensemble-debate.md) | 合議で頑健化 |
| パターン | [#28 Verifier Agent](../patterns/06-reliability/28-verifier-agent-critic.md) | 独立した検証 |
| パターン | [#57 Autonomy Ladder](../patterns/06-reliability/57-autonomy-ladder.md) | 段階的に自律性を昇格 |

---

## `[F3]` 1リクエストの価値 — 売上/意思決定への寄与

| 種別 | 項目 | F3が**高い**（高価値リクエスト）とき |
|------|------|----------------------------------|
| ダイヤル | Best-of-N | 3–5に引き上げ（コスト許容） |
| ダイヤル | 予算上限 | リクエスト価値に見合う水準まで引き上げ |
| ダイヤル | モデル階層 | 大モデル優先 |
| 二者択一 | Fail-fast↔縮退 | 縮退運転（価値の高いリクエストを落とさない） |
| パターン | [#10 Agent Ensemble](../patterns/02-composition/10-agent-ensemble-debate.md) | 合議で品質向上 |
| パターン | [#37 Semantic Gateway](../patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) | 価値に応じてモデル選択 |

---

## `[F4]` レイテンシ予算 — ユーザーの待機耐性

| 種別 | 項目 | F4が**短い**（即応を期待）とき |
|------|------|------------------------------|
| 二者択一 | 同期↔非同期 | 同期（または [#58 Sync Facade](../patterns/01-execution/58-sync-facade-over-async-core.md)） |
| 二者択一 | インライン↔事後検証 | 事後検証（レイテンシ優先） |
| ダイヤル | 自己修正ループ回数 | 0–1回（時間制約） |
| ダイヤル | 検索 top-k | 少なめ（検索時間削減） |
| パターン | [#7 Streaming Progress](../patterns/01-execution/07-streaming-progress.md) | 待機中に進捗表示 |
| パターン | [#38 Semantic Result Cache](../patterns/08-cost-scaling/38-semantic-result-cache.md) | キャッシュでレイテンシ削減 |
| パターン | [#39 Prompt Cache](../patterns/08-cost-scaling/39-prompt-cache-optimized-context.md) | prefix共有で高速化 |

---

## `[F5]` 入力の信頼度 — 攻撃/汚染の混入可能性

| 種別 | 項目 | F5が**低い**（信頼できない入力）とき |
|------|------|----------------------------------|
| ダイヤル | ガードレール厳しさ | 高めに設定 |
| ダイヤル | 露出ツール数 | 最小限に絞る |
| パターン | [#13 NL Boundary Adapter](../patterns/03-io-contract/13-natural-language-boundary-adapter.md) | 入力の構造化 |
| パターン | [#42 Data Boundary Firewall](../patterns/09-security/42-data-boundary-firewall.md) | PII/インジェクション検査 |
| パターン | [#43 Confused-Deputy](../patterns/09-security/43-confused-deputy-damage-limitation.md) | 被害半径の制限 |
| パターン | [#44 Dual-LLM](../patterns/09-security/44-dual-llm-privilege-separation.md) | 隔離LLMと特権LLMの分離 |
| パターン | [#18 Least-Privilege](../patterns/04-tools-mcp/18-least-privilege-tool-binding.md) | 最小権限 |

---

## `[F6]` タスクの変動性 — 定型↔探索

| 種別 | 項目 | F6が**高い**（探索的）とき |
|------|------|--------------------------|
| 二者択一 | ワークフロー↔エージェント | エージェント（自律的探索） |
| 二者択一 | シングル↔マルチエージェント | 専門性が分離できるならマルチ |
| ダイヤル | 温度 | 0.5–0.8（多様性重視） |
| パターン | [#59 Spectrum Selector](../patterns/01-execution/59-workflow-agent-spectrum-selector.md) | サブタスク毎に判定 |
| パターン | [#12 Blackboard](../patterns/02-composition/12-blackboard.md) | 疎結合な協調 |

F6が**低い**（定型）とき → ワークフロー、[#3 Workflow Backbone](../patterns/01-execution/03-workflow-backbone-agent-node.md)、[#11 Deterministic Core](../patterns/02-composition/11-deterministic-core-probabilistic-edge.md) を優先。

---

## `[F7]` コスト感度・スケール — QPS・月間コスト上限

| 種別 | 項目 | F7が**高い**（厳しいコスト制約）とき |
|------|------|----------------------------------|
| 二者択一 | 単一↔マルチプロバイダ | コスト比較でマルチ |
| ダイヤル | モデル階層閾値 | 上げて小モデル利用を増やす |
| ダイヤル | キャッシュ類似度閾値 | やや緩めてヒット率向上 |
| ダイヤル | トレースサンプリング率 | 1–5%に抑制 |
| パターン | [#37 Semantic Gateway](../patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) | 難易度別ルーティング |
| パターン | [#38 Semantic Result Cache](../patterns/08-cost-scaling/38-semantic-result-cache.md) | 結果再利用 |
| パターン | [#56 Adaptive Effort](../patterns/08-cost-scaling/56-adaptive-effort.md) | 計算量の動的調整 |
| パターン | [#5 Time-Budgeted](../patterns/01-execution/05-time-budgeted-agent-loop.md) | 予算上限 |

---

## `[F8]` 説明責任・規制 — 監査・コンプラ要件

| 種別 | 項目 | F8が**高い**（規制業種）とき |
|------|------|----------------------------|
| ダイヤル | トレースサンプリング率 | 100%（全件記録） |
| ダイヤル | ログ保持期間 | 1–7年（規制準拠） |
| ダイヤル | プロンプト保存粒度 | 全バージョンをGit管理 |
| 二者択一 | プロンプト↔コード制御 | コード制御（テスト・監査可能） |
| 二者択一 | 構造化↔自由出力 | 構造化（監査しやすい） |
| パターン | [#32 Agent Trace](../patterns/07-observability/32-agent-trace.md) | 完全な監査証跡 |
| パターン | [#30 Policy-as-Code](../patterns/06-reliability/30-policy-as-code-guardrail.md) | 制約のコード化 |
| パターン | [#33 Version Pinning](../patterns/07-observability/33-version-pinning.md) | 再現可能性 |
| パターン | [#52 Agent Constitution](../patterns/12-governance/52-agent-constitution.md) | 行動原則の体系化 |

---

## `[F9]` プロバイダ信頼度 — 外部LLMの可用性

| 種別 | 項目 | F9が**低い**（可用性に懸念）とき |
|------|------|-------------------------------|
| 二者択一 | 単一↔マルチプロバイダ | マルチプロバイダ |
| 二者択一 | Fail-fast↔縮退 | 縮退運転 |
| ダイヤル | リトライ回数 | 2–3回 + 指数バックオフ |
| パターン | [#40 Fallback](../patterns/08-cost-scaling/40-fallback-graceful-degradation.md) | 段階縮退 |
| パターン | [#45 Runtime Abstraction](../patterns/10-deployment/45-agent-runtime-abstraction.md) | プロバイダ差し替え |
| パターン | [#46 Compatibility Layer](../patterns/10-deployment/46-model-behavior-compatibility-layer.md) | モデル差吸収 |

---

## 関連ページ

- [駆動変数（フォース）F1–F9](../foundations/forces.md) — フォースの定義
- [意思決定の進め方](decision-flow.md) — フォース評価から始まるワークフロー
- [通し例](worked-examples.md) — フォース評価の具体例
