# B. オーケストレーション・制御フロー

このドメインのパターン一覧（frontmatter から自動生成）。

| ID | パターン | forces | driving_variables | status |
|---|---|---|---|---|
| B1 | [Deterministic Shell, Probabilistic Core｜決定論的な殻・確率的な核](b1-deterministic-shell.md) | `[F3, F16]` | `[failure_cost, task_variability, accountability]` | stable |
| B2 | [Workflow Backbone with Agentic Nodes｜骨格固定・ノード単位で自律度選定](b2-workflow-backbone.md) | `[F3, F10, F13]` | `[task_variability, failure_cost]` | stable |
| B3 | [Agentic Loop with Budget｜予算付き自律ループ](b3-agentic-loop-budget.md) | `[F13, F2, F6]` | `[task_variability, cost_sensitivity]` | stable |
| B4 | [Planner-Executor-Verifier｜計画・実行・検証の分離](b4-planner-executor-verifier.md) | `[F2, F4, F13]` | `[failure_cost, task_variability]` | stable |
| B6 | [Critic/Judge & Sampling-Aggregation｜独立検証と多数決](b6-critic-judge-sampling.md) | `[F3, F4]` | `[request_value, failure_cost]` | stable |
| B7 | [Model Router & Adaptive Effort｜モデル段階化と適応的努力配分](b7-model-router-adaptive-effort.md) | `[F2, F12]` | `[cost_sensitivity, request_value]` | stable |
