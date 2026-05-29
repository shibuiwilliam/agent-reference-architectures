# G. 観測・評価・運用

このドメインのパターン一覧です（frontmatter から自動生成）。

| ID | パターン | forces | driving_variables | status |
|---|---|---|---|---|
| G1 | [Tiered (Hot/Cold) Observability｜二層観測](g1-tiered-observability.md) | `[F2, F3, F11, F15, F16]` | `[accountability, cost_sensitivity]` | stable |
| G2 | [End-to-End Tracing｜全ホップ分散トレース](g2-end-to-end-tracing.md) | `[F1, F15]` | `[accountability]` | stable |
| G3 | [Shadow & Canary｜影武者とカナリア](g3-shadow-canary.md) | `[F9, F3]` | `[accountability]` | stable |
| G4 | [Eval Harness｜評価ハーネス](g4-eval-harness.md) | `[F3, F4, F9]` | `[accountability, cost_sensitivity]` | stable |
| G5 | [Circuit Breaker, Graded Degradation & Provider Abstraction｜遮断・縮退・抽象化](g5-circuit-breaker-degradation.md) | `[F7, F9, F12]` | `[provider_trust, cost_sensitivity]` | stable |
