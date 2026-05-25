---
title: "[F5] 入力の信頼度"
tags:
  - "駆動変数"
---

# [F5] 入力の信頼度（Input Trust）

!!! abstract "一言"
    エージェントへの入力に攻撃や汚染が混入する可能性を測るフォース。信頼度が低いほど、入力の検査・隔離・権限分離が必要になる。

## 概要

入力の信頼度は、エージェントが受け取るデータがどの程度信頼できるかを表す。社内システムからのAPI呼び出しと、不特定多数のユーザーからの自然言語入力では、プロンプトインジェクションやデータ汚染のリスクが桁違いに異なる。

## なぜ重要か

LLMベースのエージェントは自然言語を理解するがゆえに、入力に埋め込まれた悪意ある指示（プロンプトインジェクション）に対して構造的に脆弱である。信頼度を考慮しないと、ユーザー入力に含まれる指示がシステムプロンプトを上書きし、権限外の操作を実行させたり、機密データを漏洩させたりする。これは従来のSQLインジェクションと同様、入力境界のサニタイズが不可欠な問題である。

## 値域の解釈

### 低い場合

入力が信頼できる内部ソースに限定される状況。社内バッチシステムからの構造化データ、認証済み管理者からのAPI呼び出し、事前検証済みのデータパイプラインからの入力などが該当する。入力形式が固定されており、悪意ある操作の余地が小さい。検査を軽くしてスループットを優先できる。

### 高い場合（信頼度が低い＝リスクが高い）

不特定ユーザーからの自然言語入力を受け付ける状況。公開チャットボット、メール処理エージェント、Webフォーム経由のリクエスト、外部ドキュメントのRAG取り込みなどが該当する。プロンプトインジェクション、間接インジェクション（取得文書に埋め込まれた指示）、PII混入の可能性がある。入力の検査・サニタイズ・権限分離が必須になる。

## 評価の指針

- エージェントの入力は認証済みの内部システムからか、不特定ユーザーからか
- 自然言語入力をそのままプロンプトに埋め込んでいるか
- 外部ドキュメントや検索結果をコンテキストに取り込んでいるか（間接インジェクションの経路）
- 入力にPII・機密情報が含まれる可能性はあるか
- エージェントがアクセスできるツール・データの権限レベルはどの程度か

## 影響する設計判断

### 関連するダイヤル

- [ガードレール厳格度](../../decisions/dials/guardrail-strictness.md) — 信頼度が低いほど入出力の検査を厳格にする
- [公開ツール数](../../decisions/dials/exposed-tool-count.md) — 信頼度が低い入力経路では使用可能なツールを絞る
- [自律レベル](../../decisions/dials/autonomy-level.md) — 信頼できない入力に対しては自律レベルを下げる

### 関連する二者択一

- [同一モデル ↔ 異モデル](../../decisions/tradeoffs-catalog/same-vs-different-model.md) — 信頼できない入力を処理するLLMと特権操作を行うLLMを分離する
- [プロンプト ↔ コード](../../decisions/tradeoffs-catalog/prompt-vs-code.md) — 信頼できない入力の検証はコード（正規表現・スキーマ検証）で行う
- [構造化 ↔ 自由形式](../../decisions/tradeoffs-catalog/structured-vs-freeform.md) — 信頼度が低いほど入力を構造化して攻撃面を狭める

## 関連パターン

- [#42 Data Boundary Firewall](../../patterns/09-security/42-data-boundary-firewall.md) — 入出力でPII・機密情報を検査・マスクする
- [#44 Dual-LLM Privilege Separation](../../patterns/09-security/44-dual-llm-privilege-separation.md) — 入力処理と特権操作を別LLMに分離する
- [#43 Confused-Deputy Damage Limitation](../../patterns/09-security/43-confused-deputy-damage-limitation.md) — 騙されても被害半径を制限する
- [#18 Least-Privilege Tool Binding](../../patterns/04-tools-mcp/18-least-privilege-tool-binding.md) — セッション毎に最小権限を束縛する
- [#29 Guardrail Sidecar + Self-Correction](../../patterns/06-reliability/29-guardrail-sidecar-self-correction.md) — 入出力を検査し不正を検出・修正する
