# パターン・カタログ（A–G）

各パターンは「定数」ではなく**パラメータ付き関数**です。同じパターンでも [駆動変数](../concepts/driving-variables.md) が違えば目盛りが変わります。各ページの frontmatter には `forces / driving_variables / forks / related_patterns / alternatives` の機械可読メタが含まれています（[機械可読インデックス](../reference/pattern-index.md) に集約）。

- 記述様式は [テンプレート](_template.md) を参照してください。
- 採否は各ページの「選定条件（When to use / When NOT）」で判定してください。

| ドメイン | テーマ |
|---|---|
| [A 実行方式](a-execution/index.md) | 同期/非同期・タイムアウト・予算・ストリーミング |
| [B オーケストレーション](b-orchestration/index.md) | 決定論↔自律・計画/実行/検証・ルーティング |
| [C ツール・セキュリティ](c-tools-security/index.md) | ゲートウェイ・冪等・ドライラン・権限・隔離 |
| [D メモリ・コンテキスト](d-memory-context/index.md) | 階層化・予算配分・書込ゲート・減衰・登録 |
| [E 安全性・HITL](e-safety-hitl/index.md) | 承認・ポリシー・ガードレール・構造化出力・自律ラダー |
| [F データ整合性](f-data-integrity/index.md) | 短トランザクション・イベントソーシング |
| [G 観測・運用](g-observability-ops/index.md) | 二層観測・トレース・カナリア・評価・縮退 |
