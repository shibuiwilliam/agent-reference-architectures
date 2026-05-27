---
title: 決定規則（IF–THEN）
---

# 決定規則（IF–THEN候補提示）

!!! abstract "一言"
    フォース評価から「まず検討すべきパターン候補」を絞り込むIF–THEN規則。最終選定はフォース評価と人間判断に委ねる。

## この章の目的

[意思決定の進め方](decision-flow.md) のステップ②「ルール照合」で使う決定規則の一覧。`decisions.yml` の `rules[]` から生成される。

各規則は「フォースの組み合わせ → 必須/推奨/任意のパターン候補」を示す。これは**候補提示**であり、断定ではない。フォースの相互作用や個別の制約は、[通し例](worked-examples.md) で総合判断の流れを確認してほしい。

---

## 規則一覧

<!-- BEGIN:GEN:rules -->
### rule-high-f2-low-f1

**条件**: `F2`=high AND `F1`=low

- **必須**: #31 Human Approval Checkpoint, #19 Dry-Run First Tool Execution, #4 Agent Saga
- **推奨**: #3 Workflow Backbone + Agent Node, #15 Inverted Structured Output
- **任意**: #28 Verifier Agent / Critic, #10 Agent Ensemble & Debate
- **根拠**: 不可逆かつ高リスク → #31(承認), #19(Dry-Run), #4(Saga) は必須。#3(骨格) と #15(判断分離) は推奨。#28(検証), #10(合議) は F3 高の場合に追加
- **昇格条件**: F3 も高い場合は optional を recommended に昇格

### rule-high-f2-high-f8

**条件**: `F2`=high AND `F8`=high

- **必須**: #28 Verifier Agent / Critic, #30 Policy-as-Code Guardrail, #32 Agent Trace
- **推奨**: #33 Prompt/Model/Tool Version Pinning, #10 Agent Ensemble & Debate
- **任意**: #52 Agent Constitution, #54 Tiered (Hot/Cold) Observability
- **根拠**: 高リスク＋監査義務 → #28(独立検証), #30(ポリシーコード化), #32(全件トレース) は必須。#33(バージョン固定), #10(合議) は推奨
- **昇格条件**: F9 低の場合は #40(フォールバック) を recommended に追加

### rule-low-f5

**条件**: `F5`=low

- **必須**: #13 Natural Language Boundary Adapter, #42 Data Boundary Firewall, #44 Dual-LLM Privilege Separation
- **推奨**: #18 Least-Privilege Tool Binding, #43 Confused-Deputy Damage Limitation, #29 Guardrail Sidecar + Self-Correction
- **任意**: #20 Sandboxed Tool Runtime, #41 Tenant-Isolated Agent Runtime
- **根拠**: 信頼できない入力 → #13(境界), #42(データ検査), #44(権限分離) は必須。#18(最小権限), #43(被害限定), #29(ガードレール) は推奨
- **昇格条件**: マルチテナントの場合は #41 を recommended に昇格

### rule-high-f7

**条件**: `F7`=high

- **必須**: #37 Semantic Gateway & Cost-Aware Router, #5 Time-Budgeted Agent Loop
- **推奨**: #38 Semantic Result Cache, #39 Prompt Cache Optimized Context, #56 Adaptive Effort
- **任意**: #40 Fallback & Graceful Degradation, #55 Deadline & Budget Cascade
- **根拠**: コスト制約 → #37(ルーティング), #5(予算上限) は必須。#38(キャッシュ), #39(プロンプトキャッシュ), #56(努力配分) は推奨
- **昇格条件**: F9 低の場合は #40 を required に昇格

### rule-high-f8

**条件**: `F8`=high

- **必須**: #32 Agent Trace, #33 Prompt/Model/Tool Version Pinning
- **推奨**: #34 Evaluation CI/CD, #30 Policy-as-Code Guardrail, #54 Tiered (Hot/Cold) Observability
- **任意**: #52 Agent Constitution, #53 Agent Change Management
- **根拠**: 監査・規制 → #32(トレース), #33(バージョン固定) は必須。#34(評価CI/CD), #30(ポリシーコード化), #54(二層観測) は推奨
- **昇格条件**: F2 も高い場合は #30 を required に昇格

### rule-low-f9

**条件**: `F9`=low

- **必須**: #40 Fallback & Graceful Degradation
- **推奨**: #45 Agent Runtime Abstraction, #46 Model Behavior Compatibility Layer
- **任意**: #36 Shadow / Canary Deployment
- **根拠**: プロバイダ不安定 → #40(フォールバック) は必須。#45(ランタイム抽象化), #46(互換レイヤー) は推奨
- **昇格条件**: F3 高の場合は #45, #46 を required に昇格

### rule-high-f6

**条件**: `F6`=high

- **必須**: #59 Workflow–Agent Spectrum Selector
- **推奨**: #12 Blackboard, #9 Supervisor & Specialist Agents
- **任意**: #47 Agent Capability Registry
- **根拠**: 探索的タスク → #59(選定メタ) は必須。#12(黒板), #9(統括・専門) は推奨
- **昇格条件**: マルチエージェント導入時は #47 を recommended に昇格

### rule-low-f6

**条件**: `F6`=low

- **必須**: #3 Workflow Backbone + Agent Node
- **推奨**: #11 Deterministic Core, Probabilistic Edge
- **任意**: #14 Structured Output Contract
- **根拠**: 定型タスク → #3(ワークフロー骨格) は必須。#11(決定論コア) は推奨
- **昇格条件**: F8 高の場合は #11 を required に昇格

### rule-high-f3

**条件**: `F3`=high

- **必須**: #10 Agent Ensemble & Debate
- **推奨**: #8 Planner-Executor-Reviewer, #28 Verifier Agent / Critic
- **任意**: #37 Semantic Gateway & Cost-Aware Router
- **根拠**: 高価値リクエスト → #10(合議) は必須。#8(計画-検証分離), #28(独立検証) は推奨
- **昇格条件**: F7 も高い場合は #37 を recommended に昇格

### rule-low-f4

**条件**: `F4`=low

- **必須**: #58 Sync Facade over Async Core
- **推奨**: #7 Streaming Progress, #38 Semantic Result Cache
- **任意**: #39 Prompt Cache Optimized Context
- **根拠**: 即応性要求 → #58(同期ファサード) は必須。#7(ストリーミング), #38(キャッシュ) は推奨
- **昇格条件**: F7 も高い場合は #39 を recommended に昇格

<!-- END:GEN:rules -->

---

## 使い方

1. [駆動変数（フォース）](../foundations/forces.md) を「高/中/低」で評価する
2. 上記の規則から、条件に合致するものを**すべて**収集する（複数ルールが同時に該当しうる）
3. **必須** パターンを採用候補に入れる
4. **推奨** パターンをフォースの組み合わせに応じて検討する
5. **任意** パターンは escalation 条件に該当する場合に昇格を検討する
6. [二者択一](tradeoffs.md) と [ダイヤル](tuning-dials.md) を併せて設計判断を完成させる

!!! warning "候補提示であり断定ではない"
    規則は「まず検討すべきパターン」を絞り込む手段であり、自動的に採用を決めるものではない。最終判断は人間が行う。

## 関連ページ

- [意思決定の進め方](decision-flow.md)
- [フォース別逆引き](by-force.md)
- [通し例](worked-examples.md)
- [アーキテクチャ提案テンプレート](../agent-proposal-template.md)
