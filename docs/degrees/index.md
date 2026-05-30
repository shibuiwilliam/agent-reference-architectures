# 程度（Degrees）— ダイヤル・カタログ

**原則：あらゆる目盛りは「効きすぎる害」と「効かなすぎる害」のちょうどよい中点を探す問題です。** ここに載せている目安値はあくまで出発点であり、[駆動変数](../concepts/driving-variables.md) に応じて動かしてください。固定のハードコードは避け、本番メトリクス（p99レイテンシ・ヒット率・評価スコア）をもとに継続的に再調整する変数として扱ってください。

## 実行・信頼性

| ダイヤル | 効かなすぎ ⇔ 効きすぎ | 決め方 `[駆動変数]` | 目安（出発点） | 関連 |
|---|---|---|---|---|
| タイムアウト | 正当な長時間処理を殺す ⇔ リソース占有・障害隠蔽・UX悪化 | 観測P99×安全係数を**層ごと**に持つ `[latency_budget]` | ツール10–30秒／LLM呼出60–120秒／セッション全体は分〜数十分。ストリーミングは**トークン間タイムアウト**が優れる | [A6](../patterns/a-execution/a6-adaptive-timeout-retry.md) |
| ネットワーク/5xxリトライ | 一過性障害で即失敗 ⇔ コスト増幅・リトライストーム | 指数バックオフ＋ジッタ＋`Retry-After`。**非冪等な書き込みは冪等キー無しでリトライ禁止** `[failure_cost, cost_sensitivity]` | 2–4回、上限到達でサーキットを開く | [A6](../patterns/a-execution/a6-adaptive-timeout-retry.md), [C4](../patterns/c-tools-security/c4-idempotent-command-envelope.md) |
| 自己修正リトライ | 直せる出力を捨てる ⇔ 同じ誤りの反復・レイテンシ爆発 | ネットワークリトライと別物。エラー内容を文脈に足す。3回目以降は改善しないことが多い `[failure_cost]` | 1–3回、超過で安全なフォールバック | [E4](../patterns/e-safety-hitl/e4-verified-structured-output.md) |
| チェックポイント頻度 | クラッシュ時に作業消失 ⇔ I/O過多 | 意味あるステップ単位＋**副作用の直前で必ず** `[reversibility]` | 各ツール実行後・各LLM応答後・承認前 | [A2](../patterns/a-execution/a2-durable-async-agent.md) |
| 予算上限(steps/cost/deadline) | 有用作業を途中で切る ⇔ 暴走・請求事故 | タスク種別ごと。切れたら部分結果か人間へ `[cost_sensitivity]` | 調査系 max_steps 20–50／対話系 5–10／cost上限は1リクエスト価値の数%以下 | [A7](../patterns/a-execution/a7-deadline-budget-cascade.md) |

エラーは三分類で扱います。①一時障害（429/5xx/タイムアウト）→リトライが有効です。②コンテンツ起因（スキーマ不適合・低品質）→単純リトライは無意味なので self-correction に回します。③コンテキスト長超過→要約・分割で対応します。決済・発注など戻せない副作用は**自動リトライを禁止し、状態確認後に補償**してください。

## 自律性・人間介在

自律性は有無ではなく段階で設計します（L0–L6）。固定せず、実績に基づいて昇格/降格させてください（[E1](../patterns/e-safety-hitl/e1-risk-based-approval.md)）。

| Lv | 名前 | できること |
|---|---|---|
| L0 | Suggest only | 提案のみ |
| L1 | Read-only | 読み取りツールのみ |
| L2 | Draft | 下書き作成 |
| L3 | Dry-run | 実行計画と差分提示 |
| L4 | Approval required | 人間承認後に実行 |
| L5 | Bounded auto-execute | 低リスク範囲で自動 |
| L6 | Full autonomous | 広範な自動（原則、限定環境のみ） |

| ダイヤル | 効かなすぎ ⇔ 効きすぎ | 決め方 `[駆動変数]` | 目安 | 関連 |
|---|---|---|---|---|
| 自律性レベル | 価値が出ない ⇔ 被害半径拡大 | 可逆性×失敗コスト×信頼度で自動/要承認/禁止に三分 `[reversibility, failure_cost]` | 読取=自動、可逆な書込=信頼度で自動化、不可逆=常に承認 | [E1](../patterns/e-safety-hitl/e1-risk-based-approval.md) |
| HITL承認頻度 | リスク放置 ⇔ 承認疲れ | 全件でなくリスクゲート。承認はバッチ化 `[failure_cost]` | 金銭/不可逆のみ事前承認、他は標本監査 | [E1](../patterns/e-safety-hitl/e1-risk-based-approval.md) |
| ガードレールの厳しさ | 危険出力が漏れる ⇔ 誤検知でUX破壊・無限自己修正 | 高失敗コスト経路だけ厳格に。block と warn を使い分け `[failure_cost, latency_budget]` | 副作用前・外部公開前は block、内部補助は warn | [E3](../patterns/e-safety-hitl/e3-guardrail-sandwich.md) |

## コスト・品質

| ダイヤル | 効かなすぎ ⇔ 効きすぎ | 決め方 `[駆動変数]` | 目安 | 関連 |
|---|---|---|---|---|
| モデル階層 | 品質不足 ⇔ コスト/レイテンシ爆発 | 難易度で動的選択、失敗時のみ上位へ `[cost_sensitivity, request_value]` | 分類/抽出=小型、推論/計画=高性能、検証=別系統 | [B7](../patterns/b-orchestration/b7-model-router-adaptive-effort.md) |
| Best-of-N の N | 単発で不安定 ⇔ N倍コスト | 高難度/高失敗コストのみ上げる `[request_value]` | 既定 N=1、高リスクのみ 3–5 | [B6](../patterns/b-orchestration/b6-critic-judge-sampling.md) |
| 温度 | 硬直 ⇔ 不安定・逸脱 | 抽出/分類は低温、創作は高温 `[task_variability]` | 構造化 0–0.3／対話 0.5–0.7／創作 0.8+ | [E4](../patterns/e-safety-hitl/e4-verified-structured-output.md) |
| キャッシュ類似度閾値 | ヒット率低下 ⇔ 誤回答の再利用 | 高失敗コスト領域ほど上げる `[failure_cost, cost_sensitivity]` | コサイン 0.92–0.97、リスク高は再検証併用 | [D6](../patterns/d-memory-context/d6-semantic-cache-nocache-zones.md) |

## メモリ・コンテキスト

| ダイヤル | 効かなすぎ ⇔ 効きすぎ | 決め方 `[駆動変数]` | 目安 | 関連 |
|---|---|---|---|---|
| 検索 top-k / 投入文脈量 | 文脈不足でハルシネーション ⇔ "lost in the middle"・コスト増 | 信号密度最大化、リランクで絞る `[cost_sensitivity]` | 3–8件＋リランク。窓の50–70%超で圧縮 | [D2](../patterns/d-memory-context/d2-context-budget-allocator.md) |
| メモリTTL/保持量 | 継続性喪失 ⇔ 古い情報・矛盾・肥大 | 種別ごとにTTL `[failure_cost]` | 価格/状態=短期、嗜好=中期、不変知識=無期限 | [D1](../patterns/d-memory-context/d1-tiered-memory.md) |
| メモリ書込の積極度 | 学習しない ⇔ 記憶汚染 | 書込ゲート閾値。重複・低確信・機微は弾く `[input_trust]` | 明示的事実・反復確認のみ永続化 | [D3](../patterns/d-memory-context/d3-memory-write-gate.md) |
| 露出ツール数 | 仕事ができない ⇔ 選択ミス・遅延 | 動的スコーピングで必要分だけ `[task_variability]` | 同時露出10–20以下、超過はルーティング | [C1](../patterns/c-tools-security/c1-tool-gateway-mcp-broker.md) |

## 観測

| ダイヤル | 効かなすぎ ⇔ 効きすぎ | 決め方 `[駆動変数]` | 目安 | 関連 |
|---|---|---|---|---|
| トレース・サンプリング率 | 障害を再現できない ⇔ 観測コスト爆発 | エラー/高リスク/HITLは全量、成功は標本 `[accountability, cost_sensitivity]` | エラー/HITL=100%、成功=1–10% | [G1](../patterns/g-observability-ops/g1-tiered-observability.md) |
| プロンプト/出力の保存先・粒度 | 監査・デバッグ不能 ⇔ 観測基盤の肥大・PII混入 | ホット/コールド二層化 `[accountability, cost_sensitivity]` | 基盤=メタ＋truncate＋hash、本文=オブジェクトストレージ | [G1](../patterns/g-observability-ops/g1-tiered-observability.md) |
| ログ保持期間 | 監査要件を満たせない ⇔ 保管コスト・法的リスク | ホット短期、コールドは規制要件まで `[accountability]` | ホット7–30日／コールド90日〜数年 | [G1](../patterns/g-observability-ops/g1-tiered-observability.md) |
