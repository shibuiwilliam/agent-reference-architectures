# IX. セキュリティ・マルチテナント


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F5]` 入力の信頼度、`[F8]` 説明責任、`[F2]` 失敗コスト
    - **主なダイヤル**: 露出ツール数、ガードレール厳しさ → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

ユーザーが悪意ある指示をメッセージに忍ばせたり、メール本文に仕込まれた間接プロンプトインジェクションでエージェントが騙されたりする事態は、本番環境では現実の脅威です。自然言語インタフェースがそのまま攻撃面になるという前提に立った防御層を扱います。

- [#41 Tenant-Isolated Agent Runtime｜テナント分離ランタイム](41-tenant-isolated-agent-runtime.md) — テナントごとに実行環境と記憶を分離する
- [#42 Data Boundary Firewall｜データ境界ファイアウォール](42-data-boundary-firewall.md) — 入出力の境界でPII・機密情報を検査・マスクする
- [#43 Confused-Deputy Damage Limitation｜被害限定](43-confused-deputy-damage-limitation.md) — 騙されても被害半径を構造的に制限する
- [#44 Dual-LLM Privilege Separation｜デュアルLLM権限分離](44-dual-llm-privilege-separation.md) — 隔離LLMと特権LLMを分離して権限を制御する
