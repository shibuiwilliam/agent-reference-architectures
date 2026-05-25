---
title: "[F6] タスクの変動性"
tags:
  - "駆動変数"
---

# [F6] タスクの変動性（Task Variability）

!!! abstract "一言"
    タスクが定型的なルーチンか探索的な未知の問題かを測るフォース。変動性が高いほどエージェントの自律性が求められ、低いほどワークフローで十分になる。

## 概要

タスクの変動性は、処理手順の予測可能性を表す。毎回同じ手順で済む定型タスクと、状況に応じて手順自体を発見・組み替える必要がある探索タスクでは、適切な制御構造がまったく異なる。このフォースは「LLMにどこまで判断を委ねるか」の根本的な分岐点を決める。

## なぜ重要か

変動性が低いタスクにエージェントの自律判断を持ち込むと、不要なハルシネーションリスクとコストを招く。逆に変動性が高いタスクを固定ワークフローに押し込むと、想定外のケースに対応できずエラーが頻発する。タスクの性質と制御構造のミスマッチは、信頼性とコストの両方を悪化させる。

## 値域の解釈

### 低い場合

手順が固定され、入力のバリエーションも限定的な状況。請求書の定型処理、既知フォーマットのデータ変換、テンプレートに沿った通知文生成、定期レポートの集計などが該当する。分岐条件が事前に列挙でき、ワークフローエンジンやルールベースの処理で十分に対応できる。LLMは特定ノードの自然言語処理にのみ限定的に使う。

### 高い場合

手順自体が事前に確定できず、実行中に計画を立てながら進める必要がある状況。オープンエンドなリサーチ、未知のバグの調査、複雑な要件のコード生成、多段階の交渉などが典型例。必要なツールの選択、実行順序、打ち切り判断をエージェントが自律的に行う必要があり、Plan-and-Execute や ReAct 的なループが求められる。

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

- [#3 Workflow Backbone + Agent Node](../../patterns/01-execution/03-workflow-backbone-agent-node.md) — 骨格はワークフロー、判断が必要なノードだけエージェントに委譲する
- [#59 Workflow-Agent Spectrum Selector](../../patterns/01-execution/59-workflow-agent-spectrum-selector.md) — サブタスク毎に決定論と自律のバランスを選定する
- [#12 Blackboard](../../patterns/02-composition/12-blackboard.md) — 探索的タスクで複数エージェントが共有黒板を介して協調する
- [#50 Editable Plan](../../patterns/11-ux/50-editable-plan.md) — エージェントの計画を人間が編集してから実行する
- [#9 Supervisor & Specialist Agents](../../patterns/02-composition/09-supervisor-specialist-agents.md) — 変動性が高いタスクを専門エージェントに動的に委譲する
