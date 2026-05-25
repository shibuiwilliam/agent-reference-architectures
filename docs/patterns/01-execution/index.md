# I. 実行・セッション・オーケストレーション


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F4]` レイテンシ予算、`[F1]` 可逆性、`[F7]` コスト感度
    - **主なダイヤル**: タイムアウト、チェックポイント頻度、予算上限 → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **主な二者択一**: 同期↔非同期、ワークフロー↔エージェント → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

長時間にわたる処理や、予測が難しい処理、失敗の可能性がある処理を、Web層から切り離して安全に実行するための土台となるパターン群である。

- [#1 Request-to-Job Gateway｜非同期受付ゲートウェイ](01-request-to-job-gateway.md) — 1リクエストを非同期ジョブとして受け付ける
- [#2 Durable Agent Session｜耐久エージェントセッション](02-durable-agent-session.md) — 状態を永続化し、中断・再開に耐えられるようにする
- [#3 Workflow Backbone + Agent Node｜決定論骨格＋ノード](03-workflow-backbone-agent-node.md) — 全体の骨格は決定論的に保ち、判断が必要な部分だけをエージェントに委譲する
- [#4 Agent Saga｜補償トランザクション](04-agent-saga.md) — 副作用の連鎖を補償アクションで巻き戻せるようにする
- [#5 Time-Budgeted Agent Loop｜予算付きループ](05-time-budgeted-agent-loop.md) — 時間・回数・コストに予算を設けて暴走を防ぐ
- [#6 Interruptible Agent｜中断可能エージェント](06-interruptible-agent.md) — 実行途中で停止し、方針を修正できるようにする
- [#7 Streaming Progress｜進捗ストリーミング](07-streaming-progress.md) — 実行過程を監査可能な要約として逐次表示する
- [#55 Deadline & Budget Cascade｜期限・予算のカスケード](55-deadline-budget-cascade.md) — 期限と予算を呼出ツリー全体に伝播させる
- [#58 Sync Facade over Async Core｜同期ファサード](58-sync-facade-over-async-core.md) — 短い処理は同期で返し、閾値を超えたら非同期へ昇格させる
- [#59 Workflow–Agent Spectrum Selector｜選定メタ](59-workflow-agent-spectrum-selector.md) — サブタスクごとに決定論と自律のバランスを選定する
