---
title: 相反する仕組みの選定基準
---

# 相反する仕組みの選定基準

!!! abstract "一言"
    「A か B か」で迷ったとき、駆動変数 `[F#]` で判断する二者択一カタログ。

## 相反とは

あるパターンを選ぶと、別のパターンが排他的になる（あるいはトレードオフが生じる）場面がある。どちらが正しいかは文脈——[駆動変数](../foundations/forces.md) の値域——で決まる。このページは主要な二者択一を一覧し、判断の入り口を示す。

## 二者択一カタログ

| 選択肢 A | 選択肢 B | 決定変数 | デフォルト（迷ったら） | ハイブリッド | 関連パターン |
|----------|----------|---------|---------------------|-------------|-------------|
| **同期処理** | **非同期処理** | `[F4]` レイテンシ予算、`[F1]` 可逆性 | 数秒以内なら同期、超えたら非同期 | [#58 Sync Facade](../patterns/01-execution/58-sync-facade-over-async-core.md): 短ければ同期、超えたら昇格 | [#1 Gateway](../patterns/01-execution/01-request-to-job-gateway.md) |
| **シングルエージェント** | **マルチエージェント** | `[F6]` タスク変動性、`[F7]` コスト感度 | シングルで十分ならシングル | タスク分解でサブタスク毎に判断 | [#9 Supervisor](../patterns/02-composition/09-supervisor-specialist-agents.md), [#59 Spectrum Selector](../patterns/01-execution/59-workflow-agent-spectrum-selector.md) |
| **中央集権オーケストレーション** | **コレオグラフィ（自律協調）** | `[F8]` 説明責任、`[F6]` タスク変動性 | 中央集権（監査・制御が容易） | [#3 Workflow Backbone](../patterns/01-execution/03-workflow-backbone-agent-node.md): 骨格は中央、ノードは自律 | [#12 Blackboard](../patterns/02-composition/12-blackboard.md) |
| **ワークフロー（決定論的）** | **エージェント（自律的）** | `[F6]` タスク変動性、`[F2]` 失敗コスト | 定型はワークフロー、探索はエージェント | [#59 Spectrum Selector](../patterns/01-execution/59-workflow-agent-spectrum-selector.md): サブタスク毎に選定 | [#3 Workflow Backbone](../patterns/01-execution/03-workflow-backbone-agent-node.md), [#11 Deterministic Core](../patterns/02-composition/11-deterministic-core-probabilistic-edge.md) |
| **Plan（計画先行）** | **ReAct（逐次行動）** | `[F2]` 失敗コスト、`[F6]` タスク変動性 | 副作用が大きいなら Plan | Plan + ReAct: 計画後に各ステップでReAct | [#8 Planner-Executor-Reviewer](../patterns/02-composition/08-planner-executor-reviewer.md), [#50 Editable Plan](../patterns/11-ux/50-editable-plan.md) |
| **プロンプト制御** | **コード制御** | `[F8]` 説明責任、`[F6]` タスク変動性 | コード制御（テスト・バージョン管理可） | 判断はプロンプト、フローはコード | [#30 Policy-as-Code](../patterns/06-reliability/30-policy-as-code-guardrail.md), [#11 Deterministic Core](../patterns/02-composition/11-deterministic-core-probabilistic-edge.md) |
| **RAG（検索拡張生成）** | **Fine-Tuning / ロングコンテキスト** | `[F7]` コスト感度、`[F4]` レイテンシ予算 | RAG（更新容易・コスト予測可） | RAG + FT: ドメイン知識はFT、最新情報はRAG | [#24 Context Pack](../patterns/05-memory-context/24-context-pack-assembly.md), [#27 Evidence-First](../patterns/06-reliability/27-evidence-first-answer.md) |
| **単一プロバイダ** | **マルチプロバイダ** | `[F9]` プロバイダ信頼度、`[F7]` コスト感度 | 単一で始め、障害実績で複数化 | [#40 Fallback](../patterns/08-cost-scaling/40-fallback-graceful-degradation.md): プライマリ＋フォールバック | [#45 Runtime Abstraction](../patterns/10-deployment/45-agent-runtime-abstraction.md) |
| **インライン検証** | **事後検証** | `[F4]` レイテンシ予算、`[F2]` 失敗コスト | 高リスクはインライン、低リスクは事後 | インライン（軽量）+ 事後（詳細） | [#28 Verifier Agent](../patterns/06-reliability/28-verifier-agent-critic.md), [#29 Guardrail Sidecar](../patterns/06-reliability/29-guardrail-sidecar-self-correction.md) |
| **同一モデルで検証** | **別モデルで検証** | `[F2]` 失敗コスト、`[F7]` コスト感度 | 同一（低コスト）、高リスクなら別モデル | 同一で初期検証、別モデルで最終検証 | [#28 Verifier Agent](../patterns/06-reliability/28-verifier-agent-critic.md), [#44 Dual-LLM](../patterns/09-security/44-dual-llm-privilege-separation.md) |
| **LLM推論で判断** | **ツール委譲（計算・検索）** | `[F2]` 失敗コスト | 算術・厳密検索はツール委譲 | LLMで方針決定→ツールで実行 | [#15 Inverted Structured Output](../patterns/03-io-contract/15-inverted-structured-output.md), [#17 Tool Gateway](../patterns/04-tools-mcp/17-tool-mcp-gateway.md) |
| **Fail-fast（即時失敗）** | **縮退運転（Graceful Degradation）** | `[F9]` プロバイダ信頼度、`[F3]` リクエスト価値 | 低価値はfail-fast、高価値は縮退 | 段階縮退: 最高品質→簡易回答→静的応答 | [#40 Fallback](../patterns/08-cost-scaling/40-fallback-graceful-degradation.md) |
| **プッシュ（SSE/Webhook）** | **プル（ポーリング）** | `[F4]` レイテンシ予算、`[F7]` コスト感度 | プッシュ（リアルタイム性） | プッシュ＋ポーリング（フォールバック） | [#7 Streaming Progress](../patterns/01-execution/07-streaming-progress.md) |
| **文脈内状態（in-context）** | **外部状態（external store）** | `[F4]` レイテンシ予算、`[F8]` 説明責任 | 短期はin-context、永続は外部 | in-context（作業用）+ 外部（永続・監査） | [#23 Layered Memory](../patterns/05-memory-context/23-layered-memory.md), [#2 Durable Session](../patterns/01-execution/02-durable-agent-session.md) |
| **ビルド（自社構築）** | **バイ（既製品利用）** | `[F8]` 説明責任、`[F7]` コスト感度 | 差別化要素はビルド、汎用はバイ | コア自社構築＋周辺は既製品 | [#45 Runtime Abstraction](../patterns/10-deployment/45-agent-runtime-abstraction.md), [#48 Strangler Fig](../patterns/10-deployment/48-strangler-fig.md) |
| **構造化出力の強制** | **自由形式出力** | `[F8]` 説明責任、`[F6]` タスク変動性 | 下流システム連携は構造化 | 判断は構造化、ユーザー向け説明は自由 | [#14 Structured Output](../patterns/03-io-contract/14-structured-output-contract.md), [#15 Inverted](../patterns/03-io-contract/15-inverted-structured-output.md) |

## 使い方

1. 設計上の二者択一に直面したら、上表で該当行を探す
2. 「決定変数」列のフォースを自システムで評価する
3. 「デフォルト」を出発点に、「ハイブリッド」が適用可能かを検討する
4. 選定理由を [#32 Agent Trace](../patterns/07-observability/32-agent-trace.md) や設計文書に記録する

相反の選定は一度きりの判断ではない。フォースの値域が変わったら（規制強化、スケール増大など）再評価する。→ [パターンのパラメータ化](parameterization.md)
