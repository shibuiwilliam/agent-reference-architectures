# AGENTS.md — コーディングエージェント向け統合ガイド

このリポジトリは **AIエージェント本番アーキテクチャ・パターン** のカタログであり、コーディングエージェントが読み込んでアーキテクチャ提案を生成するための構造化データを含む。

## カタログの概要

- **59パターン**（12カテゴリ）
- **9つの駆動変数**（フォース F1–F9）
- **20のダイヤル**（程度パラメータ）
- **16の二者択一**（相反する設計判断）
- **6つのリファレンスアーキテクチャ**（複合構成）
- **10の決定規則**（IF–THEN候補）
- **設計原則**: 確率的なコアを、決定論的な殻——契約・検証・予算・権限・観測——で囲む。

## 取り込み経路

### 経路1: リポジトリ同梱（CLAUDE.md / .cursor/rules 等）

本リポジトリの `AGENTS.md`（このファイル）または `CLAUDE.md` から参照する。以下を `system prompt` に含めるか、参照先として指定する:

```
このプロジェクトではAIエージェントアーキテクチャの設計に
agent-reference-architectures カタログ（v1.0.0）を使用する。

- カタログ: catalog.json (59パターン、9フォース、20ダイヤル、16二者択一)
- 設計手順: フォース評価(F1-F9)→二者択一→ダイヤル→パターン選定→提案出力
- 出力様式: agent-proposal-template.md に従う
- 引用規約: #N（パターン）、[F#]（フォース）を根拠として明記
- 境界: カタログ内パターンのみ使用。不確実は明示。最終判断は人間。
```

### 経路2: llms.txt / catalog.json（Web公開）

- **索引**: `https://shibuiwilliam.github.io/agent-reference-architectures/llms.txt`
- **意思決定コア（低トークン）**: `https://shibuiwilliam.github.io/agent-reference-architectures/llms-core.txt`
- **全文**: `https://shibuiwilliam.github.io/agent-reference-architectures/llms-full.txt`
- **構造化データ**: `https://shibuiwilliam.github.io/agent-reference-architectures/catalog.json`

### 経路3: MCP接続

`mcp/` ディレクトリにMCPサーバを提供（`catalog.json` を読む薄い実装）。

ツール:
- `search_patterns(query)` — 意味検索でパターン候補
- `get_pattern(id)` — 構造化詳細
- `recommend(force_profile)` — フォース評価→推奨パターン/構成
- `list_reference_architectures()` — 複合構成一覧
- `get_decision(dial|tradeoff)` — ダイヤル/二者択一の詳細

## 設計手順

```
要件・制約を読む
  → ① フォースを評価（F1–F9 を高/中/低で見積もる）
  → ② 二者択一を解く（同期/非同期、シングル/マルチ…）
  → ③ 程度を決める（タイムアウト・リトライ・自律性…のダイヤル値）
  → ④ パターンを選び複合構成に組む（リファレンスアーキ＋語彙59）
  → ⑤ 人間へ「提案」を出力（採否の根拠＝効いたフォースを引用付きで）
```

## 引用規約

- パターン: `#N`（例: `#31 Human Approval Checkpoint`）
- フォース: `[F#]`（例: `[F2]` 失敗コスト）
- ダイヤル: ダイヤル名（例: `タイムアウト`）
- 二者択一: 二者択一名（例: `同期↔非同期`）

## 境界規約

1. **カタログ内パターンのみ使用**: 存在しないパターンを捏造しない
2. **不確実性の開示**: 不明な場合は「不確実」と明示し人間に確認を求める
3. **最終判断は人間**: 提案は人間レビュー前提
4. **網羅性の限界**: カタログ範囲外の設計判断はその旨を明示
5. **目安値は出発点**: ダイヤルの値は本番データでの検証が前提

## 出力様式

提案は `docs/agent-proposal-template.md` のテンプレートに従って出力する。

## バージョン

カタログバージョン: **v1.0.0** (`patterns.yml` / `decisions.yml` の `version`)

変更履歴は `CHANGELOG.md` を参照。
