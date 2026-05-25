# IV. Tools, MCP & External System Integration


!!! tip "Key decisions for this concern"
    - **Primary Forces**: `[F5]` Input Trustworthiness, `[F8]` Accountability, `[F2]` Failure Cost
    - **Primary Dials**: Exposed Tool Count → [Tuning Dials](../../decisions/tuning-dials.md)
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

As agents handle more tools — search APIs, databases, email sending, file operations — tracking "who called which tool when" becomes difficult, and unintended side effects risk propagating into production environments. This category addresses permissions, isolation, and idempotency when causing side effects in the external world.

- [#17 Tool / MCP Gateway](17-tool-mcp-gateway.md) — Centralize tool connections and manage authorization and auditing in one place
- [#18 Least-Privilege Tool Binding](18-least-privilege-tool-binding.md) — Grant only the minimum necessary permissions per session
- [#19 Dry-Run First Tool Execution](19-dry-run-first-tool-execution.md) — Simulate side-effecting operations first, then execute after approval
- [#20 Sandboxed Tool Runtime](20-sandboxed-tool-runtime.md) — Execute code and operations safely within an isolated environment
- [#21 MCP Adapter Isolation](21-mcp-adapter-isolation.md) — Isolate MCP adapters by trust boundary to prevent lateral movement
- [#22 Anti-Corruption Layer](22-anti-corruption-layer.md) — Introduce a translation layer to prevent concept contamination with legacy systems
