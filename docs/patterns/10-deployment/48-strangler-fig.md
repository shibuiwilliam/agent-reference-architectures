---
title: "Strangler Fig｜段階的置換"
tags:
  - "デプロイ・ベンダー抽象化・移行"
  - "F2 失敗コスト"
  - "F8 説明責任・規制"
---

# #48 Strangler Fig｜段階的置換

!!! abstract "一言"
    既存の非AI処理をエージェントで一括置換せず、ルーティング層を介して段階的に移行する。

## 概要

既存のルールベース処理や手作業ワークフローをAIエージェントに置き換える際、ビッグバンリリースはリスクが高い。Strangler Fig（絞め殺しの木）パターンは、既存システムの前段にルーティング層を置き、条件に合うトラフィックだけをエージェントに流す。成功が確認できたら対象を段階的に広げ、最終的に旧システムを退役させる。マーティン・ファウラーのStrangler Fig Applicationパターンをエージェント導入に適用したもの。

## 設計

```mermaid
flowchart LR
    R[リクエスト] --> RT[ルーティング層]
    RT -->|対象外| OLD[既存システム]
    RT -->|対象| AG[エージェント]
    AG -->|成功| RES[レスポンス]
    AG -->|失敗/低信頼| OLD
```

ルーティング層はリクエストの種別・テナント・地域・信頼度スコア等に基づいて振り分けを決定する。初期は全トラフィックを既存システムに流しつつエージェントにシャドーで送り、出力を比較する。品質が一定水準を満たしたカテゴリから順にエージェントに切り替える。エージェントが失敗した場合のフォールバック先として既存システムを残す。

## 解決する課題

エージェントの本番品質は事前に完全には検証できず、一括導入は大規模な障害リスクを伴う `[F2]`。段階的移行により、問題が小さいうちに発見・修正できる。監査観点でも「いつ・どの範囲をエージェントに移行したか」の記録が残る `[F8]`。

## 向き / 不向き

- **向き**: 既存の本番システムがあり、エージェントへの移行リスクを管理したいケース。トラフィックの種別が分類可能で、段階的な切り替え条件を定義できる場合。
- **不向き**: 新規サービスで既存システムが存在しない場合（段階移行の対象がない）。全リクエストが強く結合しており、部分的な切り替えが困難な場合。

## 要素技術

- ルーティング: Feature Flag（LaunchDarkly、Unleash）、API Gateway のルーティングルール
- シャドーテスト: [#35 Production Replay](../07-observability/35-production-replay.md) と組み合わせ
- 品質比較: [#34 Evaluation CI/CD](../07-observability/34-evaluation-ci-cd.md) で新旧出力を自動比較
- フォールバック: [#40 Fallback & Graceful Degradation](../08-cost-scaling/40-fallback-graceful-degradation.md)

## 調整（程度）

- **移行速度（慎重 ↔ 積極的）** — 慎重すぎると移行が完了せず二重運用コストが膨張 ⇔ 積極的すぎると品質未検証の範囲が拡大 / 決め手 `[F2]` / 目安: カテゴリ単位で2〜4週間の安定稼働を確認してから次へ。→ [程度ダイヤル](../../decisions/tuning-dials.md)

## 関連パターン

- [#36 Shadow / Canary Deployment](../07-observability/36-shadow-canary-deployment.md) — シャドー・カナリアデプロイで品質を段階検証
- [#45 Agent Runtime Abstraction](45-agent-runtime-abstraction.md) — 抽象化により新旧ランタイムの切り替えを容易にする
- [#40 Fallback & Graceful Degradation](../08-cost-scaling/40-fallback-graceful-degradation.md) — エージェント失敗時に既存システムへフォールバック

## 参考

- Martin Fowler, "Strangler Fig Application" (2004)
