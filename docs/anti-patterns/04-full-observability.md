---
title: "観測基盤フル投入"
tags:
  - "アンチパターン"
  - "程度の誤り"
---

# 4. 観測基盤フル投入

!!! abstract "一言"
    全リクエスト・全トークンを高コストな分析パイプラインに流し、観測コスト自体がLLM利用コストを超えてしまうアンチパターン。

## よくある場面

あるチームが本番エージェントの品質監視のために、全リクエストのプロンプトと応答をリアルタイムで分析パイプラインに送信する構成を組みました。各リクエストについて、毒性スコア、幻覚検出、トピック分類、感情分析をLLMベースの評価器で実行しました。初期は数百リクエスト/日で問題ありませんでしたが、利用者が増えて数万リクエスト/日になったとき、観測パイプラインのLLMコストがエージェント本体のLLMコストの3倍に達しました。

ストレージも肥大化しました。全トレースを無期限で保持していたため、数ヶ月で数TBに達し、障害調査のためにログを検索するクエリが数分かかるようになりました。「観測のための観測」が本来の目的を阻害する状況に陥りました。

## 症状

- 観測・監視コストがLLM利用コストの50%を超えています
- ログストレージが急速に肥大化し、検索性能が低下します
- 観測パイプライン自体が障害のSPOF（単一障害点）になります
- 大量のアラートが発生し、重要なアラートが埋もれます（アラート疲れ）
- 観測データの大半が参照されないまま保持されています

## 根本原因

「何が起きるか分からないから全部記録する」という不安駆動の設計が原因です。従来のWebシステムではログのコストは相対的に低かったですが、LLMベースの評価器を使った品質分析は1件あたりのコストが高くなります。また、ログの保持期間やサンプリング率を段階的に設計するノウハウが確立されていません。

`[F8]` 説明責任と `[F7]` コスト感度のバランスが取れていないことが根本にあります。

## 発見方法

- **コスト比率の確認**: 観測関連コスト（LLM評価器、ストレージ、分析基盤）とエージェント本体のLLMコストを比較します
- **データ利用率の確認**: 保存しているログ・トレースのうち、実際に参照（クエリ・ダッシュボード表示）された割合を確認します
- **保持期間の確認**: 90日以上前のログが参照されたことがあるか確認します
- **メトリクス**: `observability_cost / agent_cost`、`log_storage_gb`、`log_query_latency_p99`

## 対策

### ステップ1: Hot/Cold/Archiveの3層に分離する

直近のデータ（Hot）は高速ストレージで詳細に保持し、古いデータ（Cold）は安価なストレージに圧縮して移動します。一定期間を超えたデータは集計値のみ残して削除します。

### ステップ2: サンプリング率を段階的に設定する

正常リクエストはサンプリング（例: 10%）で記録し、エラーや異常検知されたリクエストのみ詳細記録します。

### ステップ3: LLMベースの評価をサンプリングに限定する

全リクエストにLLM評価器を通すのではなく、サンプリングされたリクエストのみ評価します。リアルタイム性が必要なものはルールベースの軽量チェックで代替します。

```yaml
# 観測設定例
observability:
  tracing:
    normal_sampling_rate: 0.10   # 正常: 10%サンプリング
    error_sampling_rate: 1.0     # エラー: 全件記録
    slow_request_threshold: 10s  # 遅延: 全件記録
  storage:
    hot_retention: 7d
    cold_retention: 90d
    archive: aggregates_only
  llm_evaluation:
    sampling_rate: 0.05          # 5%のみLLM評価
    rule_based_check: all        # 全件にルールベースチェック
```

## 具体例

### Before（問題のある状態）

```python
# 全リクエストをフルパイプラインで分析
for request in all_requests:
    trace = record_full_trace(request)
    toxicity = llm_evaluate_toxicity(trace)
    hallucination = llm_detect_hallucination(trace)
    topic = llm_classify_topic(trace)
    store_forever(trace, toxicity, hallucination, topic)
# 観測コスト: エージェントコストの3倍
```

### After（改善後）

```python
for request in all_requests:
    trace = record_lightweight_trace(request)  # 軽量メタデータ
    rule_check = rule_based_check(trace)       # ルールベース（低コスト）

    if rule_check.anomaly or is_sampled(rate=0.05):
        # 異常 or サンプリング対象のみ詳細分析
        llm_evaluate(trace)
        store_hot(trace, retention="7d")
    else:
        store_cold(trace.summary(), retention="90d")
# 観測コスト: エージェントコストの15%
```

## 関連するアンチパターン

- [最強モデル一択](03-strongest-model-only.md) — 「最高品質をどこにでも」という同じ発想です
- [目盛りの根拠を残さない](06-no-rationale.md) — サンプリング率や保持期間の根拠がありません

## 関連パターン

- [#54 Tiered (Hot/Cold) Observability](../patterns/07-observability/54-tiered-observability.md) — Hot/Coldの分離アーキテクチャ
- [#32 Agent Trace](../patterns/07-observability/32-agent-trace.md) — トレースの設計
- [#34 Evaluation CI/CD](../patterns/07-observability/34-evaluation-ci-cd.md) — 評価をCI/CDに組み込みます
