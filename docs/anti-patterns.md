---
title: アンチパターン
---

# アンチパターン

!!! abstract "一言"
    「やってしまいがち」な設計判断と、その症状・対策。パターンの裏返しとして読む。

## アンチパターン一覧

### 1. リトライストーム

**症状**: LLMプロバイダの一時障害でリトライが殺到し、障害が拡大する。復旧後もバックログが詰まり、正常リクエストの処理が遅延する。

**対策**: 指数バックオフ＋ジッターを必須にする。サーキットブレーカーで閾値超過時にリトライを停止し、[#40 Fallback & Graceful Degradation](patterns/08-cost-scaling/40-fallback-graceful-degradation.md) で縮退運転に切り替える。リトライ回数は [程度ダイヤル](decisions/tuning-dials.md) で管理する。

### 2. 観測基盤フル投入

**症状**: 全リクエスト・全トークンを高コストな分析パイプラインに流し、観測コストがLLM利用コストを超える。ストレージが肥大化し、必要なログが探せない。

**対策**: [#54 Tiered Observability](patterns/07-observability/54-tiered-observability.md) で Hot/Cold を分離する。サンプリング率を `[F8]` と `[F7]` で決め、異常時のみ詳細記録に切り替える。

### 3. 万能マルチエージェント

**症状**: 単一エージェントで十分なタスクにマルチエージェント構成を導入し、通信オーバーヘッド・デバッグ困難・コスト増を招く。

**対策**: [#59 Workflow–Agent Spectrum Selector](patterns/01-execution/59-workflow-agent-spectrum-selector.md) でサブタスク毎に「決定論で十分か、自律が必要か」を判定する。マルチエージェントは `[F6]` タスク変動性が高く、かつ専門性の分離が明確な場合にのみ採用する。

### 4. 無限・過大タイムアウト

**症状**: タイムアウトを長く設定しすぎ（または設定せず）、暴走したエージェントがリソースを占有し続ける。コスト上限もなく、1リクエストで数万円の請求が発生する。

**対策**: [#5 Time-Budgeted Agent Loop](patterns/01-execution/05-time-budgeted-agent-loop.md) で時間・回数・コストの3軸に上限を設ける。[#55 Deadline & Budget Cascade](patterns/01-execution/55-deadline-budget-cascade.md) で子タスクにも予算を伝播する。

### 5. 過剰ガードレール

**症状**: ガードレールを厳しくしすぎて、正当なリクエストの大半が遮断される。ユーザー体験が悪化し、ガードレール回避のためのプロンプト改変が横行する。

**対策**: ガードレールの閾値を `[F5]` 入力信頼度と `[F2]` 失敗コストで段階的に設定する。[#30 Policy-as-Code Guardrail](patterns/06-reliability/30-policy-as-code-guardrail.md) で制約をコード化し、テスト可能にすることで誤検知率を計測・改善する。

### 6. 何でも同期 / 何でも非同期

**症状**: 一律に同期処理にして長時間リクエストでタイムアウトが頻発する。あるいは一律に非同期にして、即答できるリクエストまでジョブキュー経由にし、UXが悪化する。

**対策**: [#58 Sync Facade over Async Core](patterns/01-execution/58-sync-facade-over-async-core.md) で「短ければ同期、超えたら非同期へ昇格」のハイブリッドを採用する。判断基準は `[F4]` レイテンシ予算。

### 7. 最強モデル一択

**症状**: 全リクエストに最大・最高性能のモデルを使い、コストが線形に増大する。分類・要約など簡単なタスクにも高コストモデルを投入している。

**対策**: [#37 Semantic Gateway & Cost-Aware Router](patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) で難易度に応じてモデルを振り分ける。[#56 Adaptive Effort](patterns/08-cost-scaling/56-adaptive-effort.md) で投入計算量を動的に調整する。

### 8. コンテキスト詰め込みすぎ

**症状**: 関連しそうな情報を全てプロンプトに詰め込み、コンテキスト窓を圧迫する。ノイズが増えて回答品質が下がり、コストも増大する。

**対策**: [#24 Context Pack / Assembly](patterns/05-memory-context/24-context-pack-assembly.md) で関連度の高い情報のみを選択的に組み立てる。検索 top-k と投入量を [程度ダイヤル](decisions/tuning-dials.md) で管理する。

### 9. プロンプトをセキュリティ境界にする

**症状**: 「このプロンプトに従ってね」という指示でセキュリティを担保しようとする。プロンプトインジェクションで容易に突破される。

**対策**: セキュリティは**コードと権限で**担保する。[#44 Dual-LLM Privilege Separation](patterns/09-security/44-dual-llm-privilege-separation.md) で隔離LLMと特権LLMを分離し、[#18 Least-Privilege Tool Binding](patterns/04-tools-mcp/18-least-privilege-tool-binding.md) で権限を最小化する。プロンプトはセキュリティ境界ではなく、ガイダンスである。

### 10. 目盛りの根拠を残さない

**症状**: タイムアウト値、リトライ回数、ガードレール閾値を「なんとなく」で設定し、根拠を記録しない。問題発生時に何を変えればよいか分からず、属人化する。

**対策**: [パターンのパラメータ化](decisions/parameterization.md) の作法に従い、各パラメータの値と、それを決めた `[F#]` の根拠を設計文書に記録する。[#32 Agent Trace](patterns/07-observability/32-agent-trace.md) に設定値を含める。

### 11. LLMに算術や厳密検索をやらせる

**症状**: LLMに四則演算、日付計算、正規表現マッチ、データベース検索を直接やらせ、計算ミスや検索漏れが頻発する。

**対策**: [#15 Inverted Structured Output](patterns/03-io-contract/15-inverted-structured-output.md) で LLM には「何を計算/検索するか」の判断だけを出力させ、実際の計算・検索はツールに委譲する。LLMは「考える主体」であり「計算する主体」ではない。
