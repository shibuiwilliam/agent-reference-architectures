---
title: "パターン早見表（語彙集）"
tags:
  - "パターン"
  - "語彙集"
---

# パターン早見表（語彙集）

!!! abstract "一言"
    59パターンの索引です。パターンは「意思決定の結果として現れる具体構造」であり、詳細は各意思決定ページと `catalog.json` を参照してください。

<!-- BEGIN:GEN:glossary -->

| # | パターン | カテゴリ | 一言要約 | フォース | 関与する決定 | 要素技術 |
|---|---------|---------|---------|---------|------------|---------|
| 1 | **Request-to-Job Gateway** | I. 実行 | 1リクエストを非同期ジョブとして受け付ける | `F4`, `F1` | [二者択一: sync-vs-async](decisions/tradeoffs-catalog/sync-vs-async.md) | FastAPI, Next.js API Routes, SQS … |
| 2 | **Durable Agent Session** | I. 実行 | 状態を永続化し中断・再開に耐える | `F1` | [二者択一: in-context-vs-external](decisions/tradeoffs-catalog/in-context-vs-external.md) | Redis, PostgreSQL, DynamoDB … |
| 3 | **Workflow Backbone + Agent Node** | I. 実行 | 骨格は決定論、判断だけ委譲 | `F6`, `F8` | [二者択一: workflow-vs-agent](decisions/tradeoffs-catalog/workflow-vs-agent.md) | Temporal, Airflow, Step Functions … |
| 4 | **Agent Saga** | I. 実行 | 副作用連鎖を補償で巻き戻す | `F1`, `F2` | [ダイヤル: checkpoint-frequency](decisions/dials/checkpoint-frequency.md) | Temporal, Step Functions, 冪等キー |
| 5 | **Time-Budgeted Agent Loop** | I. 実行 | 時間・回数・コストを予算化し暴走を止める | `F7`, `F3` | [ダイヤル: budget-cap](decisions/dials/budget-cap.md) | フレームワーク callback/middleware, LLM usage API, ツール呼び出しカウンタ |
| 6 | **Interruptible Agent** | I. 実行 | 途中で停止・方針修正できる | `F4` | [フォース: f4-latency-budget](foundations/forces/f4-latency-budget.md) | Redis Pub/Sub, DB flag, WebSocket … |
| 7 | **Streaming Progress** | I. 実行 | 過程を監査可能な要約で逐次表示 | `F4` | [二者択一: push-vs-pull](decisions/tradeoffs-catalog/push-vs-pull.md) | SSE, WebSocket, gRPC streaming … |
| 8 | **Planner-Executor-Reviewer** | II. 構成 | 計画/実行/検証を別ロールに分ける | `F2`, `F3` | [二者択一: plan-vs-react](decisions/tradeoffs-catalog/plan-vs-react.md) | LangGraph, CrewAI, LLM/ルール検証 |
| 9 | **Supervisor & Specialist Agents** | II. 構成 | 統括役が専門役へ委譲する | `F6`, `F7` | [二者択一: single-vs-multi-agent](decisions/tradeoffs-catalog/single-vs-multi-agent.md) | LangGraph conditional routing, OpenAI Swarm, カスタムルーティング |
| 10 | **Agent Ensemble & Debate** | II. 構成 | 複数で解き合議・討論で頑健化 | `F2`, `F3` | [二者択一: same-vs-different-model](decisions/tradeoffs-catalog/same-vs-different-model.md) | 並列 asyncio/thread pool, モデルミックス, 投票/スコアリング |
| 11 | **Deterministic Core, Probabilistic Edge** | II. 構成 | 中核は決定論、周辺だけAI | `F2`, `F8` | [二者択一: prompt-vs-code](decisions/tradeoffs-catalog/prompt-vs-code.md) | Drools/OPA, ルールエンジン, ステートマシン … |
| 12 | **Blackboard** | II. 構成 | 共有黒板で疎結合に協調 | `F6` | [二者択一: orchestration-vs-choreography](decisions/tradeoffs-catalog/orchestration-vs-choreography.md) | Redis, PostgreSQL JSONB, Firebase … |
| 13 | **Natural Language Boundary Adapter** | III. 契約 | 自然言語を構造化意図へ変換 | `F5` | [フォース: f5-input-trust](foundations/forces/f5-input-trust.md) | LLM function calling, Claude tool_use, Rasa … |
| 14 | **Structured Output Contract** | III. 契約 | 出力をスキーマで契約化 | `F8` | [二者択一: structured-vs-freeform](decisions/tradeoffs-catalog/structured-vs-freeform.md) | OpenAI response_format, Anthropic tool_use, Pydantic … |
| 15 | **Inverted Structured Output** | III. 契約 | 最終実行でなく中間判断を出させる | `F2` | [二者択一: llm-vs-tool](decisions/tradeoffs-catalog/llm-vs-tool.md) | Function calling, Enum actions, 決定論的 executor |
| 16 | **Ambiguity Negotiation** | III. 契約 | 曖昧なら確認してから実行 | `F1`, `F2` | [フォース: f1-reversibility](foundations/forces/f1-reversibility.md) | Confidence/logprobs, スロット充填率, インタラクティブUI |
| 17 | **Tool / MCP Gateway** | IV. ツール | ツール接続を集約し認可・監査 | `F5`, `F8` | [二者択一: llm-vs-tool](decisions/tradeoffs-catalog/llm-vs-tool.md) | MCP Gateway/Proxy, Kong, Envoy … |
| 18 | **Least-Privilege Tool Binding** | IV. ツール | セッション毎に最小権限を束縛 | `F5`, `F2` | [ダイヤル: exposed-tool-count](decisions/dials/exposed-tool-count.md) | MCP tools/list フィルタリング, RBAC/ABAC, OPA/Cedar |
| 19 | **Dry-Run First Tool Execution** | IV. ツール | 副作用はまず模擬実行→承認 | `F1`, `F2` | [フォース: f1-reversibility](foundations/forces/f1-reversibility.md) | --dry-run フラグ, DB transaction→result→rollback, API dryRun パラメータ … |
| 20 | **Sandboxed Tool Runtime** | IV. ツール | コード/操作を隔離環境で実行 | `F5` | [フォース: f5-input-trust](foundations/forces/f5-input-trust.md) | Docker gVisor, Firecracker, WASM … |
| 21 | **MCP Adapter Isolation** | IV. ツール | MCPを信頼境界ごとに分離 | `F5`, `F8` | [フォース: f5-input-trust](foundations/forces/f5-input-trust.md) | Kubernetes Pod/Sidecar, Docker Compose, stdio/SSE MCP transport … |
| 22 | **Anti-Corruption Layer** | IV. ツール | レガシーとの概念汚染を防ぐ翻訳層 | `F8` | [フォース: f8-accountability](foundations/forces/f8-accountability.md) | Adapter/Facade パターン, MCP as ACL, Protocol Buffers … |
| 23 | **Layered Memory** | V. メモリ | 短期/長期/共有に記憶を階層化 | `F8` | [二者択一: in-context-vs-external](decisions/tradeoffs-catalog/in-context-vs-external.md) | Redis TTL, PostgreSQL+pgvector, Pinecone … |
| 24 | **Context Pack / Assembly** | V. メモリ | 文脈を組み立てグラウンディング | `F4`, `F7` | [二者択一: rag-vs-finetuning](decisions/tradeoffs-catalog/rag-vs-finetuning.md) | Pinecone, pgvector, Cohere Rerank … |
| 25 | **Memory Write Gate** | V. メモリ | 長期保存を承認制にする | `F8` | [ダイヤル: memory-write-eagerness](decisions/dials/memory-write-eagerness.md) | Presidio, DLP, NER … |
| 26 | **Forgetting and Expiration** | V. メモリ | 記憶に失効・鮮度を持たせる | `F8` | [ダイヤル: memory-ttl](decisions/dials/memory-ttl.md) | Redis TTL, DynamoDB TTL, PostgreSQL パーティションプルーニング … |
| 27 | **Evidence-First Answer** | VI. 信頼性 | 回答前に根拠を取得・引用 | `F8` | [二者択一: rag-vs-finetuning](decisions/tradeoffs-catalog/rag-vs-finetuning.md) | RAGパイプライン, Web検索API, 社内ドキュメントAPI … |
| 28 | **Verifier Agent / Critic** | VI. 信頼性 | 独立した検証器で出荷前検査 | `F2`, `F4` | [二者択一: inline-vs-post-verification](decisions/tradeoffs-catalog/inline-vs-post-verification.md) | 別LLM/ルールチェッカ, ユニットテスト実行, URL検証 … |
| 29 | **Guardrail Sidecar + Self-Correction** | VI. 信頼性 | 入出力検査し誤りを自己修正 | `F5`, `F4` | [二者択一: inline-vs-post-verification](decisions/tradeoffs-catalog/inline-vs-post-verification.md) | Guardrails AI, NeMo Guardrails, LLM-Guard … |
| 30 | **Policy-as-Code Guardrail** | VI. 信頼性 | 制約をコード化し別途判定 | `F2`, `F8` | [二者択一: prompt-vs-code](decisions/tradeoffs-catalog/prompt-vs-code.md) | OPA/Rego, Google CEL, AWS Cedar … |
| 31 | **Human Approval Checkpoint** | VI. 信頼性 | 高リスク前に人間承認 | `F2`, `F1` | [ダイヤル: autonomy-level](decisions/dials/autonomy-level.md) | Durable Session, Slack/Teams/email通知, 承認UIダッシュボード … |
| 32 | **Agent Trace** | VII. 観測 | 全ステップを追記ログ化・再生 | `F8` | [ダイヤル: trace-sampling-rate](decisions/dials/trace-sampling-rate.md) | OpenTelemetry, Langfuse, LangSmith … |
| 33 | **Prompt/Model/Tool Version Pinning** | VII. 観測 | プロンプト/モデル/ツールを固定 | `F8` | [ダイヤル: prompt-storage](decisions/dials/prompt-storage.md) | Git tag+hash, Langfuse Registry, Humanloop … |
| 34 | **Evaluation CI/CD** | VII. 観測 | 変更毎に自動評価で回帰検知 | `F8` | [フォース: f8-accountability](foundations/forces/f8-accountability.md) | promptfoo, Braintrust, Langfuse Eval … |
| 35 | **Production Replay** | VII. 観測 | 本番ログを再生し新旧比較 | `F8`, `F9` | [フォース: f8-accountability](foundations/forces/f8-accountability.md) | BigQuery/ClickHouse抽出, promptfoo/Braintrust replay, LLM-as-Judge … |
| 36 | **Shadow / Canary Deployment** | VII. 観測 | 段階投入と自動ロールバック | `F9` | [フォース: f9-provider-reliability](foundations/forces/f9-provider-reliability.md) | Envoy/Istio/ALB weighted routing, LaunchDarkly, Datadog/Prometheus … |
| 37 | **Semantic Gateway & Cost-Aware Router** | VIII. コスト | 難易度でモデルを動的選択 | `F7`, `F3` | [ダイヤル: model-tier-routing](decisions/dials/model-tier-routing.md) | Martian, Unify, OpenRouter … |
| 38 | **Semantic Result Cache** | VIII. コスト | 意味的に近い結果を再利用 | `F4`, `F7` | [ダイヤル: cache-similarity](decisions/dials/cache-similarity.md) | OpenAI/Cohere Embedding, Redis VSS, Pinecone … |
| 39 | **Prompt Cache Optimized Context** | VIII. コスト | 共通prefixでキャッシュを効かせる | `F7`, `F4` | [フォース: f7-cost-sensitivity](foundations/forces/f7-cost-sensitivity.md) | Anthropic Prompt Caching, OpenAI Automatic, Google Context Caching |
| 40 | **Fallback & Graceful Degradation** | VIII. コスト | 障害時に段階縮退で継続 | `F9` | [二者択一: fail-fast-vs-degradation](decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) | LiteLLM Fallback, Portkey Gateway, resilience4j/Polly … |
| 41 | **Tenant-Isolated Agent Runtime** | IX. セキュリティ | テナント毎に実行・記憶を分離 | `F5`, `F8` | [フォース: f5-input-trust](foundations/forces/f5-input-trust.md) | Kubernetes Namespace, Firecracker, gVisor … |
| 42 | **Data Boundary Firewall** | IX. セキュリティ | 入出力でPII/機密を検査・マスク | `F5`, `F8` | [フォース: f5-input-trust](foundations/forces/f5-input-trust.md) | Presidio, DLP, spaCy NER … |
| 43 | **Confused-Deputy Damage Limitation** | IX. セキュリティ | 騙されても被害半径を制限 | `F5` | [フォース: f5-input-trust](foundations/forces/f5-input-trust.md) | 最小権限, レートリミッタ/金額上限, 承認キュー … |
| 44 | **Dual-LLM Privilege Separation** | IX. セキュリティ | 隔離LLMと特権LLMを分離 | `F5`, `F2` | [フォース: f5-input-trust](foundations/forces/f5-input-trust.md) | 隔離LLM（小型/サンドボックス）, スキーマバリデーション, 特権LLM（ツール実行） |
| 45 | **Agent Runtime Abstraction** | X. デプロイ | 実行基盤を差替可能に | `F9`, `F8` | [二者択一: build-vs-buy](decisions/tradeoffs-catalog/build-vs-buy.md) | Python Protocol/ABC, TypeScript interface, DI (dependency-injector/tsyringe) … |
| 46 | **Model Behavior Compatibility Layer** | X. デプロイ | モデル差を吸収する互換層 | `F9` | [二者択一: single-vs-multi-provider](decisions/tradeoffs-catalog/single-vs-multi-provider.md) | LiteLLM, OpenRouter, AI SDK (Vercel) … |
| 47 | **Agent Capability Registry** | X. デプロイ | 能力・権限・コストを台帳管理 | `F8` | [フォース: f8-accountability](foundations/forces/f8-accountability.md) | PostgreSQL/DynamoDB, etcd/Consul, gRPC/REST … |
| 48 | **Strangler Fig** | X. デプロイ | 既存処理を段階的に置換 | `F2`, `F8` | [フォース: f2-failure-cost](foundations/forces/f2-failure-cost.md) | Feature Flag (LaunchDarkly/Unleash), Production Replay比較, Eval CI/CD … |
| 49 | **Agent Workbench** | XI. UX | 計画/進捗/承認を一画面管理 | `F4` | [フォース: f4-latency-budget](foundations/forces/f4-latency-budget.md) | React/Next.js, SSE/WebSocket, 計画/進捗/成果物/承認パネル |
| 50 | **Editable Plan** | XI. UX | 実行前に計画を人が編集 | `F6` | [二者択一: plan-vs-react](decisions/tradeoffs-catalog/plan-vs-react.md) | JSON/YAMLプラン構造, ドラッグ&ドロップ, インライン編集 … |
| 51 | **Agent-to-Human Escalation** | XI. UX | 自信/権限不足で人間へ引き継ぎ | `F2`, `F4` | [フォース: f2-failure-cost](foundations/forces/f2-failure-cost.md) | 信頼度スコア/self-assess, Slack/Teams/email通知, 構造化コンテキスト引継ぎ … |
| 52 | **Agent Constitution** | XII. ガバナンス | 行動原則を体系的に展開 | `F8`, `F2` | [フォース: f8-accountability](foundations/forces/f8-accountability.md) | YAML/JSON原則階層, Git管理, Jinja2テンプレートエンジン … |
| 53 | **Agent Change Management** | XII. ガバナンス | 変更を厳格なCI/カナリア対象に | `F8`, `F9` | [フォース: f8-accountability](foundations/forces/f8-accountability.md) | Git（プロンプト/ポリシー/設定）, Eval CI/CD回帰, Shadow/Canary段階投入 … |
| 54 | **Tiered (Hot/Cold) Observability** | VII. 観測 | 観測を高速層と安価層に二分 | `F8`, `F7` | [ダイヤル: trace-sampling-rate](decisions/dials/trace-sampling-rate.md) | ClickHouse, Elasticsearch, Prometheus … |
| 55 | **Deadline & Budget Cascade** | I. 実行 | 期限・予算を呼出ツリーへ伝播 | `F7`, `F3` | [ダイヤル: budget-cap](decisions/dials/budget-cap.md) | gRPC metadata, HTTP header context, コンテキストオブジェクト |
| 56 | **Adaptive Effort** | VIII. コスト | 難易度で投入計算量を増減 | `F7`, `F2` | [フォース: f7-cost-sensitivity](foundations/forces/f7-cost-sensitivity.md) | 軽量難易度分類器, Anthropic thinking budget, OpenAI reasoning effort … |
| 57 | **Autonomy Ladder** | VI. 信頼性 | 実績に応じ自律性を段階的に昇格 | `F1`, `F2` | [ダイヤル: autonomy-level](decisions/dials/autonomy-level.md) | Feature Flag (LaunchDarkly/Unleash), 成功/失敗カウンタ, 信頼区間スコアリング |
| 58 | **Sync Facade over Async Core** | I. 実行 | 短ければ同期、超えたら非同期へ昇格 | `F4`, `F1` | [二者択一: sync-vs-async](decisions/tradeoffs-catalog/sync-vs-async.md) | FastAPI asyncio.wait_for, Next.js AbortController |
| 59 | **Workflow–Agent Spectrum Selector** | I. 実行 | サブタスク毎に決定論↔自律を選定 | `F6`, `F2` | [二者択一: workflow-vs-agent](decisions/tradeoffs-catalog/workflow-vs-agent.md) | スコアリングマトリクス, 動的分類器 |

<!-- END:GEN:glossary -->
