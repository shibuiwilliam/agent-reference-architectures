# II. エージェント構成・分担


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F6]` タスクの変動性、`[F2]` 失敗コスト、`[F3]` リクエスト価値
    - **主なダイヤル**: Best-of-N → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **主な二者択一**: シングル↔マルチエージェント、中央集権↔コレオグラフィ、Plan↔ReAct → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

1つのエージェントにすべてを任せると、プロンプトが膨張して専門性が薄れたり、自分のミスを自分で見逃したりする。人間のチームが役割分担するように、エージェントの能力やコンテキスト窓の限界を、構造的な役割分離によって乗り越えるためのパターン群である。

- [#8 Planner-Executor-Reviewer｜計画・実行・検証の分離](08-planner-executor-reviewer.md) — 計画・実行・検証を別ロールに分けて品質を高める
- [#9 Supervisor & Specialist Agents｜統括と専門](09-supervisor-specialist-agents.md) — 統括役が専門役にタスクを委譲する
- [#10 Agent Ensemble & Debate｜アンサンブル・討論](10-agent-ensemble-debate.md) — 複数エージェントで解いて合議・討論により頑健性を高める
- [#11 Deterministic Core, Probabilistic Edge｜決定論コア](11-deterministic-core-probabilistic-edge.md) — 中核は決定論的に保ち、周辺だけにAIを用いる
- [#12 Blackboard｜共有黒板](12-blackboard.md) — 共有黒板を介して疎結合に協調する
