# PROJECT.md — プロジェクト憲章

## 1. 目的

意思決定層（**程度の調整**と**相反する仕組みの選定基準**）を中心に据えた、**AIエージェントを本番システムに組み込むためのソフトウェアアーキテクチャ・パターン集**を作る。単なるパターンの羅列ではなく、「どのパターンを、どの目盛りで、どちらの仕組みで採るか」を**根拠（どの駆動変数が効いたか）とともに**決められるようにすることが主眼。

## 2. 想定読者と利用シナリオ

| 読者 | 利用シナリオ | 必要な配慮 |
|------|--------------|------------|
| 人間（設計者/レビュア） | 設計判断の根拠を引く、レビューの観点リストにする | 読みやすいHTML、検索、図 |
| コーディングエージェント | 開発時に読み込み、AIエージェントを含む構成を設計し人間に提案 | frontmatterによる機械可読メタ、生マークダウン配信、明確な提案プロトコル |

**最重要ゴール**：コーディングエージェントがこのドキュメントを読み込むだけで、(1) 程度を駆動変数から導き、(2) 相反を文脈で解き、(3) パターンを組み合わせ、(4) **目盛り値とその理由を添えて人間に提案**できること。

## 3. 設計思想（背骨）

全コンテンツは「設計判断を貫く5層モデル」の上に乗る。5層の構成は `docs/index.md` のトップページ表を参照。

| 層 | 問い | 道具 | 置き場所 |
|---|------|------|----------|
| L0 なぜ難しいか | エージェントは普通のソフトと何が違うか | 設計力学 F1–F17 | `concepts/design-forces.md` |
| L1 何を配分するか | この処理に何をどれだけ使えるか | 7つの予算 | `concepts/budgets.md` |
| L2 どう決めるか | 目盛り・二択を何が左右するか | 9つの駆動変数 | `concepts/driving-variables.md` |
| L3 どこまで回すか | 各設計変数の「ちょうど」 | 程度（ダイヤル） | `degrees/` |
| L4 どちらを採るか | 排他的な仕組みのどちらか | 相反（フォーク） | `forks/` |
| L5 何を組むか | 実装する再利用部品 | パターン（A–G） | `patterns/` |

根本原則：**確率的な核（LLM）を、決定論的な殻（コード）で包む。** 最終成果物は「値」ではなく「**なぜその値か＝どの駆動変数がどの力学に効いたか**」の記録。

## 4. 情報アーキテクチャ（ディレクトリ）

```
.
├─ CLAUDE.md                 作業規約（Claude Code が自動読込）
├─ PROJECT.md                本ファイル
├─ README.md                 リポジトリの入口
├─ mkdocs.yml                サイト設定・nav・プラグイン
├─ pyproject.toml            ビルド依存（uv で管理）
├─ .github/workflows/deploy.yml  GitHub Pages 自動デプロイ
├─ scripts/                  new_pattern / validate / gen_indexes
└─ docs/
   ├─ index.md               トップ（目的・5層モデル・読み方）
   ├─ for-agents/            エージェント向け：使い方と提案プロトコル
   ├─ concepts/              第I部 地盤（force/budget/variable）
   ├─ degrees/               第II部 程度（ダイヤル）
   ├─ forks/                 第III部 相反（フォーク）
   ├─ patterns/              第IV部 パターン（_template.md と A〜G）
   ├─ decision/              第V部 意思決定フロー
   ├─ antipatterns/          第VI部 アンチパターン
   └─ reference/             用語集・機械可読インデックス
```

## 5. パターン分類（ドメイン A–G）と一覧

| ドメイン | テーマ | パターン |
|---|---|---|
| A | 実行方式・ライフサイクル | A1 同期エッジ / A2 耐久非同期 / A3 同期ファサード / A4 進捗ストリーミング / A6 適応タイムアウト・リトライ / A7 期限・予算カスケード |
| B | オーケストレーション・制御フロー | B1 決定論的な殻 / B2 ワークフロー骨格 / B3 予算付き自律ループ / B4 計画-実行-検証 / B5 Supervisor-Worker / B6 Critic-Judge・多数決 / B7 モデルルーター・適応努力 |
| C | ツール・副作用・セキュリティ | C1 ツールゲートウェイ/MCP仲介 / C2 読取自由・書込ゲート / C3 ドライラン・コミット / C4 冪等コマンド包装 / C5 Capability Lease / C6 Confused Deputy防御 / C7 サンドボックス実行 / C8 サーガ・補償 |
| D | メモリ・コンテキスト | D1 階層化メモリ / D2 コンテキスト予算配分 / D3 メモリ書込ゲート / D4 記憶の減衰・版管理 / D5 Prompt Registry / D6 禁止領域付きキャッシュ |
| E | 安全性・HITL・自律性 | E1 リスクベース承認 / E2 Policy-as-Code / E3 ガードレールサンドイッチ / E4 検証済み構造化出力 / E5 Autonomy Ladder |
| F | データ整合性・状態 | F1 短トランザクション・長セッション / F2 イベントソーシング・リプレイ |
| G | 観測・評価・運用 | G1 二層観測 / G2 全ホップトレース / G3 シャドウ・カナリア / G4 評価ハーネス / G5 サーキットブレーカ・縮退・抽象化 |

## 6. 機械可読性の方針（コーディングエージェント対応）

1. **frontmatter スキーマ**を全パターンに付与（`id/forces/driving_variables/forks/related_patterns/...`）。統制語彙は CLAUDE.md と `concepts/` に定義。
2. **生マークダウン配信**：`mkdocs-llmstxt` で `/llms.txt`（索引）・`/llms-full.txt`（全文）・各ページ `.md` を公開サイトに生成。
3. **リポジトリ直読**：エージェントは公開サイトを待たず `docs/**.md` を直接読める。frontmatter 込みなのでメタ抽出が容易。
4. **機械可読インデックス**：`docs/reference/pattern-index.md` に「id→ファイル→forces→driving_variables→forks」の表を `scripts/gen_indexes.py` で自動生成。
5. **提案プロトコル**：`docs/for-agents/decision-protocol.md` に、エージェントが踏む決定手順と提案出力テンプレートを規定。

## 7. 公開（MkDocs + GitHub Pages）

- テーマ：Material for MkDocs。プラグイン：`search`, `llmstxt`。拡張：`admonition`, `pymdownx.superfences`(+mermaid), `pymdownx.highlight`, `tables`, `toc(permalink)`。
- デプロイ：`main` への push で GitHub Actions がビルドし Pages へ公開（Pages の Source は **GitHub Actions**）。
- セットアップ時に置換が必要：`mkdocs.yml` の `site_url` と `repo_url`。

## 8. 執筆ロードマップ（推奨順）

1. **地盤を固める**：`concepts/`（force / budget / driving-variable）→ `degrees/` → `forks/` → `decision/` → `antipatterns/`。意思決定層が主題なのでここを最優先で stable に。
2. **基幹パターンを stable 化**：B1, A2, A3, E1, C1, C3, G1（提案で多用される土台）。
3. **残りのパターン**をドメイン順に draft→review→stable。
4. **横串の検証**：相互リンク、`validate.py`、`for-agents/decision-protocol.md` に沿った提案が実際に回るかをドッグフーディング。

各パターンの完成基準は CLAUDE.md §3.3「品質ゲート」。

## 9. スコープ外（やらないこと）

- 特定ベンダーSDKのAPIリファレンス（外部公式に委ねる。本書は設計判断に集中）。
- 実行可能なサンプルアプリ一式（実装メモは断片に留める）。
- モデル性能ベンチマーク（陳腐化が速い）。

## 10. 用語

主要な用語は各概念ページ（`docs/concepts/`）で定義している。統制語彙（forces / driving_variables / forks）は `CLAUDE.md` §3.1 に一覧がある。
