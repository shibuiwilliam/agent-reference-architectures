---
title: 駆動変数（フォース）
---

# 駆動変数（フォース） F1–F9

!!! abstract "一言"
    パターンの「程度」と「選定」を決める9つの環境変数。同じパターンであっても、フォースの値域が変われば最適な実装は異なる。

## フォースとは何か

アーキテクチャパターンは固定のレシピではない。むしろ、**環境変数を引数にとる関数**のようなものである。ここで言う環境変数——駆動変数（フォース）——とは、システムが置かれた文脈を数値化・序列化したものを指す。パターンを「どの程度適用するか」（[程度ダイヤル](../decisions/tuning-dials.md)）や、「どちらを選ぶか」（[相反の選定基準](../decisions/tradeoffs.md)）は、フォースの値域によって決まる。

## F1–F9 一覧

| ID | 名前 | 問い | 低い場合 | 高い場合 | 関連パターン例 |
|----|------|------|----------|----------|--------------|
| `[F1]` | **可逆性** | 失敗をやり直せるか | 不可逆な副作用（メール送信・決済） | 何度でもリトライ可能 | [#4 Agent Saga](../patterns/01-execution/04-agent-saga.md), [#19 Dry-Run First](../patterns/04-tools-mcp/19-dry-run-first-tool-execution.md) |
| `[F2]` | **失敗コスト** | 金銭/法務/安全の痛み | 失敗しても軽微 | 誤りが訴訟・人命に関わる | [#28 Verifier Agent](../patterns/06-reliability/28-verifier-agent-critic.md), [#31 Human Approval](../patterns/06-reliability/31-human-approval-checkpoint.md) |
| `[F3]` | **1リクエストの価値** | 売上/意思決定への寄与 | 大量の低単価リクエスト | 1件が大きな契約・意思決定 | [#10 Agent Ensemble](../patterns/02-composition/10-agent-ensemble-debate.md), [#37 Semantic Gateway](../patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) |
| `[F4]` | **レイテンシ予算** | ユーザーの待機耐性 | 即応（100ms級）を期待 | 数分〜数時間の待ちを許容 | [#1 Request-to-Job Gateway](../patterns/01-execution/01-request-to-job-gateway.md), [#7 Streaming Progress](../patterns/01-execution/07-streaming-progress.md) |
| `[F5]` | **入力の信頼度** | 攻撃/汚染の混入可能性 | 信頼できる内部システムからの入力 | 不特定ユーザーの自然言語入力 | [#42 Data Boundary Firewall](../patterns/09-security/42-data-boundary-firewall.md), [#44 Dual-LLM](../patterns/09-security/44-dual-llm-privilege-separation.md) |
| `[F6]` | **タスクの変動性** | 定型↔探索 | 手順が固定のルーチン | 未知の問題を探索的に解く | [#3 Workflow Backbone](../patterns/01-execution/03-workflow-backbone-agent-node.md), [#59 Spectrum Selector](../patterns/01-execution/59-workflow-agent-spectrum-selector.md) |
| `[F7]` | **コスト感度・スケール** | QPS・月間コスト上限 | コスト制約が緩い | 大量リクエスト・厳しいコスト上限 | [#38 Semantic Result Cache](../patterns/08-cost-scaling/38-semantic-result-cache.md), [#56 Adaptive Effort](../patterns/08-cost-scaling/56-adaptive-effort.md) |
| `[F8]` | **説明責任・規制** | 監査・コンプラ要件 | 社内ツール・実験用途 | 医療・金融・法務など規制業種 | [#32 Agent Trace](../patterns/07-observability/32-agent-trace.md), [#30 Policy-as-Code](../patterns/06-reliability/30-policy-as-code-guardrail.md) |
| `[F9]` | **プロバイダ信頼度** | 外部LLMの可用性 | 単一プロバイダで十分 | 可用性・ベンダーロックインが懸念 | [#40 Fallback](../patterns/08-cost-scaling/40-fallback-graceful-degradation.md), [#45 Agent Runtime Abstraction](../patterns/10-deployment/45-agent-runtime-abstraction.md) |

## 使い方

1. **現状把握**: 自システムの F1–F9 を「高/中/低」で見積もる
2. **パターン選定**: フォースが高い領域に対応するパターンを優先的に採用する
3. **程度調整**: 選定したパターン内のダイヤル（タイムアウト値、リトライ回数など）をフォースの値に応じて調整する（→ [程度ダイヤル](../decisions/tuning-dials.md)）
4. **相反判断**: 二者択一の設計判断はフォースの組み合わせで決める（→ [相反の選定基準](../decisions/tradeoffs.md)）

## フォースは変動する

フォースは固定値ではない。同じシステムであっても、機能追加やユーザー層の変化、規制改正などによって、フォースの値域は変わりうる。そのため、定期的に見直してパターンの適用度を再調整する運用が求められる（→ [#53 Agent Change Management](../patterns/12-governance/53-agent-change-management.md)）。
