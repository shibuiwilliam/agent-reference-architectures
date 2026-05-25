---
title: "Tiered (Hot/Cold) Observability｜二層観測"
tags:
  - "観測性・監査・評価"
  - "F8 説明責任・規制"
  - "F7 コスト感度・スケール"
---

# #54 Tiered (Hot/Cold) Observability｜二層観測

!!! abstract "一言"
    観測データを**高速層（Hot）と安価層（Cold）**に二分し、リアルタイム性とコストを両立させる。


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>メタデータ（機械可読） — #54 Tiered (Hot/Cold) Observability｜二層観測</summary>

| 項目 | 値 |
|------|-----|
| **ID** | 54 |
| **カテゴリ** | 07-observability — 観測性・監査・評価 |
| **フォース** | `[F8]`, `[F7]` |
| **ダイヤル** | trace-sampling-rate, log-retention |
| **二者択一** | — |
| **関連パターン** | #32, #35, #33 |
| **向き** | 高トラフィックエージェントシステム、規制上の長期保持、コスト最適化優先 |
| **不向き** | 低トラフィックで単一層で十分; 超高速コールドアクセスが必要 |
| **要素技術** | ClickHouse, Elasticsearch, Prometheus, S3+Parquet, BigQuery, Glacier, ライフサイクルポリシー |

</details>
<!-- END:GEN:meta -->

## 概要

エージェントのトレースをすべてリアルタイム検索可能なDBに置いておくと、月間数百万リクエスト規模ではストレージ費用が急激に膨らんでいく。かといって全部をオブジェクトストレージに移してしまうと、障害発生時に「直近1時間のトレースを見たい」という要求にすぐ応えられない。

二層観測では、直近データ（数時間〜数日）をHot層に保持してリアルタイムのアラート・ダッシュボードに活用し、古いデータはCold層へ自動移行して長期保存・監査用途に備える。

!!! info "意思決定上の位置づけ"
    - **必要にするフォース**: `[F8]` 説明責任・規制・`[F7]` コスト感度・スケール
    - **関与する決定**: [程度（ダイヤル）](../../decisions/tuning-dials.md) の トレースサンプリング率・ログ保持期間
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

## 設計

```mermaid
flowchart LR
    Agent[Agent] -->|emit| Collector[Collector / Buffer]
    Collector --> Hot[(Hot Store<br/>直近N日)]
    Hot -->|TTL超過| Cold[(Cold Store<br/>長期保存)]
    Hot --> Dash[Dashboard / Alert]
    Cold --> Audit[監査・Replay]
```

Collectorがデータを受け取り、まずHot層（時系列DB・検索エンジン）へ書き込む。TTLポリシーに基づいて、期限切れのデータをHot層からCold層（オブジェクトストレージ＋カラムナDB）へ移行する。監査やリプレイが必要なときは、Cold層からバッチクエリで取得する。

## 解決する課題

エージェント1リクエストあたり数十スパン・数千トークンのログが生まれる。月間数百万リクエストの規模になると、すべてをリアルタイムDBに置くストレージ費用は数倍〜数十倍に膨らむ `[F7]`。一方で、規制要件により数年間の保持が求められる場合もある `[F8]`。二層構成はこの矛盾をうまく解消する仕組みである。

## 向き / 不向き

- **向き**: 高トラフィックなエージェントシステム、長期監査が必要な規制領域、コスト最適化が求められる運用。
- **不向き**: トラフィックが少なく単一ストアで十分な規模の場合は、過剰設計になりやすい。

## 要素技術

- Hot層: ClickHouse、Elasticsearch、Prometheus + Grafana
- Cold層: S3 / GCS + Parquet、BigQuery（長期ストレージ）、Glacier
- 移行: Lifecycle Policy（S3）、Retention Policy（ClickHouse TTL）

## 調整（程度）

- **Hot層の保持期間** — 短すぎるとインシデント調査に支障 ⇔ 長すぎるとコスト増 / 決め手 `[F7]` `[F8]` / 目安: 3〜14日。→ [程度ダイヤル](../../decisions/tuning-dials.md)

## 関連パターン

- [#32 Agent Trace](32-agent-trace.md) — 二層に保存するトレースデータそのものを生成する
- [#35 Production Replay](35-production-replay.md) — Cold層のデータを使って本番ログを再生する
- [#33 Version Pinning](33-version-pinning.md) — バージョン情報をトレースに付与し、Cold層でも追跡可能にする

## 参考

- Grafana Mimir / Loki のリテンションポリシー設計
- AWS S3 Intelligent-Tiering
