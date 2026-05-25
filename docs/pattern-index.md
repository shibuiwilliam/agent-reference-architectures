---
title: パターン早見表
---

# パターン早見表（59パターン）

| # | パターン | カテゴリ | 一言 |
|---|---------|---------|------|
| 1 | [Request-to-Job Gateway](patterns/01-execution/01-request-to-job-gateway.md) | I. 実行 | 1リクエストを非同期ジョブとして受け付ける |
| 2 | [Durable Agent Session](patterns/01-execution/02-durable-agent-session.md) | I. 実行 | 状態を永続化し中断・再開に耐える |
| 3 | [Workflow Backbone + Agent Node](patterns/01-execution/03-workflow-backbone-agent-node.md) | I. 実行 | 骨格は決定論、判断だけ委譲 |
| 4 | [Agent Saga](patterns/01-execution/04-agent-saga.md) | I. 実行 | 副作用連鎖を補償で巻き戻す |
| 5 | [Time-Budgeted Agent Loop](patterns/01-execution/05-time-budgeted-agent-loop.md) | I. 実行 | 時間・回数・コストを予算化し暴走を止める |
| 6 | [Interruptible Agent](patterns/01-execution/06-interruptible-agent.md) | I. 実行 | 途中で停止・方針修正できる |
| 7 | [Streaming Progress](patterns/01-execution/07-streaming-progress.md) | I. 実行 | 過程を監査可能な要約で逐次表示 |
| 8 | [Planner-Executor-Reviewer](patterns/02-composition/08-planner-executor-reviewer.md) | II. 構成 | 計画/実行/検証を別ロールに分ける |
| 9 | [Supervisor & Specialist Agents](patterns/02-composition/09-supervisor-specialist-agents.md) | II. 構成 | 統括役が専門役へ委譲する |
| 10 | [Agent Ensemble & Debate](patterns/02-composition/10-agent-ensemble-debate.md) | II. 構成 | 複数で解き合議・討論で頑健化 |
| 11 | [Deterministic Core, Probabilistic Edge](patterns/02-composition/11-deterministic-core-probabilistic-edge.md) | II. 構成 | 中核は決定論、周辺だけAI |
| 12 | [Blackboard](patterns/02-composition/12-blackboard.md) | II. 構成 | 共有黒板で疎結合に協調 |
| 13 | [Natural Language Boundary Adapter](patterns/03-io-contract/13-natural-language-boundary-adapter.md) | III. 契約 | 自然言語を構造化意図へ変換 |
| 14 | [Structured Output Contract](patterns/03-io-contract/14-structured-output-contract.md) | III. 契約 | 出力をスキーマで契約化 |
| 15 | [Inverted Structured Output](patterns/03-io-contract/15-inverted-structured-output.md) | III. 契約 | 最終実行でなく中間判断を出させる |
| 16 | [Ambiguity Negotiation](patterns/03-io-contract/16-ambiguity-negotiation.md) | III. 契約 | 曖昧なら確認してから実行 |
| 17 | [Tool / MCP Gateway](patterns/04-tools-mcp/17-tool-mcp-gateway.md) | IV. ツール | ツール接続を集約し認可・監査 |
| 18 | [Least-Privilege Tool Binding](patterns/04-tools-mcp/18-least-privilege-tool-binding.md) | IV. ツール | セッション毎に最小権限を束縛 |
| 19 | [Dry-Run First Tool Execution](patterns/04-tools-mcp/19-dry-run-first-tool-execution.md) | IV. ツール | 副作用はまず模擬実行→承認 |
| 20 | [Sandboxed Tool Runtime](patterns/04-tools-mcp/20-sandboxed-tool-runtime.md) | IV. ツール | コード/操作を隔離環境で実行 |
| 21 | [MCP Adapter Isolation](patterns/04-tools-mcp/21-mcp-adapter-isolation.md) | IV. ツール | MCPを信頼境界ごとに分離 |
| 22 | [Anti-Corruption Layer](patterns/04-tools-mcp/22-anti-corruption-layer.md) | IV. ツール | レガシーとの概念汚染を防ぐ翻訳層 |
| 23 | [Layered Memory](patterns/05-memory-context/23-layered-memory.md) | V. メモリ | 短期/長期/共有に記憶を階層化 |
| 24 | [Context Pack / Assembly](patterns/05-memory-context/24-context-pack-assembly.md) | V. メモリ | 文脈を組み立てグラウンディング |
| 25 | [Memory Write Gate](patterns/05-memory-context/25-memory-write-gate.md) | V. メモリ | 長期保存を承認制にする |
| 26 | [Forgetting and Expiration](patterns/05-memory-context/26-forgetting-and-expiration.md) | V. メモリ | 記憶に失効・鮮度を持たせる |
| 27 | [Evidence-First Answer](patterns/06-reliability/27-evidence-first-answer.md) | VI. 信頼性 | 回答前に根拠を取得・引用 |
| 28 | [Verifier Agent / Critic](patterns/06-reliability/28-verifier-agent-critic.md) | VI. 信頼性 | 独立した検証器で出荷前検査 |
| 29 | [Guardrail Sidecar + Self-Correction](patterns/06-reliability/29-guardrail-sidecar-self-correction.md) | VI. 信頼性 | 入出力検査し誤りを自己修正 |
| 30 | [Policy-as-Code Guardrail](patterns/06-reliability/30-policy-as-code-guardrail.md) | VI. 信頼性 | 制約をコード化し別途判定 |
| 31 | [Human Approval Checkpoint](patterns/06-reliability/31-human-approval-checkpoint.md) | VI. 信頼性 | 高リスク前に人間承認 |
| 32 | [Agent Trace](patterns/07-observability/32-agent-trace.md) | VII. 観測 | 全ステップを追記ログ化・再生 |
| 33 | [Version Pinning](patterns/07-observability/33-version-pinning.md) | VII. 観測 | プロンプト/モデル/ツールを固定 |
| 34 | [Evaluation CI/CD](patterns/07-observability/34-evaluation-ci-cd.md) | VII. 観測 | 変更毎に自動評価で回帰検知 |
| 35 | [Production Replay](patterns/07-observability/35-production-replay.md) | VII. 観測 | 本番ログを再生し新旧比較 |
| 36 | [Shadow / Canary Deployment](patterns/07-observability/36-shadow-canary-deployment.md) | VII. 観測 | 段階投入と自動ロールバック |
| 37 | [Semantic Gateway & Cost-Aware Router](patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) | VIII. コスト | 難易度でモデルを動的選択 |
| 38 | [Semantic Result Cache](patterns/08-cost-scaling/38-semantic-result-cache.md) | VIII. コスト | 意味的に近い結果を再利用 |
| 39 | [Prompt Cache Optimized Context](patterns/08-cost-scaling/39-prompt-cache-optimized-context.md) | VIII. コスト | 共通prefixでキャッシュを効かせる |
| 40 | [Fallback & Graceful Degradation](patterns/08-cost-scaling/40-fallback-graceful-degradation.md) | VIII. コスト | 障害時に段階縮退で継続 |
| 41 | [Tenant-Isolated Agent Runtime](patterns/09-security/41-tenant-isolated-agent-runtime.md) | IX. セキュリティ | テナント毎に実行・記憶を分離 |
| 42 | [Data Boundary Firewall](patterns/09-security/42-data-boundary-firewall.md) | IX. セキュリティ | 入出力でPII/機密を検査・マスク |
| 43 | [Confused-Deputy Damage Limitation](patterns/09-security/43-confused-deputy-damage-limitation.md) | IX. セキュリティ | 騙されても被害半径を制限 |
| 44 | [Dual-LLM Privilege Separation](patterns/09-security/44-dual-llm-privilege-separation.md) | IX. セキュリティ | 隔離LLMと特権LLMを分離 |
| 45 | [Agent Runtime Abstraction](patterns/10-deployment/45-agent-runtime-abstraction.md) | X. デプロイ | 実行基盤を差替可能に |
| 46 | [Model Behavior Compatibility Layer](patterns/10-deployment/46-model-behavior-compatibility-layer.md) | X. デプロイ | モデル差を吸収する互換層 |
| 47 | [Agent Capability Registry](patterns/10-deployment/47-agent-capability-registry.md) | X. デプロイ | 能力・権限・コストを台帳管理 |
| 48 | [Strangler Fig](patterns/10-deployment/48-strangler-fig.md) | X. デプロイ | 既存処理を段階的に置換 |
| 49 | [Agent Workbench](patterns/11-ux/49-agent-workbench.md) | XI. UX | 計画/進捗/承認を一画面管理 |
| 50 | [Editable Plan](patterns/11-ux/50-editable-plan.md) | XI. UX | 実行前に計画を人が編集 |
| 51 | [Agent-to-Human Escalation](patterns/11-ux/51-agent-to-human-escalation.md) | XI. UX | 自信/権限不足で人間へ引き継ぎ |
| 52 | [Agent Constitution](patterns/12-governance/52-agent-constitution.md) | XII. ガバナンス | 行動原則を体系的に展開 |
| 53 | [Agent Change Management](patterns/12-governance/53-agent-change-management.md) | XII. ガバナンス | 変更を厳格なCI/カナリア対象に |
| 54 | [Tiered (Hot/Cold) Observability](patterns/07-observability/54-tiered-observability.md) | VII. 観測 | 観測を高速層と安価層に二分 |
| 55 | [Deadline & Budget Cascade](patterns/01-execution/55-deadline-budget-cascade.md) | I. 実行 | 期限・予算を呼出ツリーへ伝播 |
| 56 | [Adaptive Effort](patterns/08-cost-scaling/56-adaptive-effort.md) | VIII. コスト | 難易度で投入計算量を増減 |
| 57 | [Autonomy Ladder](patterns/06-reliability/57-autonomy-ladder.md) | VI. 信頼性 | 実績に応じ自律性を段階的に昇格 |
| 58 | [Sync Facade over Async Core](patterns/01-execution/58-sync-facade-over-async-core.md) | I. 実行 | 短ければ同期、超えたら非同期へ昇格 |
| 59 | [Workflow–Agent Spectrum Selector](patterns/01-execution/59-workflow-agent-spectrum-selector.md) | I. 実行 | サブタスク毎に決定論↔自律を選定 |
