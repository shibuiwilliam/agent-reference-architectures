# IV. ツール・MCP・外部システム接続


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F5]` 入力の信頼度、`[F8]` 説明責任、`[F2]` 失敗コスト
    - **主なダイヤル**: 露出ツール数 → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

「考える主体」が外部世界に副作用を起こすための、権限・隔離・冪等性を扱う層である。

- [#17 Tool / MCP Gateway｜ツール・MCPゲートウェイ](17-tool-mcp-gateway.md) — ツール接続を一箇所に集約し、認可・監査を一元管理する
- [#18 Least-Privilege Tool Binding｜最小権限バインディング](18-least-privilege-tool-binding.md) — セッションごとに必要最小限の権限だけを付与する
- [#19 Dry-Run First Tool Execution｜ドライラン優先実行](19-dry-run-first-tool-execution.md) — 副作用のある操作はまず模擬実行し、承認を得てから本実行する
- [#20 Sandboxed Tool Runtime｜サンドボックス実行](20-sandboxed-tool-runtime.md) — コードや操作を隔離環境の中で安全に実行する
- [#21 MCP Adapter Isolation｜MCPアダプタ分離](21-mcp-adapter-isolation.md) — MCPアダプタを信頼境界ごとに分離して横展開を防ぐ
- [#22 Anti-Corruption Layer｜アンチコラプション層](22-anti-corruption-layer.md) — レガシーシステムとの概念汚染を防ぐ翻訳層を設ける
