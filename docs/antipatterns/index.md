# アンチパターン — よくある設計の落とし穴

| アンチパターン | 何が起きるか | 対処 |
|---|---|---|
| リトライストーム | 障害時に全クライアントが一斉リトライし障害を増幅 | バックオフ＋ジッタ＋サーキットブレーカ、リトライ予算 |
| 全プロンプト観測基盤フル投入 | コスト爆発・PII混入・保持違反 | [G1 二層観測](../patterns/g-observability-ops/g1-tiered-observability.md) |
| 万能マルチエージェント | シングルで足りるのに分割し、コスト/遅延/非決定性/デバッグ困難 | まずシングル（[F-2](../forks/index.md)） |
| 無限/過大タイムアウト | 失敗が隠れリソースが詰まる | 層別タイムアウト＋全体デッドライン（[A7](../patterns/a-execution/a7-deadline-budget-cascade.md)） |
| 過剰ガードレール | 誤検知で正当出力を弾き、自己修正ループが回り続けUX破壊 | block/warn使い分け、ループ上限 |
| 何でも同期/何でも非同期 | 短い処理を非同期化して複雑化、長い処理を同期化してタイムアウト | [A3 同期ファサード](../patterns/a-execution/a3-sync-facade-async-core.md) |
| 最強モデル一択 | 単純クエリにも最上位でコスト破綻 | [B7 ルーター](../patterns/b-orchestration/b7-model-router-adaptive-effort.md) |
| コンテキスト詰め込みすぎ | "lost in the middle" で精度低下・コスト増 | top-k＋リランク＋圧縮（[D2](../patterns/d-memory-context/d2-context-budget-allocator.md)） |
| プロンプトをセキュリティ境界にする | インジェクション/挙動変化で禁止が破れる | [E2 Policy-as-Code](../patterns/e-safety-hitl/e2-policy-as-code.md) ＋ [C1 ゲートウェイ](../patterns/c-tools-security/c1-tool-gateway-mcp-broker.md) |
| 自動メモリの無制限書込 | 記憶汚染で将来の判断が静かに劣化 | [D3 書込ゲート](../patterns/d-memory-context/d3-memory-write-gate.md) ＋ [D1 階層化メモリ](../patterns/d-memory-context/d1-tiered-memory.md)（減衰/失効） |
| 目盛りの根拠を残さない | なぜその値か誰も説明できず、変更が怖くなる | 駆動変数を設計ドキュメント/コードコメントに明記 |
| Excessive Agency | 過剰な権限・自律で被害半径が拡大 | [C1 ゲートウェイ](../patterns/c-tools-security/c1-tool-gateway-mcp-broker.md)（リース）・[A7 予算](../patterns/a-execution/a7-deadline-budget-cascade.md)・[E1 承認](../patterns/e-safety-hitl/e1-risk-based-approval.md) |
