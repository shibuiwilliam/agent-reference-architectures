# MCP Server — Agent Reference Architectures

`catalog.json` を読んでコーディングエージェントにパターン検索・推薦を提供する MCP サーバ。

## セットアップ

```bash
# 依存インストール
pip install "mcp[cli]"
# または
uv pip install "mcp[cli]"

# catalog.json を生成（未生成の場合）
uv run python scripts/generate.py
```

## 起動

```bash
# stdio transport（Claude Code、Cursor 等から接続）
python mcp-server/server.py
```

## Claude Code での接続

`.claude/settings.json` に追加:

```json
{
  "mcpServers": {
    "agent-reference-architectures": {
      "command": "python",
      "args": ["mcp/server.py"],
      "cwd": "/path/to/agent-reference-architectures"
    }
  }
}
```

## 提供ツール

| ツール | 説明 |
|-------|------|
| `search_patterns(query)` | キーワードでパターンを検索 |
| `get_pattern(pattern_id)` | パターンIDで詳細を取得 |
| `recommend(force_profile)` | フォース評価から推奨パターン・構成を返す |
| `list_reference_architectures()` | 6つの複合構成の一覧 |
| `get_decision(decision_type, decision_id)` | ダイヤル/二者択一の詳細 |
| `get_forces()` | 9つのフォースの一覧と説明 |

## 使用例

### パターン検索

```
search_patterns("キャッシュ")
→ #38 Semantic Result Cache, #39 Prompt Cache Optimized Context
```

### フォース評価から推奨

```
recommend({"F2": "high", "F1": "low"})
→ #31 Human Approval, #19 Dry-Run First, #4 Agent Saga, ...
  + 副作用重視構成
```

### ダイヤル詳細

```
get_decision("dial", "timeout")
→ { name: "タイムアウト", driver: ["F4"], default: "同期 5–10秒、非同期 5–30分", ... }
```
