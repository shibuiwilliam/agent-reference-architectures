---
title: "Workflow Backbone + Agent Node｜決定論骨格＋ノード"
tags:
  - "実行・セッション・オーケストレーション"
  - "F6 タスクの変動性"
  - "F8 説明責任・規制"
---

# #3 Workflow Backbone + Agent Node｜決定論骨格＋ノード

!!! abstract "一言"
    全体の実行順序は決定論的なワークフローエンジンが制御し、判断が必要なノードだけをLLMエージェントに委譲する。

## 概要

ワークフローエンジン（DAG実行器）が骨格となり、データ取得・変換・保存・通知といった定型ステップを決定論的に実行する。そのうえで、LLMの判断力が必要なノード――分類、要約、計画立案など――だけをエージェントに委ねる。骨格が全体の進行を制御するため、監査ログの取得やリトライ制御は既存のワークフロー技術で対応できる。

!!! info "意思決定上の位置づけ"
    - **必要にするフォース**: `[F6]` タスクの変動性・`[F8]` 説明責任・規制
    - **関与する決定**: [相反](../../decisions/tradeoffs.md) の ワークフロー↔エージェント
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

## 設計

```mermaid
flowchart TD
    WF[Workflow Engine] -->|"1. データ取得"| S1[ETLステップ]
    WF -->|"2. 分類判断"| AN[Agent Node / LLM]
    AN -->|"構造化結果"| WF
    WF -->|"3. 後処理"| S2[DB書き込み]
    WF -->|"4. 通知"| S3[Slack / Email]
```

エージェントノードはワークフローの1タスクとして呼ばれ、入力スキーマと出力スキーマが契約化されている。タイムアウト・リトライ・フォールバックはワークフロー側で定義する。

## 解決する課題

エージェントに全体制御を任せると、ステップの順序が非決定的になり、`[F8]` 監査や再現が困難になる。さらに、定型処理までLLMに通すとコスト `[F7]` とレイテンシが不必要に増えてしまう。骨格を決定論的に組み、確率的な判断だけを局所化することで、説明責任と効率を両立できる。

## 向き / 不向き

- **向き**: 業務フローが比較的固定されており、一部のステップだけにAI判断を差し込みたいケースに適している。規制産業でプロセスの再現性が求められる場合にも有効である。
- **不向き**: タスクの手順自体が事前に決まらない探索的な作業（リサーチ、自由形式のコーディングなど）には向かない。ステップ数や順序が動的に変わる場合は [#59 Workflow-Agent Spectrum Selector](59-workflow-agent-spectrum-selector.md) と併用して判断するとよい。

## 要素技術

- ワークフローエンジン: Temporal、Airflow、Step Functions、Prefect、Hatchet
- エージェントノード: LangGraph の単一ノード、OpenAI Agents SDK のハンドオフ先
- 契約: 入出力を [#14 Structured Output Contract](../03-io-contract/14-structured-output-contract.md) で型定義

## 選定（相反）

- **決定論ワークフロー ↔ 自律エージェント** — タスクの変動性 `[F6]` が低ければ骨格寄り、高ければエージェント寄り。デフォルト: 手順が3回以上同じなら骨格化。→ [相反の選定基準](../../decisions/tradeoffs.md)

## 関連パターン

- [#59 Workflow-Agent Spectrum Selector](59-workflow-agent-spectrum-selector.md) — サブタスク単位で骨格と自律の比率を選定するメタパターン
- [#11 Deterministic Core, Probabilistic Edge](../02-composition/11-deterministic-core-probabilistic-edge.md) — 同じ原則をシステム構成レベルで適用したもの
- [#5 Time-Budgeted Agent Loop](05-time-budgeted-agent-loop.md) — エージェントノードの暴走をループ予算で制御する
- [#14 Structured Output Contract](../03-io-contract/14-structured-output-contract.md) — ノード間の入出力を契約化する手段

## 参考

- Temporal Workflow Patterns
- AWS Step Functions + Bedrock Agent 統合
