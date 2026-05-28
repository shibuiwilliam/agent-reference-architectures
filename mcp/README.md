# MCP Server — Agent Reference Architectures

`catalog.json` を読み、コーディングエージェントがパターン・フォース・ダイヤル・二者択一を問い合わせるためのMCPサーバ。

## 起動

```bash
# stdio transport (Claude Code, Cursor 等)
python mcp/server.py

# uv 経由
uv run python mcp/server.py
```

## 必要パッケージ

```bash
pip install "mcp[cli]"
```

## 提供ツール

| ツール | 説明 |
|--------|------|
| `search_patterns(query)` | キーワード検索 |
| `get_pattern(pattern_id)` | パターン詳細取得 |
| `recommend(force_profile)` | フォース評価→推奨パターン |
| `list_reference_architectures()` | リファレンスアーキテクチャ一覧 |
| `get_decision(decision_type, decision_id)` | ダイヤル/二者択一の詳細 |
| `get_forces()` | フォースF1–F9の一覧 |

## 接続例（Claude Code）

```json
{
  "mcpServers": {
    "agent-architectures": {
      "command": "python",
      "args": ["mcp/server.py"],
      "cwd": "/path/to/agent-reference-architectures"
    }
  }
}
```

## スモークテスト

```bash
cd mcp && python smoke_test.py
```
