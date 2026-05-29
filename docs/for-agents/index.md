# コーディングエージェント向けガイド

このドキュメントは、**あなた（コーディングエージェント）が AIエージェントを含むソフトウェアを設計し、人間に提案する**ために最適化されています。ここを最初に読んでください。

## このドキュメントの構造を一言で

設計判断を5層で扱います（詳細は [5層モデル](../concepts/layer-model.md)）。

```
L0 設計力学(F1–F17)  なぜ普通の設計が通用しないか
L1 予算(7種)         何をどれだけ使えるか
L2 駆動変数(9種)     目盛り・二択を何が決めるか   ← あなたが最初に埋める表
L3 程度(degrees)     各設計変数のちょうど
L4 相反(forks)       排他的な仕組みのどちら
L5 パターン(A–G)     実装する部品（frontmatter付き）
```

## どこから情報を取るか（機械可読アクセス）

- **リポジトリ直読（推奨）**：`docs/**/*.md` を直接読みます。各パターンは frontmatter
  （`id / forces / driving_variables / forks / related_patterns / alternatives`）を持っているので、
  まず [機械可読インデックス](../reference/pattern-index.md) で候補を絞り、必要な `.md` を開いてください。
- **公開サイト経由**：`/, llms.txt`（索引）、`/llms-full.txt`（全文連結）、各ページの `.md` URL から取得できます。
  サイトは `mkdocs-llmstxt` がこれらを自動生成しています。

## 統制語彙（提案やメタ抽出で使う固定キー）

- 設計力学：`F1`–`F17`（[定義](../concepts/design-forces.md)）
- 駆動変数：`reversibility` / `failure_cost` / `request_value` / `latency_budget` /
  `input_trust` / `task_variability` / `cost_sensitivity` / `accountability` / `provider_trust`
  （[定義](../concepts/driving-variables.md)）
- 相反ID：`F-1`–`F-18`（[定義](../forks/index.md)）

## あなたがやること（要約）

1. [設計提案プロトコル](decision-protocol.md) に従ってください。
2. **目盛りをハードコードしないでください。** 値は必ず駆動変数から導き、「なぜその値か」を添えてください。
3. **単独で結論を出さないでください。** 人間に選択肢・トレードオフ・推奨と根拠を提示し、選んでもらいます。
4. 不可逆・高失敗コスト・低入力信頼の箇所は、安全側のパターン（[E1](../patterns/e-safety-hitl/e1-risk-based-approval.md) /
   [C1](../patterns/c-tools-security/c1-tool-gateway-mcp-broker.md) /
   [C3](../patterns/c-tools-security/c3-dry-run-commit.md)）を必ず併置提案してください。

## やってはいけないこと

- このドキュメントに無い駆動変数名・force名を勝手に作らないでください。
- 「とりあえずマルチエージェント」「とりあえず自律ループ」のような既定への安易な振り切りは避けてください
  （[アンチパターン](../antipatterns/index.md) 参照）。
- 観測（[G1](../patterns/g-observability-ops/g1-tiered-observability.md)）と予算上限
  （[A7](../patterns/a-execution/a7-deadline-budget-cascade.md)）の無い自律実行は提案しないでください。
