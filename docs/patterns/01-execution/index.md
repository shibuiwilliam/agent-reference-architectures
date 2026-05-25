# I. 実行・セッション・オーケストレーション

長時間・予測不能・失敗しうる実行を、Web層から切り離して安全に走らせる土台。

- [#1 Request-to-Job Gateway｜非同期受付ゲートウェイ](01-request-to-job-gateway.md) — 1リクエストを非同期ジョブとして受け付ける
- [#2 Durable Agent Session｜耐久エージェントセッション](02-durable-agent-session.md) — 状態を永続化し中断・再開に耐える
- [#3 Workflow Backbone + Agent Node｜決定論骨格＋ノード](03-workflow-backbone-agent-node.md) — 骨格は決定論、判断だけ委譲
- [#4 Agent Saga｜補償トランザクション](04-agent-saga.md) — 副作用連鎖を補償で巻き戻す
- [#5 Time-Budgeted Agent Loop｜予算付きループ](05-time-budgeted-agent-loop.md) — 時間・回数・コストを予算化し暴走を止める
- [#6 Interruptible Agent｜中断可能エージェント](06-interruptible-agent.md) — 途中で停止・方針修正できる
- [#7 Streaming Progress｜進捗ストリーミング](07-streaming-progress.md) — 過程を監査可能な要約で逐次表示
- [#55 Deadline & Budget Cascade｜期限・予算のカスケード](55-deadline-budget-cascade.md) — 期限・予算を呼出ツリーへ伝播
- [#58 Sync Facade over Async Core｜同期ファサード](58-sync-facade-over-async-core.md) — 短ければ同期、超えたら非同期へ昇格
- [#59 Workflow–Agent Spectrum Selector｜選定メタ](59-workflow-agent-spectrum-selector.md) — サブタスク毎に決定論↔自律を選定
