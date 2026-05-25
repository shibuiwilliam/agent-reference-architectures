# VI. 信頼性・検証・ガードレール・自律


!!! tip "この関心で効く意思決定"
    - **主なフォース**: `[F2]` 失敗コスト、`[F5]` 入力の信頼度、`[F1]` 可逆性
    - **主なダイヤル**: ガードレール厳しさ、自己修正ループ回数、HITL頻度、自律性レベル → [程度（ダイヤル）](../../decisions/tuning-dials.md)
    - **主な二者択一**: インライン↔事後検証、同一↔別モデル検証 → [相反（二者択一）](../../decisions/tradeoffs.md)
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

ハルシネーションと逸脱を出荷前に検出し回復する層。目的は制御でなく封じ込め。

- [#27 Evidence-First Answer｜根拠優先回答](27-evidence-first-answer.md) — 回答前に根拠を取得・引用
- [#28 Verifier Agent / Critic｜検証エージェント](28-verifier-agent-critic.md) — 独立した検証器で出荷前検査
- [#29 Guardrail Sidecar + Self-Correction｜ガードレール](29-guardrail-sidecar-self-correction.md) — 入出力検査し誤りを自己修正
- [#30 Policy-as-Code Guardrail｜ポリシー・アズ・コード](30-policy-as-code-guardrail.md) — 制約をコード化し別途判定
- [#31 Human Approval Checkpoint｜人間承認チェックポイント](31-human-approval-checkpoint.md) — 高リスク前に人間承認
- [#57 Autonomy Ladder｜自律性のはしご](57-autonomy-ladder.md) — 実績に応じ自律性を段階的に昇格
