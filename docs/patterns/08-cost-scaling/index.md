# VIII. コスト・性能・スケーリング


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F7]` コスト感度、`[F3]` リクエスト価値、`[F9]` プロバイダ信頼度
    - **主なダイヤル**: モデル階層閾値、キャッシュ類似度閾値、リトライ回数 → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **主な二者択一**: 単一↔マルチプロバイダ、Fail-fast↔縮退 → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

エージェントのリクエスト数が増えるにつれ、LLMのAPI費用は想定を超えて膨らんでいく。さらに、外部プロバイダの障害やレート制限で突然応答が返らなくなる場面も珍しくない。LLMの利用量を資源として管理し、外部LLMの不安定さを吸収するためのパターン群である。

- [#37 Semantic Gateway & Cost-Aware Router｜動的ルーティング](37-semantic-gateway-cost-aware-router.md) — 難易度に応じてモデルを動的に選択する
- [#38 Semantic Result Cache｜セマンティック結果キャッシュ](38-semantic-result-cache.md) — 意味的に近い過去の結果を再利用する
- [#39 Prompt Cache Optimized Context｜プロンプトキャッシュ](39-prompt-cache-optimized-context.md) — 共通prefixを活かしてキャッシュ効率を高める
- [#40 Fallback & Graceful Degradation｜フォールバック縮退](40-fallback-graceful-degradation.md) — 障害時に段階的に縮退してサービスを継続する
- [#56 Adaptive Effort｜適応的努力配分](56-adaptive-effort.md) — 難易度に応じて投入する計算量を増減させる
