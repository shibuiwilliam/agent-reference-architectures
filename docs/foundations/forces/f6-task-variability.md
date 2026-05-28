---
title: "[F6] タスクの変動性"
tags:
  - "駆動変数"
---

# [F6] タスクの変動性（Task Variability）

!!! abstract "一言"
    タスクが定型的なルーチンか探索的な未知の問題かを測るフォース。変動性が高いほどエージェントの自律性が求められ、低いほどワークフローで十分になります。

## 概要

請求書の定型処理なら手順をフローチャートに落とせますが、未知のバグを調査するタスクでは、どのファイルを読み、どのログを追い、誰に聞くかを実行しながら判断するしかありません。この「手順を事前に決められるか」が、ワークフローで済むかエージェントが必要かの分岐点です。

タスクの変動性は、処理手順の予測可能性を表します。「LLMにどこまで判断を委ねるか」という根本的な問いに直結するフォースです。

## なぜ重要か

変動性が低いタスクにエージェントの自律判断を持ち込むと、不要なハルシネーションリスクとコストを招きます。逆に、変動性が高いタスクを固定ワークフローに押し込めば、想定外のケースに対応できずエラーが頻発します。タスクの性質と制御構造のミスマッチは、信頼性とコストの両面を悪化させます。

## 値域の解釈

### 低い場合

手順が固定され、入力のバリエーションも限定的な状況です。請求書の定型処理、既知フォーマットのデータ変換、テンプレートに沿った通知文生成、定期レポートの集計などが該当します。分岐条件が事前に列挙でき、ワークフローエンジンやルールベースの処理で十分対応できます。LLMは特定ノードの自然言語処理にのみ限定的に使うイメージです。

### 高い場合

手順自体が事前に確定できず、実行中に計画を立てながら進める必要がある状況です。オープンエンドなリサーチ、未知のバグの調査、複雑な要件のコード生成、多段階の交渉などが典型例です。必要なツールの選択、実行順序、打ち切り判断をエージェントが自律的に行う必要があり、Plan-and-Execute や ReAct 的なループが求められます。

## 評価の指針

- タスクの処理手順をフローチャートで事前に記述できるか
- 入力パターンの種類は有限か、それとも無限に近いか
- 過去のリクエストの何割が「想定外」のケースだったか
- 処理中に外部情報の検索や追加ツールの呼び出しが動的に必要になるか
- 同じタスクを異なる人が処理したとき、手順が大きく異なるか

## 影響する設計判断

### 関連するダイヤル

- [自律レベル](../../decisions/dials/autonomy-level.md) — 変動性が高いほどエージェントの自律レベルを上げる
- [公開ツール数](../../decisions/dials/exposed-tool-count.md) — 探索タスクでは利用可能なツールを増やす
- [Temperature](../../decisions/dials/temperature.md) — 探索的タスクではtemperatureを上げて多様な出力を得る

### 関連する二者択一

- [ワークフロー ↔ エージェント](../../decisions/tradeoffs-catalog/workflow-vs-agent.md) — 変動性が低ければワークフロー、高ければエージェント
- [Plan ↔ React](../../decisions/tradeoffs-catalog/plan-vs-react.md) — 変動性が中程度なら計画駆動、極めて高ければ反応駆動
- [オーケストレーション ↔ コレオグラフィー](../../decisions/tradeoffs-catalog/orchestration-vs-choreography.md) — 変動性が高く参加者が多い場合はコレオグラフィーが有利になりうる
- [構造化 ↔ 自由形式](../../decisions/tradeoffs-catalog/structured-vs-freeform.md) — 定型タスクは構造化入出力で十分、探索タスクは自由形式が必要

## 関連パターン

- [#3 Workflow Backbone + Agent Node](../../decisions/tradeoffs-catalog/workflow-vs-agent.md) — 骨格はワークフロー、判断が必要なノードだけエージェントに委譲する
- [#59 Workflow-Agent Spectrum Selector](../../decisions/tradeoffs-catalog/workflow-vs-agent.md) — サブタスク毎に決定論と自律のバランスを選定する
- [#12 Blackboard](../../decisions/tradeoffs-catalog/orchestration-vs-choreography.md) — 探索的タスクで複数エージェントが共有黒板を介して協調する
- [#50 Editable Plan](../../decisions/tradeoffs-catalog/plan-vs-react.md) — エージェントの計画を人間が編集してから実行する
- [#9 Supervisor & Specialist Agents](../../decisions/tradeoffs-catalog/single-vs-multi-agent.md) — 変動性が高いタスクを専門エージェントに動的に委譲する

<!-- BEGIN:GEN:patterns -->

## 関与する具体構造

| # | パターン | 一言 | 向き |
|---|---------|------|------|
| #3 | **Workflow Backbone + Agent Node** | 骨格は決定論、判断だけ委譲 | 固定手順にAI判断を組み込む場面、規制業種で再現性が必要 |
| #9 | **Supervisor & Specialist Agents** | 統括役が専門役へ委譲する | 多様なタスク種別（FAQ/技術/請求）、マルチモーダル、ドメイン専門性が分離可能 |
| #12 | **Blackboard** | 共有黒板で疎結合に協調 | 複雑なマルチエージェント分析、動的なエージェント参加、探索的問題解決 |
| #50 | **Editable Plan** | 実行前に計画を人が編集 | マルチステップ、手順が変動、再実行コストが高い |
| #59 | **Workflow–Agent Spectrum Selector** | サブタスク毎に決定論↔自律を選定 | 複数サブタスクのシステム設計、定型と探索が混在するタスク |
<!-- END:GEN:patterns -->
