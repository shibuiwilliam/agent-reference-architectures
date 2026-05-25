# IV. ツール・MCP・外部システム接続

「考える主体」が外部世界に副作用を起こすための、権限・隔離・冪等性の層。

- [#17 Tool / MCP Gateway｜ツール・MCPゲートウェイ](17-tool-mcp-gateway.md) — ツール接続を集約し認可・監査
- [#18 Least-Privilege Tool Binding｜最小権限バインディング](18-least-privilege-tool-binding.md) — セッション毎に最小権限を束縛
- [#19 Dry-Run First Tool Execution｜ドライラン優先実行](19-dry-run-first-tool-execution.md) — 副作用はまず模擬実行→承認
- [#20 Sandboxed Tool Runtime｜サンドボックス実行](20-sandboxed-tool-runtime.md) — コード/操作を隔離環境で実行
- [#21 MCP Adapter Isolation｜MCPアダプタ分離](21-mcp-adapter-isolation.md) — MCPを信頼境界ごとに分離
- [#22 Anti-Corruption Layer｜アンチコラプション層](22-anti-corruption-layer.md) — レガシーとの概念汚染を防ぐ翻訳層
