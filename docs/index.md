---
title: はじめに
---

# AIエージェント本番アーキテクチャ・パターン

!!! abstract "基本原理"
    **確率的なコアを、決定論的な殻——契約・検証・予算・権限・観測——で囲む。そして、殻の目盛りを文脈（フォース）に応じて調整する。**

## このサイトについて

AIエージェントは、プロトタイプならすぐ動く。しかし本番に載せた途端に、タイムアウト、コスト爆発、ハルシネーションが噴出する——そんな経験はないだろうか。

本サイトは、そうした**「本番で壊れる」を防ぐためのアーキテクチャパターン集**だ。12カテゴリ・59パターンの設計意図・向き不向き・要素技術・調整の勘所を解説している。

ただのパターンカタログではない。**意思決定（フォース・程度・相反）が中心**にある。パターンは語彙、程度と相反は文法、フォースは文意——この順序で設計判断を組み立てていく。

## 対象読者

### 人間（アーキテクト・エンジニア）

「デモでは動いたのに本番で落ちる」「コストが読めない」「ハルシネーションをどう防ぐか」——プロトタイプから本番への移行で直面するこうした課題に取り組むアーキテクトやエンジニアのためのサイトだ。「壊れ方」を理解し、その防波堤となるパターンを選ぶ判断力を身につけてほしい。

### コーディングエージェント

本カタログは人間だけでなく、**コーディングエージェント（LLM）にも読まれることを前提に設計**されている。構造化データ（`catalog.json`）を読み込み、設計要件に対して根拠（フォース・パターン番号）付きのアーキテクチャ提案を生成することが期待される。

## まず「選定の5問」に答える

どこから読むか迷ったら、以下の5問に答えるところから始める。

1. **失敗したとき何が壊れるか？** → `[F2]` が高ければ [副作用重視構成](reference-architectures/02-side-effect-first.md)
2. **入力は信頼できるか？** → `[F5]` が低ければ [信頼できない入力構成](reference-architectures/03-untrusted-input.md)
3. **月間コスト上限は？** → `[F7]` が高ければ [コスト重視構成](reference-architectures/05-cost-first.md)
4. **監査・規制要件はあるか？** → `[F8]` が高ければ [継続改善運用構成](reference-architectures/06-continuous-improvement.md)
5. **まだプロトタイプか？** → はいなら [最小構成](reference-architectures/01-mvp.md) から始める

→ 5問の詳細は [リファレンスアーキテクチャ](reference-architectures/index.md) を参照

## 読み方

### 人間の場合 — ブラウズ → 理解 → 判断

1. **[意思決定の進め方](decisions/decision-flow.md)** を辿る — フォース評価 → 二者択一 → ダイヤル → 構成合成 → 記録の6ステップ
2. 必要なパターンを **[パターン早見表](pattern-index.md)** から引く
3. 実際の使い方は **[通し例](decisions/worked-examples.md)** で確認する

### コーディングエージェントの場合 — 取り込み → 評価 → 提案

1. `_agent/README.md` を読む — エントリポイント・決定アルゴリズム・制約
2. `_agent/decision-core.md` を読む — フォース F1–F9 を評価し、ルールを照合
3. `_agent/pattern-cards.json` から候補パターンの構造化サマリを取得
4. 詳細が必要なパターンは `docs/patterns/<cat>/<slug>.md` を個別取得
5. `_agent/proposal-template.md` に従って提案を出力

→ 詳しくは **[`_agent/README.md`](https://github.com/shibuiwilliam/agent-reference-architectures/blob/main/_agent/README.md)** へ

→ ショートカット: [タスク別インデックス](https://github.com/shibuiwilliam/agent-reference-architectures/blob/main/_agent/by-task.md) / [問題別インデックス](https://github.com/shibuiwilliam/agent-reference-architectures/blob/main/_agent/by-problem.md)

→ 守ってほしいこと: カタログ内パターンのみ使用 / 不確実なら明示 / 最終判断は人間

### 各ページの役割

| 区分 | ページ | 役割 | 主な読者 |
|------|--------|------|---------|
| **意思決定** | [意思決定の進め方](decisions/decision-flow.md) | 6ステップの通しワークフロー | 共通 |
| | [駆動変数（フォース）](foundations/forces.md) | F1–F9 の定義 | 共通 |
| | [程度（ダイヤル）](decisions/tuning-dials.md) | 20のダイヤル | 共通 |
| | [相反（二者択一）](decisions/tradeoffs.md) | 16の二者択一 | 共通 |
| | [フォース別逆引き](decisions/by-force.md) | フォースから引く辞書 | 共通 |
| | [通し例](decisions/worked-examples.md) | 一気通貫の実演 | 共通（few-shot） |
| **パターン** | [パターン早見表](pattern-index.md) | 59パターン一覧 | 人間 |
| **複合構成** | [リファレンスアーキテクチャ](reference-architectures/index.md) | 構成例 | 共通 |
| | [アンチパターン](anti-patterns/index.md) | やってはいけない設計 | 共通 |
| **機械可読** | `catalog.json` | 構造化マニフェスト | エージェント |
| | `llms-core.txt` | 意思決定コア | エージェント |
| | `llms-full.txt` | 全ページ連結 | エージェント |
| **統合** | [エージェント向けガイド](agent-guide.md) | 利用手順・規約 | エージェント |
| | [提案テンプレート](agent-proposal-template.md) | 出力様式 | エージェント |
| **エージェント経路** | `_agent/README.md` | エントリポイント | エージェント |
| | `_agent/decision-core.md` | 決定データ（軽量） | エージェント |
| | `_agent/pattern-cards.json` | パターン選定データ | エージェント |
| | `_agent/by-task.md` | タスク別逆引き | エージェント |
| | `_agent/by-problem.md` | 問題別逆引き | エージェント |
