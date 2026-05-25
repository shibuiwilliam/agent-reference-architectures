# PROJECT.md

**意思決定（フォース・程度・相反）を中心に**、AIエージェントを本番システムへ組み込むアーキテクチャパターンのドキュメントサイト。**MkDocs (Material)** で構築し、**GitHub Pages** に公開する。IAの重心は「意思決定を背骨、パターンを語彙」。

- 対象読者: AIエージェントを本番システムへ組み込むアーキテクト／エンジニア
- 規模: 12カテゴリ・59パターン ＋ 意思決定層（中核）・複合構成・アンチパターン
- 正本（single source of truth）: [`patterns.yml`](patterns.yml)
- 執筆ルール: [`CLAUDE.md`](CLAUDE.md)

---

## 技術スタック

| 役割 | 採用 |
|---|---|
| 静的サイトジェネレータ | MkDocs |
| テーマ | Material for MkDocs |
| 図 | Mermaid（`pymdownx.superfences` 経由） |
| ホスティング | GitHub Pages（`gh-pages` ブランチ） |
| CI/CD | GitHub Actions（`.github/workflows/deploy.yml`） |
| 言語 | 日本語（`theme.language: ja`、検索も `lang: ja`） |

---

## ディレクトリ構成

```text
agent-architecture-patterns/
├─ mkdocs.yml                  # サイト設定・ナビゲーション（nav は手動管理）
├─ requirements.txt            # mkdocs-material, pymdown-extensions
├─ patterns.yml                # ★59パターンの正本（scaffold が参照）
├─ PROJECT.md                  # このファイル
├─ CLAUDE.md                   # Claude Code 向け執筆指示
├─ .github/workflows/deploy.yml# Pages へ自動デプロイ
├─ scripts/
│  └─ scaffold.py              # patterns.yml からスタブ生成（冪等）
├─ templates/
│  └─ pattern.md               # パターン執筆テンプレート（ビルド対象外）
└─ docs/                       # ★ビルド対象。ここがサイトの中身
   ├─ index.md                 # トップ
   ├─ assets/stylesheets/extra.css
   ├─ foundations/
   │  ├─ characteristics.md     # AIエージェントの特性
   │  └─ forces.md              # 駆動変数 F1–F9
   ├─ patterns/
   │  ├─ 01-execution/          # I. 実行・セッション・オーケストレーション
   │  │  ├─ index.md            # カテゴリ概要
   │  │  ├─ 01-request-to-job-gateway.md   # ← 完成済みの手本
   │  │  ├─ 02-durable-agent-session.md
   │  │  └─ … (03,04,05,06,07,55,58,59)
   │  ├─ 02-composition/        # II. 構成・分担 (08–12)
   │  ├─ 03-io-contract/        # III. 入出力・契約化 (13–16)
   │  ├─ 04-tools-mcp/          # IV. ツール・MCP (17–22)
   │  ├─ 05-memory-context/     # V. メモリ・コンテキスト (23–26)
   │  ├─ 06-reliability/        # VI. 信頼性・検証・自律 (27–31,57)
   │  ├─ 07-observability/      # VII. 観測・監査・評価 (32,54,33–36)
   │  ├─ 08-cost-scaling/       # VIII. コスト・性能 (37–40,56)
   │  ├─ 09-security/           # IX. セキュリティ (41–44)
   │  ├─ 10-deployment/         # X. デプロイ・抽象化 (45–48)
   │  ├─ 11-ux/                 # XI. UI/UX (49–51)
   │  └─ 12-governance/         # XII. 組織・ガバナンス (52,53)
   ├─ decisions/
   │  ├─ tuning-dials.md        # 程度（B-1）
   │  ├─ tradeoffs.md           # 相反（B-2）
   │  └─ parameterization.md    # パターンのパラメータ化（B-3）
   ├─ anti-patterns.md
   ├─ reference-architectures.md
   └─ pattern-index.md          # 59パターン早見表
```

ファイル名は `NN-slug.md`（`NN` = グローバルなパターン番号の2桁ゼロ詰め、`slug` = 英小文字ハイフン）。番号は飛び番（55,58,59 が I に入る等）になるが、これは新規パターンを後から各カテゴリへ統合した経緯による。**番号と slug は `patterns.yml` を正本とし、勝手に変えない。**

---

## セットアップとローカルプレビュー

```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 未作成のパターンページ・カテゴリ index を一括生成（既存は上書きしない）
python scripts/scaffold.py

# ローカルプレビュー（http://127.0.0.1:8000 / ホットリロード）
mkdocs serve

# 本番と同条件でビルド（リンク切れ等があれば失敗）
mkdocs build --strict
```

---

## デプロイ（GitHub Pages）

1. リポジトリを GitHub に push（デフォルトブランチ `main`）。
2. `mkdocs.yml` の `site_url` / `repo_url` / `repo_name` の `<user>` を自分のものに置換。
3. `main` への push で `.github/workflows/deploy.yml` が走り、`mkdocs gh-deploy` が `gh-pages` ブランチを生成・更新する。
4. GitHub の **Settings → Pages → Build and deployment → Source = "Deploy from a branch"**、**Branch = `gh-pages` / `(root)`** に設定。
5. 数十秒後 `https://<user>.github.io/agent-architecture-patterns/` で公開される。

> 手動デプロイは `mkdocs gh-deploy --force`。CI を使わず Pages の GitHub Actions ソースで配信したい場合は、`upload-pages-artifact` + `deploy-pages` 方式に差し替えてもよい。

---

## 執筆ワークフロー（Claude Code）

1. `python scripts/scaffold.py` でスタブを用意する。
2. Claude Code で対象パターンの `.md` を開き、[`CLAUDE.md`](CLAUDE.md) の規約に従って執筆する。
3. `mkdocs build --strict` が通ること（リンク切れ・nav 不整合がないこと）を確認する。
4. 1パターン＝1コミット（例: `docs(#12): write Blackboard pattern`）。

「完成（Definition of Done）」の基準は [`CLAUDE.md`](CLAUDE.md) を参照。

---

## 進捗チェックリスト

- [x] #1 Request-to-Job Gateway（手本・完成）
- [x] #2–#7, #55, #58, #59（I 実行）
- [x] #8–#12（II 構成）
- [x] #13–#16（III 契約）
- [x] #17–#22（IV ツール）
- [x] #23–#26（V メモリ）
- [x] #27–#31, #57（VI 信頼性）
- [x] #32, #54, #33–#36（VII 観測）
- [x] #37–#40, #56（VIII コスト）
- [x] #41–#44（IX セキュリティ）
- [x] #45–#48（X デプロイ）
- [x] #49–#51（XI UX）
- [x] #52–#53（XII 組織）
- [x] 土台2本（characteristics, forces）
- [x] 意思決定層3本（tuning-dials, tradeoffs, parameterization）
- [x] anti-patterns / reference-architectures / pattern-index
