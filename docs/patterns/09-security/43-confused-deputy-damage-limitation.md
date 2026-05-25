---
title: "Confused-Deputy Damage Limitation｜被害限定"
tags:
  - "セキュリティ・マルチテナント"
  - "F5 入力の信頼度"
---

# #43 Confused-Deputy Damage Limitation｜被害限定

!!! abstract "一言"
    エージェントがプロンプトインジェクション等で騙されても、被害半径を構造的に制限する。

## 概要

Confused Deputy（混乱した代理人）問題とは、権限を持つ主体が第三者に騙されて、その権限を意図しない操作に使われることを指す。LLMエージェントは自然言語入力を信頼境界なく処理するため、間接プロンプトインジェクションにより「騙される」リスクが常にある。本パターンは「騙されること自体は防げない」という前提に立ち、騙された場合の被害半径（Blast Radius）を最小化する設計を採る。

!!! info "意思決定上の位置づけ"
    - **必要にするフォース**: `[F5]` 入力の信頼度
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

## 設計

被害限定は単一コンポーネントではなく、複数の制約を組み合わせて実現する。

1. **最小権限**: セッションごとにツール・データアクセスを必要最小限に束縛する
2. **操作上限**: 1セッションあたりの書き込み回数・金額・影響範囲に上限を設ける
3. **不可逆操作の遅延**: 削除・送金・公開などは即時実行せず、承認キューに入れる
4. **影響範囲の分離**: 1エージェントが触れるリソースのスコープを限定する

これらを重ねることで、単一の防御が破られても被害が全体に波及しない。

## 解決する課題

エージェントに広い権限を与えると、プロンプトインジェクション1回で大規模な被害が生じる `[F5]`。メール送信、データ削除、コード実行、決済など副作用を持つ操作が連鎖すると、被害は指数的に拡大する。防御を「インジェクションを100%防ぐ」に賭けるのは非現実的であり、「突破されても痛みを限定する」設計が不可欠。

## 向き / 不向き

- **向き**: 外部データ（メール本文・Webページ・ユーザー入力）を処理するエージェント全般。副作用を持つツールにアクセスするエージェント。
- **不向き**: 読み取り専用で副作用を一切持たないエージェント（被害半径が元々小さい）。ただし情報漏洩も被害であり、完全に不要なケースは少ない。

## 要素技術

- 権限制御: [#18 Least-Privilege Tool Binding](../04-tools-mcp/18-least-privilege-tool-binding.md) のセッション単位適用
- 操作制限: Rate Limiter、金額上限、影響行数キャップ
- 承認キュー: [#31 Human Approval Checkpoint](../06-reliability/31-human-approval-checkpoint.md) との組み合わせ
- 影響分離: コンテナ分離、データベースのRow-Level Security

## 関連パターン

- [#44 Dual-LLM Privilege Separation](44-dual-llm-privilege-separation.md) — 権限分離による被害限定の具体的実装
- [#41 Tenant-Isolated Agent Runtime](41-tenant-isolated-agent-runtime.md) — テナント単位の分離で被害範囲を限定
- [#18 Least-Privilege Tool Binding](../04-tools-mcp/18-least-privilege-tool-binding.md) — 最小権限の原則をツールに適用
- [#4 Agent Saga](../01-execution/04-agent-saga.md) — 被害発生時の補償トランザクションで巻き戻す

## 参考

- Simon Willison, "Prompt injection and the confused deputy problem" (2023)
