# VI. 信頼性・検証・ガードレール・自律


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F2]` 失敗コスト、`[F5]` 入力の信頼度、`[F1]` 可逆性
    - **主なダイヤル**: ガードレール厳しさ、自己修正ループ回数、HITL頻度、自律性レベル → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **主な二者択一**: インライン↔事後検証、同一↔別モデル検証 → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

LLMが自信たっぷりに間違えたり、プロンプトの意図から逸脱した回答を返したりすることは珍しくありません。こうしたハルシネーションや逸脱をユーザーに届く前に検出し、回復する層です。目的は完全な制御ではなく、影響の封じ込めにあります。

- [#27 Evidence-First Answer｜根拠優先回答](27-evidence-first-answer.md) — 回答の前にまず根拠を取得し、出典付きで提示する
- [#28 Verifier Agent / Critic｜検証エージェント](28-verifier-agent-critic.md) — 独立した検証器で出力を検査してから出荷する
- [#29 Guardrail Sidecar + Self-Correction｜ガードレール](29-guardrail-sidecar-self-correction.md) — 入出力をサイドカーで検査し、誤りがあれば自己修正する
- [#30 Policy-as-Code Guardrail｜ポリシー・アズ・コード](30-policy-as-code-guardrail.md) — 行動制約をコードとして定義し、決定論的に判定する
- [#31 Human Approval Checkpoint｜人間承認チェックポイント](31-human-approval-checkpoint.md) — 高リスクな操作の前に人間の承認を求める
- [#57 Autonomy Ladder｜自律性のはしご](57-autonomy-ladder.md) — 実績に応じてエージェントの自律性を段階的に引き上げる
