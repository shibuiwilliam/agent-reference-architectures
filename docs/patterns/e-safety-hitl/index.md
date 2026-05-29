# E. 安全性・HITL・自律性

このドメインのパターン一覧（frontmatter から自動生成）。

| ID | パターン | forces | driving_variables | status |
|---|---|---|---|---|
| E1 | [Risk-based Human Approval｜リスクベース人間承認](e1-risk-based-approval.md) | `[F4, F8, F17]` | `[reversibility, failure_cost]` | stable |
| E2 | [Policy-as-Code Guardrail｜ポリシーのコード化](e2-policy-as-code.md) | `[F14, F16]` | `[failure_cost, accountability]` | stable |
| E3 | [Input/Output Guardrail Sandwich｜入出力ガードレール](e3-guardrail-sandwich.md) | `[F4, F5, F10, F14]` | `[failure_cost, latency_budget]` | stable |
| E4 | [Verified Structured Output｜検証済み構造化出力](e4-verified-structured-output.md) | `[F5, F10]` | `[failure_cost]` | stable |
| E5 | [Autonomy Ladder / Progressive Autonomy｜自律性のはしご](e5-autonomy-ladder.md) | `[F4, F8, F17]` | `[failure_cost, reversibility]` | stable |
