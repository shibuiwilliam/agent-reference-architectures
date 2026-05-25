# III. Input/Output & Contracts


!!! tip "Key decisions for this concern"
    - **Primary Forces**: `[F5]` Input Trustworthiness, `[F8]` Accountability, `[F2]` Failure Cost
    - **Primary Tradeoffs**: Structured ↔ Free-form Output, LLM Reasoning ↔ Tool Delegation → [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

LLM inputs are ambiguous natural language, and outputs are probabilistic text that varies subtly each time. These patterns handle the boundary that converts these into "contracts" that existing software can safely exchange.

- [#13 Natural Language Boundary Adapter](13-natural-language-boundary-adapter.md) — Convert natural language into structured intent representations
- [#14 Structured Output Contract](14-structured-output-contract.md) — Contractualize LLM output with schemas
- [#15 Inverted Structured Output](15-inverted-structured-output.md) — Have the LLM output intermediate decisions rather than final execution
- [#16 Ambiguity Negotiation](16-ambiguity-negotiation.md) — When input is ambiguous, confirm before executing
