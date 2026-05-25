---
title: AIエージェントの特性
---

# AIエージェントの特性

!!! abstract "一言"
    AIエージェントが従来のソフトウェアと異なる点を整理し、パターンが「何に対する防波堤か」を明確にする。

## なぜ特性を整理するのか

パターンは「問題に対する解」である。そのため、AIエージェントのアーキテクチャパターンを理解するには、まずAIエージェントが本番環境にどのような**新しい壊れ方**を持ち込むのかを把握しておく必要がある。

## 特性一覧

| # | 特性 | 説明 | 主な対応パターン |
|---|------|------|-----------------|
| C1 | **非決定論的な出力** | 同じ入力でも異なる出力を返す。テスト・再現・比較が従来手法では困難 | [#14 Structured Output Contract](../patterns/03-io-contract/14-structured-output-contract.md), [#28 Verifier Agent](../patterns/06-reliability/28-verifier-agent-critic.md), [#34 Evaluation CI/CD](../patterns/07-observability/34-evaluation-ci-cd.md) |
| C2 | **長時間・可変長の実行** | 数秒〜数十分、ステップ数も事前に読めない。HTTPタイムアウトやリソース占有の問題 | [#1 Request-to-Job Gateway](../patterns/01-execution/01-request-to-job-gateway.md), [#5 Time-Budgeted Agent Loop](../patterns/01-execution/05-time-budgeted-agent-loop.md), [#6 Interruptible Agent](../patterns/01-execution/06-interruptible-agent.md) |
| C3 | **外部世界への副作用** | ツール呼び出しでメール送信・DB更新など不可逆な操作を行う | [#4 Agent Saga](../patterns/01-execution/04-agent-saga.md), [#19 Dry-Run First](../patterns/04-tools-mcp/19-dry-run-first-tool-execution.md), [#31 Human Approval Checkpoint](../patterns/06-reliability/31-human-approval-checkpoint.md) |
| C4 | **ハルシネーション** | 事実と異なる情報を自信を持って生成する | [#27 Evidence-First Answer](../patterns/06-reliability/27-evidence-first-answer.md), [#29 Guardrail Sidecar](../patterns/06-reliability/29-guardrail-sidecar-self-correction.md) |
| C5 | **コンテキスト窓の有限性** | 入力長に制限があり、長い会話や大量の文書を一度に扱えない | [#23 Layered Memory](../patterns/05-memory-context/23-layered-memory.md), [#24 Context Pack](../patterns/05-memory-context/24-context-pack-assembly.md), [#26 Forgetting and Expiration](../patterns/05-memory-context/26-forgetting-and-expiration.md) |
| C6 | **外部LLMへの依存** | 推論エンジンが外部サービス。レイテンシ・可用性・価格が自社で制御できない | [#37 Semantic Gateway](../patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md), [#40 Fallback](../patterns/08-cost-scaling/40-fallback-graceful-degradation.md), [#45 Agent Runtime Abstraction](../patterns/10-deployment/45-agent-runtime-abstraction.md) |
| C7 | **自然言語インターフェース＝攻撃面** | プロンプトインジェクション・データ漏洩など新しい攻撃ベクトル | [#42 Data Boundary Firewall](../patterns/09-security/42-data-boundary-firewall.md), [#43 Confused-Deputy](../patterns/09-security/43-confused-deputy-damage-limitation.md), [#44 Dual-LLM Privilege Separation](../patterns/09-security/44-dual-llm-privilege-separation.md) |
| C8 | **コストが入力/出力量に比例** | トークン課金のため、使い方次第でコストが桁違いに変動する | [#38 Semantic Result Cache](../patterns/08-cost-scaling/38-semantic-result-cache.md), [#39 Prompt Cache](../patterns/08-cost-scaling/39-prompt-cache-optimized-context.md), [#56 Adaptive Effort](../patterns/08-cost-scaling/56-adaptive-effort.md) |
| C9 | **挙動変更＝モデル更新** | コード変更なしにモデル更新で挙動が変わる。従来のCI/CDでは検知できない | [#33 Version Pinning](../patterns/07-observability/33-version-pinning.md), [#35 Production Replay](../patterns/07-observability/35-production-replay.md), [#36 Shadow/Canary Deployment](../patterns/07-observability/36-shadow-canary-deployment.md) |

## 特性と駆動変数の関係

各特性がどの程度のリスクになるかは、システムの文脈——すなわち [駆動変数（フォース）](forces.md) によって決まる。たとえば「非決定論的な出力」(C1) は、失敗コスト `[F2]` が高い医療・金融の領域では致命的になりうるが、レコメンドのように `[F2]` が低い場面では許容範囲となる。

パターンは特性に対する汎用的な防波堤であるが、どのパターンをどの程度適用するかは駆動変数によって決まる。こうした判断を助けるのが [意思決定層](../decisions/tuning-dials.md) である。
