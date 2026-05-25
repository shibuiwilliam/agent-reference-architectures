---
title: "Adaptive Effort｜適応的努力配分"
tags:
  - "コスト・性能・スケーリング"
  - "F7 コスト感度・スケール"
  - "F2 失敗コスト"
---

# #56 Adaptive Effort｜適応的努力配分

!!! abstract "一言"
    リクエストの難易度・重要度に応じて**投入する計算量（推論ステップ数・トークン数・検証回数）を増減**する。


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>メタデータ（機械可読） — #56 Adaptive Effort｜適応的努力配分</summary>

| 項目 | 値 |
|------|-----|
| **ID** | 56 |
| **カテゴリ** | 08-cost-scaling — コスト・性能・スケーリング |
| **フォース** | `[F7]`, `[F2]` |
| **ダイヤル** | — |
| **二者択一** | — |
| **関連パターン** | #37, #5, #28 |
| **向き** | 難易度が変動するワークロード、thinking-budget API利用可能、コスト制約下の品質柔軟性 |
| **不向き** | 均一な複雑さ; 常に最大努力が必要（医療診断）; コスト>>品質 |
| **要素技術** | 軽量難易度分類器, Anthropic thinking budget, OpenAI reasoning effort, 動的 max_tokens |

</details>
<!-- END:GEN:meta -->

## 概要

「明日の予定を教えて」と「この契約書のリスクを分析して」では、必要な推論の深さがまったく異なる。前者に5段階の検証を行うのは無駄であり、後者を1ステップで済ませるのは危険である。

[#37 Semantic Gateway](37-semantic-gateway-cost-aware-router.md) がモデルを切り替えるのに対し、Adaptive Effortは同一モデル内でも投入する計算量を調整する。簡単なクエリには短い思考・少ないステップで即答し、複雑・高リスクなクエリにはChain-of-Thoughtの深化、複数パスの検証、追加のツール呼び出しを行う。「すべてに全力」ではなく、難易度と失敗コストに応じて計算資源を傾斜配分する考え方である。

!!! info "意思決定上の位置づけ"
    - **必要にするフォース**: `[F7]` コスト感度・スケール・`[F2]` 失敗コスト
    - **関与する決定**: [程度（ダイヤル）](../../decisions/tuning-dials.md) の モデル階層
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

## 設計

リクエストを受けたら、まず軽量な難易度推定（入力の長さ・複雑度スコア・ドメイン分類）を行う。その推定結果に応じて、エージェントの実行パラメータを動的に設定する。具体的には、最大推論ステップ数、思考トークン上限（thinking budget）、検証器の起動有無、アンサンブル数などを調整する。また、推定が外れた場合に備えて、初回応答の自信度が低ければ上位の努力レベルで再試行するエスカレーション機構も組み込んでおく。

## 解決する課題

エージェントの計算コストはステップ数・トークン数に比例する。全リクエストに最大限の推論リソースを割くとコストが膨張する `[F7]`。一方で一律に制限すると、高リスクなリクエストの品質が低下してしまう `[F2]`。Adaptive Effortはリソース配分を動的に最適化することで、同一予算内での期待品質を最大化する。

## 向き / 不向き

- **向き**: 難易度のばらつきが大きいワークロード、コスト予算が限られた運用、LLMのthinking budget機能を活用できる環境。
- **不向き**: 全リクエストが同等の複雑さである場合には効果が薄い。また、難易度推定の誤りが致命的な結果につながる高リスク領域（医療診断など、常に最大努力が求められるケース）にも向かない。

## 要素技術

- 難易度推定: 小型分類モデル、ルールベース（入力長・キーワード）、前段LLMの確信度
- 努力調整: Anthropic extended thinking budget、OpenAI reasoning effort、max_tokens動的設定
- 検証スケーリング: [#28 Verifier Agent](../06-reliability/28-verifier-agent-critic.md) の起動条件を難易度連動にする

## 調整（程度）

- **努力のレンジ**（最小努力 ⇔ 最大努力）— 最小が低すぎると簡単なクエリでも品質劣化 ⇔ 最大が高すぎるとコスト・レイテンシ爆発 / 決め手 `[F7]` `[F2]` / 目安: 最小=単発推論、最大=3パス検証付き推論。→ [程度ダイヤル](../../decisions/tuning-dials.md)

## 関連パターン

- [#37 Semantic Gateway](37-semantic-gateway-cost-aware-router.md) — モデル選択レベルの最適化（Adaptive Effortはモデル内の計算量調整）
- [#5 Time-Budgeted Agent Loop](../01-execution/05-time-budgeted-agent-loop.md) — 時間・回数の予算制約と組み合わせて使う
- [#28 Verifier Agent / Critic](../06-reliability/28-verifier-agent-critic.md) — 高努力時に検証を追加するかの判断に使う

## 参考

- Anthropic Extended Thinking Documentation
- OpenAI Reasoning Effort Parameter
