# C. ツール・副作用・セキュリティ

このドメインのパターン一覧（frontmatter から自動生成）。

| ID | パターン | forces | driving_variables | status |
|---|---|---|---|---|
| C1 | [Tool Gateway / MCP Broker｜ツールゲートウェイ・MCP仲介](c1-tool-gateway-mcp-broker.md) | `[F8, F14, F16]` | `[input_trust, accountability]` | stable |
| C2 | [Read-Free / Write-Gated｜読取自由・書込ゲート](c2-read-free-write-gated.md) | `[F8]` | `[reversibility, failure_cost]` | stable |
| C3 | [Dry-run & Commit / Plan-then-Apply｜差分提示してから実行](c3-dry-run-commit.md) | `[F4, F8]` | `[reversibility, failure_cost]` | stable |
| C4 | [Idempotent Command Envelope｜冪等コマンド包装](c4-idempotent-command-envelope.md) | `[F3, F8]` | `[reversibility]` | stable |
| C6 | [Confused Deputy Defense｜代理の混同防御](c6-confused-deputy-defense.md) | `[F14, F5]` | `[input_trust]` | stable |
