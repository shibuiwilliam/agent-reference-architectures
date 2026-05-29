---
id: G4
slug: g4-eval-harness
title: "Eval Harness｜評価ハーネス"
domain: g-observability-ops
status: stable
layer: L5-pattern
summary: "ゴールデンデータセットと自動評価関数でエージェントの品質を定量測定し、変更の回帰を検知する。"
forces: [F3, F4, F9]
driving_variables: [accountability, cost_sensitivity]
forks: []
related_patterns: [D5, E3, G1, G3, F2]
alternatives: []
tags: [observability, eval, testing, regression, quality, harness]
---

# Eval Harness｜評価ハーネス

## 一言で（TL;DR）

ゴールデンデータセット（入力と期待出力のペア）と自動評価関数（完全一致・LLM-as-Judge・カスタムメトリクス）を組み合わせた評価パイプラインを構築し、プロンプト・モデル・コードの変更ごとにCIで回帰検知を行う。評価はオフライン（デプロイ前バッチ）、オンライン（本番サンプリング）、シャドウ（A/B比較）の3層で実施し、精度・レイテンシ・コスト・安全性をカテゴリ別に追跡する。

## 解決する問題

AIエージェントは[確率的（F3）](../../concepts/design-forces.md)であるため、コードの単体テストのように「全入力に対して正解が決定論的に定まる」前提が成り立たない。従来のassertベースのテストだけでは品質の変化を捕捉できず、リリース後に品質劣化が判明するまでの時間が長くなる。

[ハルシネーション（F4）](../../concepts/design-forces.md)は個別入力への目視確認では検出しきれない。数百件のゴールデンデータに対して自動評価を回すことで、ハルシネーション率の統計的な変動を検知できる。

[LLMドリフト（F9）](../../concepts/design-forces.md)は、プロバイダ側のモデル更新やAPIの挙動変更によって、自チームが何も変更していなくても品質が変わる現象を指す。評価ハーネスを定期実行することで、外部起因の回帰も検知できる。

評価ハーネスがなければ、品質の変化は本番のユーザークレームや障害として初めて顕在化する。

## 選定条件（When to use / When NOT）

- **使う条件**
    - エージェントが本番トラフィックを処理しており、プロンプト・モデル・コードのいずれかを継続的に変更する開発体制がある。
    - `[accountability]` が中以上で、品質の変化を定量的に示す必要がある（社内レビュー、規制報告、SLA遵守など）。
    - ゴールデンデータを作成・維持できるドメイン知識を持つチームメンバーがいる。
- **使わない条件**
    - プロトタイプ段階でプロンプトが日単位で大幅に変わり、ゴールデンデータの維持コストが評価の価値を上回る → 手動スポット確認で十分。
    - 出力が自由形式のクリエイティブ生成（小説、詩など）で、正解の定義が困難 → LLM-as-Judgeの基準設計に過大な工数がかかるため、ユーザーフィードバックによる定性評価を優先する。
    - LLM呼び出しが補助的で、後段に決定論的な検証ロジックがあり誤りが自動修正される → 検証ロジック自体がテスト対象であり、評価ハーネスの優先度は低い。

## 駆動変数とチューニング（程度）

| 目盛り | 効かなすぎ ⇔ 効きすぎ | 決め方 `[駆動変数]` | 目安（出発点） |
|---|---|---|---|
| ゴールデンデータ件数 | 統計的に有意差を検出できない ⇔ 維持コスト・実行時間が過大 | カテゴリごとに最低30件。`[accountability]` が高い領域ほど件数を増やす `[accountability]` | 全体100〜500件、重要カテゴリ各30件以上 |
| 評価関数のコスト | 安価だが精度が低い（完全一致のみ） ⇔ 高精度だが実行コストが高い（LLM-as-Judge全件） | 安価な関数でフィルタし、不合格のみLLM-as-Judgeに回す。`[cost_sensitivity]` が高いほどサンプリング率を下げる `[cost_sensitivity]` | 完全一致/ルール: 全件、LLM-as-Judge: 10〜30%サンプル |
| 回帰ゲートの閾値 | 緩すぎて品質劣化を見逃す ⇔ 厳しすぎてデプロイが頻繁にブロックされる | `[accountability]` が高いほど閾値を厳しく。ベースラインスコアの95%信頼区間を基準にする `[accountability]` | 精度: ベースライン-2%以内、安全性: 劣化0件 |
| 定期実行頻度 | ドリフト検知が遅れる ⇔ 評価コストが膨らむ | 変更がなくてもモデルドリフト（F9）検知のため定期実行が必要 `[cost_sensitivity]` | CI: 変更ごと、定期: 日次〜週次 |

## 相反における立ち位置（相反）

本パターンは特定のフォークの片側に強く倒れるものではなく、品質ゲートの基盤として他パターンを横断的に支える。

- **F-9（インライン検証 vs 事後検証）**：評価ハーネスは事後検証の仕組みだが、その結果はインライン検証（[E3 ガードレール](../e-safety-hitl/e3-guardrail-sandwich.md)）の閾値チューニングにフィードバックする。ガードレールの偽陽性率・偽陰性率を評価ハーネスで定量測定し、閾値を駆動変数の関数として調整する。
- **F-12（中央モデルレジストリ vs 分散）**：プロンプトとモデルバージョンが[D5 プロンプトレジストリ](../d-memory-context/d5-prompt-registry.md)で管理されている場合、レジストリの変更をトリガーに評価パイプラインを自動実行できる。分散管理の場合は変更検知の仕組みを別途設計する必要がある。

## 構造

```mermaid
flowchart TD
  Trigger[トリガー<br/>PR / モデル更新 / cron] --> Pipeline[評価パイプライン]

  subgraph データ
    Golden[ゴールデンデータセット<br/>input + expected output]
    Replay[本番リプレイデータ<br/>F2 から供給]
  end

  Golden --> Pipeline
  Replay --> Pipeline

  Pipeline --> Exec[エージェント実行<br/>バッチ推論]
  Exec --> EvalFn[評価関数]

  subgraph 評価関数
    direction LR
    EM[完全一致 / ルール]
    LLMJudge[LLM-as-Judge]
    Custom[カスタムメトリクス<br/>安全性・事実性]
  end

  EvalFn --> Scores[スコア集計<br/>精度 / レイテンシ / コスト / 安全性]
  Scores --> Gate{回帰ゲート}
  Gate -->|PASS| Deploy[デプロイ許可]
  Gate -->|FAIL| Block[デプロイ阻止<br/>+ 差分レポート]
  Scores --> Dashboard[G1 メトリクス<br/>トレンド可視化]
```

## 実装メモ

評価データセットの最小構造：

```yaml
# golden_dataset.yml
- id: "order-happy-path-001"
  category: "order_processing"
  input: "注文番号12345のステータスを教えてください"
  context:
    order_id: "12345"
    status: "shipped"
    tracking: "JP1234567890"
  expected:
    contains: ["発送済み", "JP1234567890"]
    not_contains: ["キャンセル", "返金"]
    eval_fn: "factual_accuracy"
```

評価パイプラインの最小実装：

```python
import statistics

def run_eval(agent, dataset, eval_fns, baseline_scores):
    results = []
    for case in dataset:
        output = agent.run(case["input"], context=case.get("context"))
        scores = {}
        for fn_name, fn in eval_fns.items():
            scores[fn_name] = fn(output, case["expected"])
        results.append({"id": case["id"], "category": case["category"], **scores})

    # カテゴリ別集計
    by_category = {}
    for r in results:
        by_category.setdefault(r["category"], []).append(r)

    # 回帰ゲート判定
    for category, items in by_category.items():
        accuracy = statistics.mean([i["factual_accuracy"] for i in items])
        baseline = baseline_scores.get(category, {}).get("factual_accuracy", 0)
        if accuracy < baseline - 0.02:  # 2%劣化で阻止
            raise RegressionError(f"{category}: {accuracy:.3f} < {baseline:.3f} - 0.02")
    return results
```

LLM-as-Judge の評価プロンプト例：

```text
あなたは品質評価者です。以下のエージェント出力を評価してください。

【入力】{input}
【期待される内容】{expected}
【エージェント出力】{output}

以下の基準で1-5のスコアをつけてください：
- 事実の正確性（hallucination がないか）
- 質問への回答の完全性
- 不要な情報の有無

JSON形式で回答: {"accuracy": N, "completeness": N, "conciseness": N, "reasoning": "..."}
```

落とし穴：

- **ゴールデンデータの腐敗**。プロダクトの仕様変更に伴い期待出力が古くなると、正しい出力が「回帰」と判定される。ゴールデンデータにオーナーと最終更新日を付与し、定期的な棚卸しを仕組み化する。
- **LLM-as-Judgeの自己矛盾**。評価用LLMも確率的であるため、同じ入力に対してスコアが揺れる。温度を0に設定し、判定が分かれるケースでは3回実行の多数決を取るなどの安定化策を講じる。ただし評価コストが3倍になるため、`[cost_sensitivity]` とのバランスを取る。
- **過剰な完全一致依存**。自然言語の出力に完全一致テストを多用すると、表現の揺れだけで偽陰性が多発する。キーワード包含、正規表現、意味的類似度など、出力の性質に合った評価関数を選ぶ。
- **ベースラインの固定忘れ**。評価スコアは「前回の安定版」との相対比較が基本。ベースラインを更新するタイミング（デプロイ成功後に自動更新など）を明示的に定めておく。

## 効かせる力学（forces）

- **F3（確率的）**：決定論的テストでは捕捉できない品質のばらつきを、統計的な評価スコアとして定量化する。カテゴリ別のスコアトレンドを追跡することで、特定ドメインでの品質変化を早期に検知する。
- **F4（ハルシネーション）**：事実性評価関数（ゴールデンデータとの照合、LLM-as-Judge による事実チェック）をパイプラインに組み込み、ハルシネーション率の統計的な増減を自動検知する。
- **F9（LLMドリフト）**：CIでの変更時実行に加え、変更がなくても定期実行（日次〜週次）することで、プロバイダ側のモデル更新による品質変動を検知する。スコアの時系列推移を[G1 二層観測](g1-tiered-observability.md)のダッシュボードに統合する。

## 関連・代替

- [D5 プロンプトレジストリ](../d-memory-context/d5-prompt-registry.md)：プロンプトのバージョン管理とCIトリガーの連携先。レジストリへのマージをトリガーに評価パイプラインを自動実行し、スコアが回帰ゲートを通過したバージョンのみ昇格させる。
- [E3 ガードレール](../e-safety-hitl/e3-guardrail-sandwich.md)：ガードレールの偽陽性率・偽陰性率を評価ハーネスで定量測定する。評価結果をもとにガードレールの閾値を調整し、精度と安全性のバランスを取る。
- [G1 二層観測](g1-tiered-observability.md)：本番メトリクス（レイテンシ、コスト、エラー率）と評価スコアを同一ダッシュボードで突合する。評価スコアの劣化と本番メトリクスの異常が同時期に発生していればモデルドリフトの裏付けになる。
- [G3 シャドウ・カナリア](g3-shadow-canary.md)：シャドウテストやカナリアリリースの「合否判定基準」を評価ハーネスのスコアが供給する。G3の昇格ゲートにG4の評価関数を再利用することで、判定基準の一貫性を保つ。
- [F2 イベントソース・リプレイ](../f-data-integrity/f2-event-sourced-replayable.md)：本番のリプレイデータを評価入力として再利用する。ゴールデンデータだけでは網羅できないエッジケースを、実トラフィックから補完する。

## コーディングエージェント向け指示（machine-actionable）

このパターンを人間に提案するなら、同時に以下を提案/確認する：

- [ ] ゴールデンデータセットの初期件数とカテゴリ分類を設計し、`[accountability]` から件数の根拠を添えて提示したか
- [ ] 評価関数の構成（完全一致 / LLM-as-Judge / カスタム）を決め、`[cost_sensitivity]` に応じたサンプリング戦略を提示したか
- [ ] 回帰ゲートの閾値を `[accountability]` から導出し、カテゴリ別に設定したか（安全性カテゴリは劣化0件を推奨）
- [ ] [D5 プロンプトレジストリ](../d-memory-context/d5-prompt-registry.md)との連携を設計し、プロンプト変更時のCI自動実行を含めたか
- [ ] [G1 二層観測](g1-tiered-observability.md)のダッシュボードにスコアトレンドを統合する設計を含めたか
- [ ] ゴールデンデータの棚卸し頻度とオーナーシップを定めたか
- [ ] LLM-as-Judgeを使う場合、評価用モデルの温度・再実行回数・コストを見積もったか
- [ ] 定期実行（cron）の頻度を `[cost_sensitivity]` から決定し、モデルドリフト検知の遅延許容度と合わせて根拠を提示したか
