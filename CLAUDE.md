# CLAUDE.md

このリポジトリで作業する Claude Code への指示。AIエージェント本番アーキテクチャ・パターンの **MkDocs ドキュメントサイト**を執筆・保守する。

## このプロジェクトの目的

**意思決定（フォース・程度・相反）を中心**に、12カテゴリ・59パターンの解説ページを MkDocs (Material) でビルドして GitHub Pages に公開する。IAの重心は「意思決定を背骨、パターンを語彙」。全体像・構成・デプロイ手順は `PROJECT.md`、パターンの正本は `patterns.yml`。

## まず守る原則

- **`patterns.yml` + `decisions.yml` が正本。** パターン・フォース・ダイヤル・二者択一・リファレンスアーキテクチャ・決定規則はここに従う。**勝手に追加・改名・採番しない。** 変更が要るときは正本YAMLを更新し、`python scripts/generate.py` で成果物を再生成、`mkdocs.yml` の `nav` も手で合わせ、その旨をコミットメッセージに書く。
- **機械可読成果物は生成物。** `catalog.json`、`llms.txt`、`llms-core.txt`、`llms-full.txt`、各パターンの `GEN:meta` ブロック、`pattern-index.md` の表は `generate.py` が正本YAMLから生成する。**直接編集しない。**
- **手本は `docs/patterns/01-execution/01-request-to-job-gateway.md`。** 迷ったらこの構成・粒度・トーンに合わせる。
- **テンプレートは `templates/pattern.md`。** 新規ページはこれを基に書く（`scaffold.py` が適用済み）。
- 出力言語は**日本語**。技術用語・パターン名の英語表記は併記してよい。

## ファイルの場所

| やりたいこと | 触るファイル |
|---|---|
| パターン本文を書く | `docs/patterns/<NN-category>/<NN-slug>.md` |
| カテゴリ概要を書く | `docs/patterns/<NN-category>/index.md` |
| 土台ページ | `docs/foundations/characteristics.md`, `forces.md` |
| 意思決定層（中核） | `docs/decisions/decision-flow.md`（背骨）, `tuning-dials.md`, `tradeoffs.md`, `interactions.md`, `by-force.md`, `worked-examples.md`, `adr-template.md`, `parameterization.md` |
| 横断ページ | `docs/anti-patterns.md`, `reference-architectures.md`, `pattern-index.md` |
| ナビ追加・並び替え | `mkdocs.yml` の `nav`（手動） |
| スタブ生成 | `python scripts/scaffold.py`（既存は上書きしない） |
| 成果物再生成 | `python scripts/generate.py`（catalog.json, llms.txt, メタブロック等） |
| エージェント利用ガイド | `docs/agent-guide.md`, `docs/agent-proposal-template.md` |
| エージェント統合 | `AGENTS.md`（リポジトリ直下） |
| MCP サーバ | `mcp-server/server.py` |
| 意思決定層データ | `decisions.yml`（正本） |

`templates/`・`scripts/`・`patterns.yml`・`decisions.yml`・`site/`（ビルド成果物）は**サイト本文ではない**。`site/` は触らない・コミットしない。生成物（`catalog.json`等）はコミットするが直接編集しない。

## パターンページの必須構成

各パターンは次の見出しを**この順**で持つ（手本と同じ）。

1. YAML フロントマター（`title` と `tags`：カテゴリ名＋該当する `F#`）
2. `# #{番号} {タイトル}`
3. `!!! abstract "一言"` … 1文のTL;DR
4. `## 概要` … 2〜4文。何を・どこに置くか
5. `!!! info "意思決定上の位置づけ"` … **必須**。必要にするフォース・関与するダイヤル/二者択一・意思決定の進め方へのリンク
6. `## 設計` … 構成要素とデータの流れ。必要なら mermaid 図
6. `## 解決する課題` … どの特性／設計圧力に効くか、「無いと何が壊れるか」
7. `## 向き / 不向き` … **両方必須**。不向きを書かないものはパターンでなく宣伝
8. `## 要素技術` … 具体的な実装候補に接続
9. `## 調整（程度）` … 目盛りがある場合のみ。無ければ節ごと削除
10. `## 選定（相反）` … 相反する代替がある場合のみ。無ければ節ごと削除
11. `## 関連パターン` … **最低1つ**、相対リンクで
12. `## 参考` … 任意

書く順序のコツ: **特性 → それが壊す前提 → 必要な構造 → 向き/不向き** の流れで考える。能力自慢でなく「本番で壊れる箇所への防波堤」として書く。

## 記法・スタイル規約

- **長さの目安**: 1パターン 250〜500語程度。冗長な前置きや能書きを避け、密度を上げる。
- **トーン**: 断定しすぎず、トレードオフを明示する実務的な解説。
- **過度な装飾を避ける**: 見出し・太字・箇条書きは必要最小限。手本の密度に合わせる。
- **mermaid 図**は ```` ```mermaid ```` フェンスで。`flowchart` / `sequenceDiagram` を基本に、ノードは3〜7個程度に抑える。無理に図を足さない。
- **admonition** は Material 記法（`!!! note`, `!!! warning`, `!!! abstract` 等）。一言TL;DRは `!!! abstract "一言"` を使う。
- **コードブロック**には言語を付ける。
- 既存の本文を消す破壊的編集をしない。スタブを埋める／加筆する形で進める。

## クロスリファレンスの規約

- **駆動変数**は `` `[F#]` `` 形式（例 `[F4]`）。一覧は `docs/foundations/forces.md`。本文中で目盛りや二択の根拠として明示する。
- **同カテゴリの他パターン**: `[#12 Blackboard](12-blackboard.md)`（同フォルダ相対）
- **別カテゴリのパターン**: `[#44 Dual-LLM Privilege Separation](../09-security/44-dual-llm-privilege-separation.md)`
- **意思決定層へのリンク**（パターンページから）: `../../decisions/tuning-dials.md`, `../../decisions/tradeoffs.md`
- リンク先ファイルが**まだ無い**場合は、先に `scaffold.py` を走らせてスタブを用意してからリンクする（`--strict` ビルドでリンク切れを出さないため）。
- リンクは**ファイルパス**で書く（`.md` 付き）。URL直書きや存在しないアンカーを使わない。

## ビルドと品質ゲート（コミット前に必ず）

```bash
python scripts/generate.py   # 正本から成果物を再生成
mkdocs build --strict         # リンク切れ・nav不整合をチェック
```

両方が**エラーゼロで通ること**が完成条件。`--strict` はリンク切れ・nav 不整合・未参照ファイルを失敗にする。
`generate.py` は冪等（2回実行しても差分が出ない）。CIでも毎回実行される。

`scaffold.py --check` で「未作成ページがないか」を確認できる。

## 完成の定義（Definition of Done / 1パターン）

- [ ] 必須見出しが順に揃い、`向き` と `不向き` の両方がある
- [ ] `!!! info "意思決定上の位置づけ"` ブロックがある（フォース・関与する決定・意思決定の進め方へのリンク）
- [ ] `関連パターン` に有効な相対リンクが1つ以上ある
- [ ] 該当するなら `調整`/`選定` に `[F#]` と決定層へのリンクがある
- [ ] フロントマターの `tags` にカテゴリ名と該当 `F#` がある
- [ ] `patterns.yml` に `related`, `when_to_use`, `when_not`, `element_tech`, `dials`, `tradeoffs` が記入されている
- [ ] `<!-- BEGIN:GEN:meta --><!-- END:GEN:meta -->` マーカーがある（`generate.py` がメタブロックを注入）
- [ ] `python scripts/generate.py && mkdocs build --strict` がエラーなく通る
- [ ] `mkdocs.yml` の `nav` に当該ページが登録されている（scaffold 生成分は手で nav に追記）

## やってはいけないこと

- パターン番号・slug の改変、`patterns.yml` 外でのパターン新設
- `site/`（生成物）の編集・コミット
- 外部記事・書籍からの**長文のコピペ**（要約・自分の言葉で書く。出典は `参考` に）
- 事実が不確かな製品仕様・バージョン番号・価格の断定（必要なら一般化して書くか、出典を添える）
- 1コミットに複数パターンを混ぜること（原則 1パターン＝1コミット）

## コミットメッセージ規約

```
docs(#12): write Blackboard pattern
docs(forces): add F1–F9 driving variables page
chore(nav): register #57 Autonomy Ladder
fix(links): repair cross-refs in 04-tools-mcp
```

## タスクの進め方（標準フロー）

1. `python scripts/scaffold.py` で対象のスタブが存在することを確認（無ければ生成）。
2. 対象 `.md` をテンプレ／手本に沿って執筆。`patterns.yml` の `tagline`・`forces` を反映。
3. `patterns.yml` に `related`, `when_to_use`, `when_not`, `element_tech`, `dials`, `tradeoffs` を記入。
4. 関連パターン・決定層への相対リンクを張る（リンク先スタブが無ければ先に生成）。
5. `python scripts/generate.py` を実行し、メタブロック注入・成果物更新。
6. `mkdocs build --strict` を実行し、エラーを解消。
7. `nav` 登録を確認し、1パターン＝1コミットで記録。

## エージェント統合の規約

- **`AGENTS.md`**（リポジトリ直下）と **`docs/agent-guide.md`**（サイト掲載）は同じ情報を齟齬なく保つ。
- **`docs/agent-proposal-template.md`** がエージェントの出力様式。変更時は `AGENTS.md` も合わせる。
- **MCP サーバ** (`mcp-server/server.py`) は `catalog.json` を読む。`catalog.json` は `generate.py` が生成するため、MCPサーバを直接編集する必要は通常ない。
- **バージョン** は `patterns.yml` / `decisions.yml` の `version` フィールド。変更時は `CHANGELOG.md` を更新する。
