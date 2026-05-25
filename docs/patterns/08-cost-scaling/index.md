# VIII. コスト・性能・スケーリング

知能の使用量を資源として管理し、外部LLMの不安定さを吸収する。

- [#37 Semantic Gateway & Cost-Aware Router｜動的ルーティング](37-semantic-gateway-cost-aware-router.md) — 難易度でモデルを動的選択
- [#38 Semantic Result Cache｜セマンティック結果キャッシュ](38-semantic-result-cache.md) — 意味的に近い結果を再利用
- [#39 Prompt Cache Optimized Context｜プロンプトキャッシュ](39-prompt-cache-optimized-context.md) — 共通prefixでキャッシュを効かせる
- [#40 Fallback & Graceful Degradation｜フォールバック縮退](40-fallback-graceful-degradation.md) — 障害時に段階縮退で継続
- [#56 Adaptive Effort｜適応的努力配分](56-adaptive-effort.md) — 難易度で投入計算量を増減
