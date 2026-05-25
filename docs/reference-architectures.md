---
title: リファレンスアーキテクチャ
---

# リファレンスアーキテクチャ

!!! abstract "一言"
    個別パターンを**層として重ねた複合構成**の例。「何から始めるか」の出発点として使う。

## パターンの重ね方

個別パターンは単独でも有用であるが、本番システムでは複数のパターンを組み合わせて使うことが多い。以下に、典型的なユースケース別の複合構成を示す。

各構成には「このパターンを採用する理由」と「省略してよい条件」を併記している。全てを一度に導入する必要はなく、最小構成から始めて、[駆動変数](foundations/forces.md) の変化に応じて層を追加していくのがよい。

---

## 1. 最小構成（MVP）

**想定**: 社内ツール・プロトタイプ。`[F2]` 失敗コスト低、`[F8]` 説明責任低。

| 層 | パターン | 役割 |
|---|---------|------|
| 受付 | [#1 Request-to-Job Gateway](patterns/01-execution/01-request-to-job-gateway.md) | 非同期化でタイムアウト回避 |
| 状態 | [#2 Durable Agent Session](patterns/01-execution/02-durable-agent-session.md) | 中断・再開 |
| 出力 | [#14 Structured Output Contract](patterns/03-io-contract/14-structured-output-contract.md) | 下流システムとの接続 |
| 観測 | [#32 Agent Trace](patterns/07-observability/32-agent-trace.md) | 最低限のデバッグ情報 |

**省略可**: ガードレール、マルチエージェント、コスト最適化。

---

## 2. 副作用重視構成

**想定**: メール送信・決済・DB更新など不可逆な操作を含む。`[F1]` 可逆性低、`[F2]` 失敗コスト高。

| 層 | パターン | 役割 |
|---|---------|------|
| 受付 | [#1 Request-to-Job Gateway](patterns/01-execution/01-request-to-job-gateway.md) | 非同期受付 |
| 骨格 | [#3 Workflow Backbone + Agent Node](patterns/01-execution/03-workflow-backbone-agent-node.md) | 決定論的なフロー制御 |
| 補償 | [#4 Agent Saga](patterns/01-execution/04-agent-saga.md) | 失敗時の巻き戻し |
| 承認 | [#31 Human Approval Checkpoint](patterns/06-reliability/31-human-approval-checkpoint.md) | 高リスク操作前の人間承認 |
| ツール | [#19 Dry-Run First Tool Execution](patterns/04-tools-mcp/19-dry-run-first-tool-execution.md) | 副作用の模擬実行 |
| 出力 | [#15 Inverted Structured Output](patterns/03-io-contract/15-inverted-structured-output.md) | LLMは判断のみ、実行はコード |
| 観測 | [#32 Agent Trace](patterns/07-observability/32-agent-trace.md) | 全操作の追跡 |

---

## 3. 信頼できない入力構成

**想定**: 不特定ユーザーからの自然言語入力を処理する。`[F5]` 入力信頼度低。

| 層 | パターン | 役割 |
|---|---------|------|
| 境界 | [#13 Natural Language Boundary Adapter](patterns/03-io-contract/13-natural-language-boundary-adapter.md) | 入力の構造化 |
| 検査 | [#42 Data Boundary Firewall](patterns/09-security/42-data-boundary-firewall.md) | PII/インジェクション検査 |
| 分離 | [#44 Dual-LLM Privilege Separation](patterns/09-security/44-dual-llm-privilege-separation.md) | 隔離LLMと特権LLMの分離 |
| 権限 | [#18 Least-Privilege Tool Binding](patterns/04-tools-mcp/18-least-privilege-tool-binding.md) | 最小権限 |
| 被害限定 | [#43 Confused-Deputy Damage Limitation](patterns/09-security/43-confused-deputy-damage-limitation.md) | 被害半径の制限 |
| ガードレール | [#29 Guardrail Sidecar + Self-Correction](patterns/06-reliability/29-guardrail-sidecar-self-correction.md) | 出力検査 |

---

## 4. 事実性重視構成

**想定**: 医療・法務・金融など、ハルシネーションが許されない。`[F2]` 失敗コスト高、`[F8]` 説明責任高。

| 層 | パターン | 役割 |
|---|---------|------|
| 根拠 | [#27 Evidence-First Answer](patterns/06-reliability/27-evidence-first-answer.md) | 回答前に根拠取得 |
| 検証 | [#28 Verifier Agent / Critic](patterns/06-reliability/28-verifier-agent-critic.md) | 独立した事実検証 |
| 合議 | [#10 Agent Ensemble & Debate](patterns/02-composition/10-agent-ensemble-debate.md) | 複数モデルの合議 |
| 契約 | [#14 Structured Output Contract](patterns/03-io-contract/14-structured-output-contract.md) | 出力の構造化・引用付き |
| ポリシー | [#30 Policy-as-Code Guardrail](patterns/06-reliability/30-policy-as-code-guardrail.md) | 規制準拠の自動検査 |
| 観測 | [#32 Agent Trace](patterns/07-observability/32-agent-trace.md) + [#33 Version Pinning](patterns/07-observability/33-version-pinning.md) | 完全な監査証跡 |

---

## 5. コスト重視構成

**想定**: 大量リクエストを低コストで処理する。`[F7]` コスト感度高。

| 層 | パターン | 役割 |
|---|---------|------|
| ルーティング | [#37 Semantic Gateway & Cost-Aware Router](patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) | 難易度別モデル振り分け |
| キャッシュ | [#38 Semantic Result Cache](patterns/08-cost-scaling/38-semantic-result-cache.md) | 類似クエリの再利用 |
| プロンプト | [#39 Prompt Cache Optimized Context](patterns/08-cost-scaling/39-prompt-cache-optimized-context.md) | prefix共有でキャッシュ |
| 努力配分 | [#56 Adaptive Effort](patterns/08-cost-scaling/56-adaptive-effort.md) | 難易度で計算量調整 |
| 予算 | [#5 Time-Budgeted Agent Loop](patterns/01-execution/05-time-budgeted-agent-loop.md) | リクエスト単位の上限 |
| フォールバック | [#40 Fallback & Graceful Degradation](patterns/08-cost-scaling/40-fallback-graceful-degradation.md) | 障害時の縮退 |

---

## 6. 継続改善運用構成

**想定**: 本番稼働後の品質維持・改善サイクル。`[F8]` 説明責任高。

| 層 | パターン | 役割 |
|---|---------|------|
| 固定 | [#33 Version Pinning](patterns/07-observability/33-version-pinning.md) | 再現可能性の確保 |
| 評価 | [#34 Evaluation CI/CD](patterns/07-observability/34-evaluation-ci-cd.md) | 変更毎の自動回帰検知 |
| リプレイ | [#35 Production Replay](patterns/07-observability/35-production-replay.md) | 新旧比較 |
| デプロイ | [#36 Shadow / Canary Deployment](patterns/07-observability/36-shadow-canary-deployment.md) | 段階投入 |
| 変更管理 | [#53 Agent Change Management](patterns/12-governance/53-agent-change-management.md) | 変更プロセスの規律化 |
| 観測 | [#54 Tiered Observability](patterns/07-observability/54-tiered-observability.md) | コスト効率のよい観測 |

---

## 選定の5問

どの構成から始めるか迷ったら、以下の5問に答える。

1. **失敗したとき何が壊れるか？** → `[F2]` が高ければ副作用重視 or 事実性重視構成
2. **入力は信頼できるか？** → `[F5]` が低ければ信頼できない入力構成を重ねる
3. **月間コスト上限は？** → `[F7]` が高ければコスト重視構成を優先
4. **監査・規制要件はあるか？** → `[F8]` が高ければ継続改善運用構成を早期に導入
5. **まだプロトタイプか？** → はいなら最小構成から始め、本番化に伴い層を追加

構成は排他的ではない。たとえば、副作用重視とコスト重視のように、複数の構成を重ねて使うことも多い。重要なのは、[駆動変数](foundations/forces.md) に基づいて「なぜこの層が必要か」をきちんと説明できることである。
