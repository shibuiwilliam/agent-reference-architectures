# F. データ整合性・状態

このドメインのパターン一覧（frontmatter から自動生成）。

| ID | パターン | forces | driving_variables | status |
|---|---|---|---|---|
| F1 | [Short DB Transaction, Long Agent Session｜長セッション・短トランザクション](f1-short-tx-long-session.md) | `[F1, F3]` | `[reversibility]` | draft |
| F2 | [Event-sourced / Replayable Runs｜イベントソーシングとリプレイ](f2-event-sourced-replayable.md) | `[F3, F15, F16]` | `[accountability]` | draft |
