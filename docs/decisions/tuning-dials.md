---
title: 程度（チューニング）ダイヤル
---

# 程度（チューニング）ダイヤル

!!! abstract "一言"
    パターンは ON/OFF でなく**目盛り付き**。ダイヤルの値域を駆動変数 `[F#]` で決める。

## ダイヤルとは

多くのパターンには「どの程度適用するか」を決めるパラメータがある。たとえば、タイムアウト値やリトライ回数、ガードレールの厳しさなどがそれにあたる。これらは小さすぎても大きすぎても問題が起きるため、最適点はシステムの文脈——すなわち [駆動変数（フォース）](../foundations/forces.md) の値域——に応じて決める必要がある。

このページでは主要なダイヤルを一覧し、目安値と調整の決め手を示す。ただし、目安値はあくまで**出発点**であり、本番データで検証しながら調整していくことが前提である。

## ダイヤル・カタログ

| ダイヤル | 小さすぎ | 大きすぎ | 決め手 | 目安（出発点） | 関連パターン |
|---------|---------|---------|-------|--------------|-------------|
| **タイムアウト（1リクエスト）** | 正常な処理が途中で打ち切られる | コネクション占有・リソース枯渇 | `[F4]` レイテンシ予算 | 同期 5–10秒、非同期 5–30分 | [#1 Gateway](../patterns/01-execution/01-request-to-job-gateway.md), [#5 Time-Budgeted](../patterns/01-execution/05-time-budgeted-agent-loop.md) |
| **リトライ回数（ネットワーク）** | 一時障害で即失敗 | リトライストーム・コスト増 | `[F9]` プロバイダ信頼度 | 2–3回（指数バックオフ） | [#40 Fallback](../patterns/08-cost-scaling/40-fallback-graceful-degradation.md) |
| **自己修正ループ回数** | 最初の失敗で諦める | トークン浪費・無限ループ | `[F7]` コスト感度、`[F3]` リクエスト価値 | 1–3回 | [#29 Guardrail Sidecar](../patterns/06-reliability/29-guardrail-sidecar-self-correction.md) |
| **チェックポイント頻度** | 長時間分のやり直し | I/Oオーバーヘッド・レイテンシ増 | `[F1]` 可逆性 | ステップ毎またはN分毎 | [#2 Durable Agent Session](../patterns/01-execution/02-durable-agent-session.md) |
| **予算上限（トークン/コスト）** | 有用な結果を出す前に打ち切り | コスト爆発 | `[F7]` コスト感度、`[F3]` リクエスト価値 | リクエスト価値の10–30% | [#5 Time-Budgeted](../patterns/01-execution/05-time-budgeted-agent-loop.md), [#55 Deadline Cascade](../patterns/01-execution/55-deadline-budget-cascade.md) |
| **自律性レベル** | 毎回人間承認で遅延 | 暴走リスク | `[F2]` 失敗コスト、`[F1]` 可逆性 | 新規は低→実績で段階昇格 | [#57 Autonomy Ladder](../patterns/06-reliability/57-autonomy-ladder.md) |
| **HITL（Human-in-the-Loop）頻度** | 人間がボトルネック | リスクの見逃し | `[F2]` 失敗コスト | 高リスク操作のみ | [#31 Human Approval](../patterns/06-reliability/31-human-approval-checkpoint.md) |
| **ガードレール厳しさ** | 有害出力の見逃し | 正当な出力まで遮断（過検知） | `[F5]` 入力信頼度、`[F2]` 失敗コスト | 閾値0.7–0.9（用途依存） | [#29 Guardrail Sidecar](../patterns/06-reliability/29-guardrail-sidecar-self-correction.md), [#30 Policy-as-Code](../patterns/06-reliability/30-policy-as-code-guardrail.md) |
| **モデル階層（ルーティング閾値）** | 簡単なタスクに高コストモデル | 難問を低品質モデルに回す | `[F7]` コスト感度、`[F3]` リクエスト価値 | 分類器の信頼度 0.8 以上で小モデル | [#37 Semantic Gateway](../patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) |
| **Best-of-N（生成数）** | 最初の1つに依存 | コスト N倍 | `[F2]` 失敗コスト、`[F3]` リクエスト価値 | 1（低リスク）、3–5（高リスク） | [#10 Agent Ensemble](../patterns/02-composition/10-agent-ensemble-debate.md) |
| **温度（Temperature）** | 創造性不足・同一回答の繰り返し | 出力の不安定・ハルシネーション増 | `[F6]` タスク変動性 | 0.0–0.3（定型）、0.5–0.8（探索） | [#33 Version Pinning](../patterns/07-observability/33-version-pinning.md) |
| **キャッシュ類似度閾値** | ほぼ同一クエリしかヒットしない | 意味が異なるクエリに古い結果を返す | `[F7]` コスト感度 | コサイン類似度 0.92–0.97 | [#38 Semantic Result Cache](../patterns/08-cost-scaling/38-semantic-result-cache.md) |
| **検索 top-k / 投入量** | 関連情報の取りこぼし | コンテキスト溢れ・ノイズ混入 | `[F4]` レイテンシ予算、`[F7]` コスト感度 | top-k 5–20、全体の50%以下 | [#24 Context Pack](../patterns/05-memory-context/24-context-pack-assembly.md) |
| **メモリ TTL** | 有用な記憶が早く消える | 古い情報で判断を誤る | `[F8]` 説明責任 | セッション: 1時間、長期: 30–90日 | [#26 Forgetting](../patterns/05-memory-context/26-forgetting-and-expiration.md) |
| **メモリ書き込み積極度** | 重要な学びを忘れる | ノイズが蓄積しコンテキストを圧迫 | `[F8]` 説明責任 | 信頼度閾値で自動、低ければ人間承認 | [#25 Memory Write Gate](../patterns/05-memory-context/25-memory-write-gate.md) |
| **要約タイミング** | コンテキスト溢れ | 重要な詳細の欠落 | `[F4]` レイテンシ予算 | トークン使用量が窓の70%到達時 | [#23 Layered Memory](../patterns/05-memory-context/23-layered-memory.md) |
| **露出ツール数** | 必要なツールが使えない | 選択肢過多で誤選択 | `[F6]` タスク変動性 | 5–15個/セッション | [#18 Least-Privilege Tool Binding](../patterns/04-tools-mcp/18-least-privilege-tool-binding.md) |
| **トレースサンプリング率** | 問題発生時に情報不足 | ストレージ・コスト増 | `[F8]` 説明責任、`[F7]` コスト感度 | 開発100%、本番1–10% | [#32 Agent Trace](../patterns/07-observability/32-agent-trace.md), [#54 Tiered Observability](../patterns/07-observability/54-tiered-observability.md) |
| **プロンプト保存先・粒度** | 変更追跡ができない | リポジトリ肥大化 | `[F8]` 説明責任 | Git管理、バージョンタグ付き | [#33 Version Pinning](../patterns/07-observability/33-version-pinning.md) |
| **ログ保持期間** | コンプラ違反・調査不能 | ストレージコスト | `[F8]` 説明責任、`[F7]` コスト感度 | Hot 7–30日、Cold 1–7年 | [#54 Tiered Observability](../patterns/07-observability/54-tiered-observability.md) |

## 使い方

1. 導入するパターンの「調整（程度）」節に記載されたダイヤルを確認する
2. 自システムの [駆動変数](../foundations/forces.md) を「高/中/低」で見積もる
3. 上表の「決め手」列と照合し、目安値を出発点として設定する
4. 本番のメトリクス（エラー率、コスト、レイテンシ）を見て継続的に調整する

ダイヤルの値は「一度決めたら終わり」ではない。[#53 Agent Change Management](../patterns/12-governance/53-agent-change-management.md) のプロセスに沿って、定期的に見直していくことが大切である。
