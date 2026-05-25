---
title: "Planner-Executor-Reviewer｜計画・実行・検証の分離"
tags:
  - "エージェント構成・分担"
  - "F2 失敗コスト"
  - "F3 1リクエストの価値"
---

# #8 Planner-Executor-Reviewer｜計画・実行・検証の分離

!!! abstract "一言"
    計画・実行・検証を**別ロール**に分けることで、単一エージェントの自己過信や見落としを構造的に抑える。

## 概要

1つのLLMに「考えて・やって・確かめて」をすべて任せると、自分の計画を自分で検証するという利益相反が生まれる。Planner-Executor-Reviewer は、計画（Plan）・実行（Execute）・検証（Review）を独立したロール――場合によっては別モデルや別プロンプト――に分離する構成である。Planner がステップ列を生成し、Executor がツール呼び出しや副作用を実行し、Reviewer が結果を検証して差し戻しまたは承認する。

!!! info "意思決定上の位置づけ"
    - **必要にするフォース**: `[F2]` 失敗コスト・`[F3]` 1リクエストの価値
    - **関与する決定**: [相反](../../decisions/tradeoffs.md) の Plan↔ReAct
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

## 設計

```mermaid
flowchart LR
    P[Planner] -->|計画| E[Executor]
    E -->|実行結果| R[Reviewer]
    R -->|OK| Out[最終出力]
    R -->|差し戻し| P
```

Planner はタスク分解と順序付けを担い、構造化された計画（JSON やステップリスト）を出力する。Executor は計画を逐次実行し、各ステップの結果を記録する。Reviewer は実行結果を計画の意図・品質基準と照合し、不合格なら理由を添えて Planner へ差し戻す。差し戻しループには回数上限を設け、[#5 Time-Budgeted Agent Loop](../01-execution/05-time-budgeted-agent-loop.md) と組み合わせて暴走を防ぐ。

## 解決する課題

`[F2]` 失敗コストが高い場面で、単一エージェントの「やったつもり」を防ぐことができる。計画と検証が独立しているため、Executor の実行ミスや Planner の論理飛躍を第三者視点で捕捉しやすくなる。`[F3]` 1リクエストの価値が高いほど、この分離に投じるトークンコストは正当化される。

## 向き / 不向き

- **向き**: コード生成→テスト→修正、レポート作成→ファクトチェック、複数ステップの調査タスクなど、検証基準を明示できるタスクに適している。
- **不向き**: 単発の質問応答や分類など、計画・検証を分けるオーバーヘッドがタスク自体より重い場合には向かない。リアルタイム性が求められる低レイテンシ要件 `[F4]` にも合わない。

## 要素技術

- Planner: 構造化出力（[#14 Structured Output Contract](../03-io-contract/14-structured-output-contract.md)）で計画を JSON/YAML で返す
- Executor: ツール呼び出し基盤（LangGraph・CrewAI・自前ループ）
- Reviewer: 別プロンプト／別モデル／ルールベース検証の組み合わせ
- ループ制御: 最大リトライ回数、タイムアウト

## 調整（程度）

- **検証の厳しさ** — Reviewer の合格基準を緩めるとループは収束しやすいが、ミスを見逃しやすくなる。一方、厳しすぎるとループが収束しない / 決め手 `[F2]` / 目安: 差し戻し上限は2〜3回。→ [程度ダイヤル](../../decisions/tuning-dials.md)

## 関連パターン

- [#10 Agent Ensemble & Debate](10-agent-ensemble-debate.md) — 検証を討論形式に拡張する変種
- [#28 Verifier Agent / Critic](../06-reliability/28-verifier-agent-critic.md) — Reviewer を独立した検証エージェントとして汎用化したもの
- [#50 Editable Plan](../11-ux/50-editable-plan.md) — Planner の出力を人間が編集してから Executor に渡す
- [#5 Time-Budgeted Agent Loop](../01-execution/05-time-budgeted-agent-loop.md) — 差し戻しループの暴走防止
