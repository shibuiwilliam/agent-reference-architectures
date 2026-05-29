# 設計提案プロトコル（コーディングエージェント用）

AIエージェントを含むアーキテクチャを設計し、人間に提案するときは**この手順を順番に踏んでください**。最終出力は末尾の「提案テンプレート」の形に揃えてください。

## ステップ0：対象の言語化

「どのユースケースの、どの処理に、AIエージェントをどう組み込むか」を1〜2文で明確にしてください。曖昧な場合は**人間に1問だけ**質問してください（複数同時に聞かないでください）。

## ステップ1：駆動変数を埋める（L2）

[9つの駆動変数](../concepts/driving-variables.md) を当該ユースケースについて高/中/低で評価してください。不明な変数があれば、**最も結論を左右する1つだけ**人間に確認します。

| 駆動変数 | 評価(高/中/低) | 根拠 |
|---|---|---|
| reversibility（可逆性） | | |
| failure_cost（失敗コスト） | | |
| request_value（1リクエストの価値） | | |
| latency_budget（レイテンシ予算） | | |
| input_trust（入力の信頼度） | | |
| task_variability（タスクの変動性） | | |
| cost_sensitivity（コスト感度・スケール） | | |
| accountability（説明責任・規制） | | |
| provider_trust（プロバイダ信頼度） | | |

## ステップ2：7つの予算を設定（L1）

[7つの予算](../concepts/budgets.md) に具体値（または範囲）と**枯渇時の挙動**を割り当ててください。最低でも時間・コスト・自律性・リスク・観測は明示します。

## ステップ3：候補パターンを出す（L3–L5）

[意思決定フロー](../decision/decision-flow.md) を上から辿り、候補パターンを列挙します。各分岐で**効いた駆動変数を記録**してください。並行して [機械可読インデックス](../reference/pattern-index.md) で、当該駆動変数に紐づくパターンを拾います。

## ステップ4：採否を判定する

候補ごとに、そのパターンの `.md` の **「選定条件（When to use / When NOT）」** を読み、採用/不採用を決めてください。不採用の場合は frontmatter の `alternatives` に倒します。

## ステップ5：相反を解き、目盛りを決める

- 関係する [相反（forks）](../forks/index.md) について、駆動変数に基づいてどちら側に倒すかを決めてください（デフォルト/ハイブリッドも検討します）。
- 採用パターンが持つ [程度（degrees）](../degrees/index.md) の目盛りを、**駆動変数の関数として**値付けしてください。**固定の定数で書かないでください。**

## ステップ6：安全網を必ず併置する

以下は条件に当たれば**自動的に併置提案**してください（人間が外す判断はできますが、あなたから落とさないでください）。

- 不可逆 or 高 failure_cost → [E1 リスクベース承認](../patterns/e-safety-hitl/e1-risk-based-approval.md) ＋ [C3 ドライラン](../patterns/c-tools-security/c3-dry-run-commit.md)
- 副作用ツール/MCP → [C1 ツールゲートウェイ](../patterns/c-tools-security/c1-tool-gateway-mcp-broker.md) ＋ [C4 冪等](../patterns/c-tools-security/c4-idempotent-command-envelope.md)
- 低 input_trust → [C6 Confused Deputy防御](../patterns/c-tools-security/c6-confused-deputy-defense.md) ＋ [C7 サンドボックス](../patterns/c-tools-security/c7-sandboxed-execution.md) ＋ [E2 Policy-as-Code](../patterns/e-safety-hitl/e2-policy-as-code.md)
- 自律ループ → [A7 予算カスケード](../patterns/a-execution/a7-deadline-budget-cascade.md)（予算上限）
- 常時 → [G1 二層観測](../patterns/g-observability-ops/g1-tiered-observability.md) ＋ [G2 トレース](../patterns/g-observability-ops/g2-end-to-end-tracing.md)

## ステップ7：提案を出力する

下のテンプレートで人間に提示してください。**結論を押し付けず、推奨＋根拠＋代替＋未確認事項**を必ず含めてください。

---

### 提案テンプレート

```markdown
## アーキテクチャ提案：<ユースケース名>

### 1. 前提（駆動変数）
<9変数の評価表。中核となった2–3変数を太字>

### 2. 予算
<7予算の値と枯渇時挙動>

### 3. 採用パターン（と却下したもの）
| パターン | 採否 | 理由（効いた駆動変数） |
|---|---|---|
| B1 決定論的な殻 | 採用 | task_variability=低, accountability=高 |
| B3 自律ループ | 却下 | 経路が列挙可能なため（→ B2 に倒す） |

### 4. 解いた相反（forks）
| フォーク | 採った側 | 根拠 |
|---|---|---|
| F-1 同期/非同期 | 非同期 | latency_budget=寛容, reversibility=低 |

### 5. 目盛り（程度）と根拠
| 目盛り | 値 | なぜこの値か（駆動変数） |
|---|---|---|
| タイムアウト(LLM) | 90s | p99×1.5, latency_budget=寛容 |
| 承認頻度 | 不可逆操作のみ事前承認 | failure_cost=高 |

### 6. 構成図
（mermaid）

### 7. 併置した安全網
- G1 二層観測 / G2 トレース / E1 承認 / C1 ゲートウェイ …

### 8. 人間に確認したいこと（未確定の駆動変数・前提）
- …
```

## 不変条件（このプロトコルの約束）

1. **目盛りは関数です**：値の隣には必ず駆動変数を記載してください。定数のハードコードは避けてください。
2. **根拠を残してください**：各分岐・各目盛りに「効いた駆動変数」を明記してください。
3. **人間に選んでもらってください**：単独で確定せず、推奨＋代替＋トレードオフを提示してください。
4. **安全側をデフォルトにしてください**：迷ったら自律度を下げ、観測・予算・承認を足してください。
