# A. 実行方式・ライフサイクル

このドメインのパターン一覧です（frontmatter から自動生成しています）。

| ID | パターン | forces | driving_variables | status |
|---|---|---|---|---|
| A1 | [Synchronous Edge Agent｜同期エッジ](a1-sync-edge-agent.md) | `[F12]` | `[latency_budget]` | stable |
| A2 | [Durable Async Agent｜耐久非同期セッション](a2-durable-async-agent.md) | `[F1, F7, F15, F17]` | `[reversibility, latency_budget, accountability]` | stable |
| A3 | [Sync Facade over Async Core｜非同期コアの同期ファサード](a3-sync-facade-async-core.md) | `[F1, F12, F7]` | `[latency_budget]` | stable |
| A4 | [Streaming with Progressive Commit｜進捗ストリーミング＋遅延コミット](a4-streaming-progressive-commit.md) | `[F8, F12]` | `[latency_budget, failure_cost]` | stable |
| A6 | [Adaptive Timeout & Budget-Bounded Retry｜適応タイムアウト＋予算律速リトライ](a6-adaptive-timeout-retry.md) | `[F1, F7, F12]` | `[latency_budget, cost_sensitivity, failure_cost]` | stable |
| A7 | [Deadline & Budget Cascade｜期限・予算のカスケード伝播](a7-deadline-budget-cascade.md) | `[F2, F13]` | `[request_value, cost_sensitivity]` | stable |
