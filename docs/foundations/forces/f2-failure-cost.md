---
title: "[F2] 失敗コスト"
tags:
  - "駆動変数"
---

# [F2] 失敗コスト（Failure Cost）

!!! abstract "一言"
    エージェントが誤った出力や操作をしたとき、どれだけの痛み（金銭・法務・安全・信用）が生じるかを測るフォース。

## 概要

社内チャットボットが社員の質問に的外れな回答をしても笑い話で済むが、医療診断支援AIが誤った投薬量を提示すれば患者の命に関わります。同じ「間違い」でも、その代償の大きさによって必要な防御策はまるで違います。

失敗コストは、エージェントの誤りがもたらす損害の深刻度を表します。このフォースの値が高いほど、検証・承認・監査の層を厚くする必要があります。

## なぜ重要か

失敗コストを過小評価すると、本番環境で「たまたまうまく動いている」状態に安住し、稀な失敗が訴訟・規制違反・人的被害に直結します。逆に過大評価すると、すべての操作に重い承認フローを課してスループットが崩壊します。正確な見積もりが、防御層の適切な厚みを決めます。

## 値域の解釈

### 低い場合

誤っても実害が軽微な状況。社内FAQボット、ドラフト文書の下書き生成、開発者向けコード補完などが典型例。ユーザーが結果を目視確認してから使う前提があり、誤りのフィードバックループが短いです。この領域ではガードレールを軽くし、速度や利便性を優先できます。

### 高い場合

誤りが金銭的損失・法的責任・安全上の危険に直結する状況。金融取引の執行、医療レポートの生成、法務文書のレビュー、インフラ変更の自動実行などが該当します。1件の誤りが数百万円の損害や規制当局からの制裁につながりえます。多段階の検証、独立したVerifierエージェント、Policy-as-Code による制約の明文化が必要になります。

## 評価の指針

- エージェントの誤出力が直接ユーザーや外部システムに届くか、人間のレビューを経るか
- 最悪ケースの金銭的損失はいくらか（1件あたり）
- 誤りが法的責任や規制違反を引き起こす可能性はあるか
- 誤りが人の安全や健康に影響しうるか
- 過去に類似システムで発生した障害の影響範囲はどの程度だったか

## 影響する設計判断

### 関連するダイヤル

- [自己修正ループ回数](../../decisions/dials/self-correction-loops.md) — 失敗コストが高いほど、出力を自己検証・修正するループを増やす
- [ガードレール厳格度](../../decisions/dials/guardrail-strictness.md) — コストが高い領域では厳格なガードレールを設定する
- [HITL頻度](../../decisions/dials/hitl-frequency.md) — 失敗コストに比例して人間承認の頻度を上げる
- [Best-of-N](../../decisions/dials/best-of-n.md) — 高コスト判断では複数候補から最良を選ぶ
- [自律レベル](../../decisions/dials/autonomy-level.md) — 失敗コストが高いほど自律レベルを抑制する

### 関連する二者択一

- [単一エージェント ↔ マルチエージェント](../../decisions/tradeoffs-catalog/single-vs-multi-agent.md) — 失敗コストが高ければ検証役を分離するマルチエージェント構成が有利
- [同一モデル ↔ 異モデル](../../decisions/tradeoffs-catalog/same-vs-different-model.md) — 高コスト判断では異なるモデルで検証し、共通の盲点を避ける
- [インライン検証 ↔ 事後検証](../../decisions/tradeoffs-catalog/inline-vs-post-verification.md) — 失敗コストが高ければインライン検証を優先
- [ワークフロー ↔ エージェント](../../decisions/tradeoffs-catalog/workflow-vs-agent.md) — 高コスト領域ではワークフローで制御可能性を確保

## 関連パターン

- [#28 Verifier Agent / Critic](../../patterns/06-reliability/28-verifier-agent-critic.md) — 独立した検証器で出荷前検査を行う
- [#31 Human Approval Checkpoint](../../patterns/06-reliability/31-human-approval-checkpoint.md) — 高リスク操作の前に人間承認を挟む
- [#30 Policy-as-Code Guardrail](../../patterns/06-reliability/30-policy-as-code-guardrail.md) — 制約をコード化して機械的に判定する
- [#10 Agent Ensemble & Debate](../../patterns/02-composition/10-agent-ensemble-debate.md) — 複数エージェントの合議で頑健性を高める
- [#8 Planner-Executor-Reviewer](../../patterns/02-composition/08-planner-executor-reviewer.md) — 計画・実行・検証を分離し、各段階で品質を担保する

<!-- BEGIN:GEN:patterns -->

## 関与する具体構造

| # | パターン | 一言 | 向き |
|---|---------|------|------|
| #4 | **Agent Saga** | 副作用連鎖を補償で巻き戻す | 複数外部システムへの書き込み連鎖（カレンダー→チケット→メール） |
| #8 | **Planner-Executor-Reviewer** | 計画/実行/検証を別ロールに分ける | コード生成→テスト→修正、レポートのファクトチェック、検証基準が明確なマルチステップ調査 |
| #10 | **Agent Ensemble & Debate** | 複数で解き合議・討論で頑健化 | 高リスク判断（医療・金融）、正確性検証、不一致検出が高価値 |
| #11 | **Deterministic Core, Probabilistic Edge** | 中核は決定論、周辺だけAI | 金融・保険・医療プロトコル、正確な金額・ロジックが必須 |
| #15 | **Inverted Structured Output** | 最終実行でなく中間判断を出させる | 承認・分類・ルーティング判断、判断のみ（実行はコード） |
| #16 | **Ambiguity Negotiation** | 曖昧なら確認してから実行 | 可逆な操作、複数解釈可能な入力（ファイル削除）、スロット不足の入力 |
| #18 | **Least-Privilege Tool Binding** | セッション毎に最小権限を束縛 | 10以上のツール、マルチテナント、ユーザー毎に異なる権限 |
| #19 | **Dry-Run First Tool Execution** | 副作用はまず模擬実行→承認 | データ変更（削除・API書き込み）、インフラ変更（Terraform的操作） |
| #28 | **Verifier Agent / Critic** | 独立した検証器で出荷前検査 | コード生成（テスト検証）、金融レポート、法務文書、公開コンテンツ |
| #30 | **Policy-as-Code Guardrail** | 制約をコード化し別途判定 | 金融・医療・法務の高失敗コスト操作、監査証跡が必要、決定論的ルールが可能 |
| #31 | **Human Approval Checkpoint** | 高リスク前に人間承認 | 金融、インフラ変更、顧客メール送信、契約確認 |
| #44 | **Dual-LLM Privilege Separation** | 隔離LLMと特権LLMを分離 | 信頼できない入力→ツールチェーン、高リスク副作用（決済・削除・通知） |
| #48 | **Strangler Fig** | 既存処理を段階的に置換 | 既存システムのエージェント置換（段階的リスク管理）、ルールベース→AI段階移行 |
| #51 | **Agent-to-Human Escalation** | 自信/権限不足で人間へ引き継ぎ | サポート/法務/医療ドメイン、不確実→エスカレーションが推測より良い、専門家判断が必要 |
| #52 | **Agent Constitution** | 行動原則を体系的に展開 | マルチエージェント組織、規制業種、監査証跡が必要、行動一貫性が重要 |
| #56 | **Adaptive Effort** | 難易度で投入計算量を増減 | 難易度が変動するワークロード、thinking-budget API利用可能、コスト制約下の品質柔軟性 |
| #57 | **Autonomy Ladder** | 実績に応じ自律性を段階的に昇格 | エージェント権限の段階的ロールアウト、タスク種別ごとにリスクレベルが異なる |
| #59 | **Workflow–Agent Spectrum Selector** | サブタスク毎に決定論↔自律を選定 | 複数サブタスクのシステム設計、定型と探索が混在するタスク |
<!-- END:GEN:patterns -->
