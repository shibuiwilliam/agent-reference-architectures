# 機械可読パターンインデックス

全パターンの frontmatter メタを1表に集約（`scripts/gen_indexes.py` で自動生成）。
コーディングエージェントはこの表から候補を絞り、各 `.md` を読みに行くとよい。

| ID | パターン | domain | forces | driving_variables | forks | status |
|---|---|---|---|---|---|---|
| A1 | [Synchronous Edge Agent｜同期エッジ](../patterns/a-execution/a1-sync-edge-agent.md) | a-execution | `[F12]` | `[latency_budget]` | `` | stable |
| A2 | [Durable Async Agent｜耐久非同期セッション](../patterns/a-execution/a2-durable-async-agent.md) | a-execution | `[F1, F7, F15, F17]` | `[reversibility, latency_budget, accountability]` | `` | stable |
| A3 | [Sync Facade over Async Core｜非同期コアの同期ファサード](../patterns/a-execution/a3-sync-facade-async-core.md) | a-execution | `[F1, F12, F7]` | `[latency_budget]` | `` | stable |
| A4 | [Streaming with Progressive Commit｜進捗ストリーミング＋遅延コミット](../patterns/a-execution/a4-streaming-progressive-commit.md) | a-execution | `[F8, F12]` | `[latency_budget, failure_cost]` | `` | stable |
| A6 | [Adaptive Timeout & Budget-Bounded Retry｜適応タイムアウト＋予算律速リトライ](../patterns/a-execution/a6-adaptive-timeout-retry.md) | a-execution | `[F1, F7, F12]` | `[latency_budget, cost_sensitivity, failure_cost]` | `` | stable |
| A7 | [Deadline & Budget Cascade｜期限・予算のカスケード伝播](../patterns/a-execution/a7-deadline-budget-cascade.md) | a-execution | `[F2, F13]` | `[request_value, cost_sensitivity]` | `[]` | stable |
| B1 | [Deterministic Shell, Probabilistic Core｜決定論的な殻・確率的な核](../patterns/b-orchestration/b1-deterministic-shell.md) | b-orchestration | `[F3, F16]` | `[failure_cost, task_variability, accountability]` | `` | stable |
| B2 | [Workflow Backbone with Agentic Nodes｜骨格固定・ノード単位で自律度選定](../patterns/b-orchestration/b2-workflow-backbone.md) | b-orchestration | `[F3, F10, F13]` | `[task_variability, failure_cost]` | `` | stable |
| B3 | [Agentic Loop with Budget｜予算付き自律ループ](../patterns/b-orchestration/b3-agentic-loop-budget.md) | b-orchestration | `[F13, F2]` | `[task_variability, cost_sensitivity]` | `` | stable |
| B4 | [Planner-Executor-Verifier｜計画・実行・検証の分離](../patterns/b-orchestration/b4-planner-executor-verifier.md) | b-orchestration | `[F2, F4, F13]` | `[failure_cost, task_variability]` | `` | stable |
| B5 | [Supervisor-Worker｜中央オーケストレーション](../patterns/b-orchestration/b5-supervisor-worker.md) | b-orchestration | `[F6, F13, F15]` | `[task_variability, cost_sensitivity]` | `` | stable |
| B6 | [Critic/Judge & Sampling-Aggregation｜独立検証と多数決](../patterns/b-orchestration/b6-critic-judge-sampling.md) | b-orchestration | `[F3, F4]` | `[request_value, failure_cost]` | `` | stable |
| B7 | [Model Router & Adaptive Effort｜モデル段階化と適応的努力配分](../patterns/b-orchestration/b7-model-router-adaptive-effort.md) | b-orchestration | `[F2, F12]` | `[cost_sensitivity, request_value]` | `` | stable |
| C1 | [Tool Gateway / MCP Broker｜ツールゲートウェイ・MCP仲介](../patterns/c-tools-security/c1-tool-gateway-mcp-broker.md) | c-tools-security | `[F8, F14, F16]` | `[input_trust, accountability]` | `` | stable |
| C2 | [Read-Free / Write-Gated｜読取自由・書込ゲート](../patterns/c-tools-security/c2-read-free-write-gated.md) | c-tools-security | `[F8]` | `[reversibility, failure_cost]` | `` | stable |
| C3 | [Dry-run & Commit / Plan-then-Apply｜差分提示してから実行](../patterns/c-tools-security/c3-dry-run-commit.md) | c-tools-security | `[F4, F8]` | `[reversibility, failure_cost]` | `` | stable |
| C4 | [Idempotent Command Envelope｜冪等コマンド包装](../patterns/c-tools-security/c4-idempotent-command-envelope.md) | c-tools-security | `[F3, F8]` | `[reversibility]` | `` | stable |
| C5 | [Capability Lease｜短命権限チケット](../patterns/c-tools-security/c5-capability-lease.md) | c-tools-security | `[F8, F14]` | `[input_trust]` | `` | stable |
| C6 | [Confused Deputy Defense｜代理の混同防御](../patterns/c-tools-security/c6-confused-deputy-defense.md) | c-tools-security | `[F14, F5]` | `[input_trust]` | `` | stable |
| C7 | [Sandboxed Execution｜隔離実行](../patterns/c-tools-security/c7-sandboxed-execution.md) | c-tools-security | `[F14]` | `[input_trust]` | `` | stable |
| C8 | [Saga / Compensation｜補償トランザクション](../patterns/c-tools-security/c8-saga-compensation.md) | c-tools-security | `[F3, F8]` | `[reversibility]` | `` | stable |
| D1 | [Tiered Memory｜階層化メモリ](../patterns/d-memory-context/d1-tiered-memory.md) | d-memory-context | `[F4, F6]` | `[failure_cost]` | `` | stable |
| D2 | [Context Budget Allocator｜コンテキスト予算配分](../patterns/d-memory-context/d2-context-budget-allocator.md) | d-memory-context | `[F6, F11]` | `[cost_sensitivity]` | `` | stable |
| D3 | [Memory Write Gate / Quarantine｜メモリ書込ゲート](../patterns/d-memory-context/d3-memory-write-gate.md) | d-memory-context | `[F6, F4, F14]` | `[input_trust, failure_cost]` | `` | stable |
| D4 | [Memory Decay & Versioned Truth｜記憶の減衰とバージョン管理](../patterns/d-memory-context/d4-memory-decay-versioned-truth.md) | d-memory-context | `[F6]` | `[failure_cost]` | `[]` | stable |
| D5 | [Prompt Registry / Prompt Artifact｜プロンプトの成果物化](../patterns/d-memory-context/d5-prompt-registry.md) | d-memory-context | `[F9, F16]` | `[accountability]` | `[]` | stable |
| D6 | [Semantic Cache with No-Cache Zones｜禁止領域付きキャッシュ](../patterns/d-memory-context/d6-semantic-cache-nocache-zones.md) | d-memory-context | `[F2, F11]` | `[cost_sensitivity, failure_cost]` | `[]` | stable |
| E1 | [Risk-based Human Approval｜リスクベース人間承認](../patterns/e-safety-hitl/e1-risk-based-approval.md) | e-safety-hitl | `[F4, F8, F17]` | `[reversibility, failure_cost]` | `` | stable |
| E2 | [Policy-as-Code Guardrail｜ポリシーのコード化](../patterns/e-safety-hitl/e2-policy-as-code.md) | e-safety-hitl | `[F14, F16]` | `[failure_cost, accountability]` | `` | stable |
| E3 | [Input/Output Guardrail Sandwich｜入出力ガードレール](../patterns/e-safety-hitl/e3-guardrail-sandwich.md) | e-safety-hitl | `[F4, F5, F10, F14]` | `[failure_cost, latency_budget]` | `` | stable |
| E4 | [Verified Structured Output｜検証済み構造化出力](../patterns/e-safety-hitl/e4-verified-structured-output.md) | e-safety-hitl | `[F5, F10]` | `[failure_cost]` | `` | stable |
| E5 | [Autonomy Ladder / Progressive Autonomy｜自律性のはしご](../patterns/e-safety-hitl/e5-autonomy-ladder.md) | e-safety-hitl | `[F4, F8, F17]` | `[failure_cost, reversibility]` | `` | stable |
| F1 | [Short DB Transaction, Long Agent Session｜長セッション・短トランザクション](../patterns/f-data-integrity/f1-short-tx-long-session.md) | f-data-integrity | `[F1, F3]` | `[reversibility]` | `` | stable |
| F2 | [Event-sourced / Replayable Runs｜イベントソーシングとリプレイ](../patterns/f-data-integrity/f2-event-sourced-replayable.md) | f-data-integrity | `[F3, F15, F16]` | `[accountability]` | `[]` | stable |
| G1 | [Tiered (Hot/Cold) Observability｜二層観測](../patterns/g-observability-ops/g1-tiered-observability.md) | g-observability-ops | `[F2, F3, F11, F15, F16]` | `[accountability, cost_sensitivity]` | `[]` | stable |
| G2 | [End-to-End Tracing｜全ホップ分散トレース](../patterns/g-observability-ops/g2-end-to-end-tracing.md) | g-observability-ops | `[F1, F15]` | `[accountability]` | `[]` | stable |
| G3 | [Shadow & Canary｜影武者とカナリア](../patterns/g-observability-ops/g3-shadow-canary.md) | g-observability-ops | `[F9, F3]` | `[accountability]` | `[]` | stable |
| G4 | [Eval Harness｜評価ハーネス](../patterns/g-observability-ops/g4-eval-harness.md) | g-observability-ops | `[F3, F4, F9]` | `[accountability, cost_sensitivity]` | `[]` | stable |
| G5 | [Circuit Breaker, Graded Degradation & Provider Abstraction｜遮断・縮退・抽象化](../patterns/g-observability-ops/g5-circuit-breaker-degradation.md) | g-observability-ops | `[F7, F9, F12]` | `[provider_trust, cost_sensitivity]` | `` | stable |
