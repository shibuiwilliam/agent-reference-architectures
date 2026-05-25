# IX. セキュリティ・マルチテナント


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F5]` 入力の信頼度、`[F8]` 説明責任、`[F2]` 失敗コスト
    - **主なダイヤル**: 露出ツール数、ガードレール厳しさ → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

自然言語I/F＝攻撃面、という前提に立った防御層。

- [#41 Tenant-Isolated Agent Runtime｜テナント分離ランタイム](41-tenant-isolated-agent-runtime.md) — テナント毎に実行・記憶を分離
- [#42 Data Boundary Firewall｜データ境界ファイアウォール](42-data-boundary-firewall.md) — 入出力でPII/機密を検査・マスク
- [#43 Confused-Deputy Damage Limitation｜被害限定](43-confused-deputy-damage-limitation.md) — 騙されても被害半径を制限
- [#44 Dual-LLM Privilege Separation｜デュアルLLM権限分離](44-dual-llm-privilege-separation.md) — 隔離LLMと特権LLMを分離
