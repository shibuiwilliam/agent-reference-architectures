# 相反（Forks）— 二者択一カタログ

**原則：排他的な仕組みの選択は、[駆動変数](../concepts/driving-variables.md) が決めてくれます。** 各フォークには**デフォルト**（迷ったらどちらを選ぶか）と**ハイブリッド**（折衷の定石）を付けています。ここで最も大切な教訓は **「相反は先に切る」** ことです。キャッシュ可否・承認要否・同期/非同期のような二択は領域ごとに先に分類し、その内側ではじめて [程度](../degrees/index.md) を調整してください。

各フォークの ID（`F-1`〜`F-18`）はパターン frontmatter の `forks` で参照されます。

| ID | フォーク | 選定基準 `[駆動変数]` | デフォルト | ハイブリッド | 関連 |
|---|---|---|---|---|---|
| F-1 | 同期 vs 非同期 | 処理時間が待機耐性（体感5–10秒/API連携30秒）を超えるか・途中再開が要るか `[latency_budget, reversibility]` | 数秒の読取/分類=同期、多段=非同期 | [A3 同期ファサード](../patterns/a-execution/a3-sync-facade-async-core.md) | [A1](../patterns/a-execution/a1-sync-edge-agent.md), [A2](../patterns/a-execution/a2-durable-async-agent.md) |
| F-2 | シングル vs マルチエージェント | 専門性/権限に分解できる・並列で時短・単一窓が溢れる・調整コストに見合う `[task_variability, cost_sensitivity]` | **まずシングル** | Supervisor＋専門役（文脈分離） | [B3](../patterns/b-orchestration/b3-agentic-loop-budget.md) |
| F-3 | オーケストレーション vs コレオグラフィ | 制御・監査・一貫性=中央／高スケール・疎結合=イベント `[accountability]` | 業務系=中央集権 | 中核は中央、周辺探索はイベント | [B3](../patterns/b-orchestration/b3-agentic-loop-budget.md) |
| F-4 | ワークフロー(決定論) vs エージェント(自律) | 手順が定型か変動か。規制下・高リスクは固定 `[task_variability, accountability]` | **できる限りワークフロー** | 決定論骨格＋確率論ノード | [B1](../patterns/b-orchestration/b1-deterministic-shell.md), [B2](../patterns/b-orchestration/b2-workflow-backbone.md) |
| F-5 | Plan-then-Execute vs ReAct | 環境が静的=計画先行／動的=ReAct `[task_variability]` | 計画先行（編集可能プラン） | 計画先行＋逸脱時のみ再計画 | [B4](../patterns/b-orchestration/b4-planner-executor-verifier.md) |
| F-6 | プロンプト制御 vs コード/ポリシー制御 | 境界・法的制約・不可逆操作はコード `[failure_cost, accountability]` | 境界はコード | ポリシー強制＋プロンプト誘導 | [E2](../patterns/e-safety-hitl/e2-policy-as-code.md) |
| F-7 | RAG vs FT vs ロングコンテキスト | 知識が変わる/出典要=RAG／様式固定=FT／文書が小さい=ロング `[accountability, cost_sensitivity]` | 知識はRAG | 様式はFT、事実はRAG | [D2](../patterns/d-memory-context/d2-context-budget-allocator.md) |
| F-8 | 単一プロバイダ vs マルチプロバイダ | 可用性SLA厳しい/コスト最適化=マルチ／一貫性・キャッシュ=単一 `[provider_trust, cost_sensitivity]` | 単一で開始 | 抽象化層越しにマルチ | [A6](../patterns/a-execution/a6-adaptive-timeout-retry.md) |
| F-9 | インライン検証(block) vs 事後・標本検証 | 悪い出力が届くコストが高い=インライン `[failure_cost, latency_budget]` | 高リスク経路=インライン | 高=インライン、低=標本監査 | [E3](../patterns/e-safety-hitl/e3-guardrail-sandwich.md) |
| F-10 | 生成と検証を同一 vs 別系統 | 事実性・安全性が重要なら独立・できれば決定論的検証を別に `[failure_cost]` | 高リスクは別系統 | 同一で一次反省＋別系統で最終 | [B6](../patterns/b-orchestration/b6-critic-judge-sampling.md) |
| F-11 | LLMに推論 vs ツール/コードに委譲 | 決定論的に解ける処理はコードへ、LLMは曖昧な解釈・生成 `[failure_cost, cost_sensitivity]` | 決定可能はコード | LLMが計画、コードが計算 | [B1](../patterns/b-orchestration/b1-deterministic-shell.md) |
| F-12 | Fail-fast vs 縮退継続 | 部分結果が有用か危険か `[failure_cost, latency_budget]` | 危険なら fail-fast | 段階的縮退ラダー | [A6](../patterns/a-execution/a6-adaptive-timeout-retry.md) |
| F-13 | プッシュ(SSE/WS/Webhook) vs プル(ポーリング) | リアルタイム進捗要=プッシュ `[latency_budget]` | 進捗表示=プッシュ | 進捗SSE＋確定Webhook | [A3](../patterns/a-execution/a3-sync-facade-async-core.md) |
| F-14 | インコンテキスト状態 vs 外部ステートストア | 耐久性・再開・複数共有が要れば外部化 `[reversibility]` | 長時間/承認/複数=外部 | 作業中は窓、節目で永続 | [A2](../patterns/a-execution/a2-durable-async-agent.md), [F1](../patterns/f-data-integrity/f1-short-tx-long-session.md) |
| F-15 | 読取専用 vs 書込可能エージェント | 書込は境界明確・dry-run・冪等・監査・補償・高リスク承認が揃って初めて許可 `[reversibility, failure_cost]` | まず読取専用 | Read自由・Writeはゲート | [C2](../patterns/c-tools-security/c2-read-free-write-gated.md) |
| F-16 | 自動メモリ vs 承認型メモリ | 低リスク嗜好=自動／重要・機微=承認 `[input_trust, failure_cost]` | 推測属性は保存しない | 候補抽出→隔離→承認 | [D3](../patterns/d-memory-context/d3-memory-write-gate.md) |
| F-17 | 構造化出力強制 vs 自由出力＋抽出 | 下流が厳格な型=強制／自由さが価値=自由 `[accountability, task_variability]` | 下流連携=強制 | 自由生成後に抽出パス | [E4](../patterns/e-safety-hitl/e4-verified-structured-output.md) |
| F-18 | ビルド vs バイ | 制御・データ主権=ビルド／速度・運用負荷=バイ `[cost_sensitivity, accountability]` | 抽象化層越しでバイ開始 | ランタイム抽象化で差替可能に | [A6](../patterns/a-execution/a6-adaptive-timeout-retry.md) |
