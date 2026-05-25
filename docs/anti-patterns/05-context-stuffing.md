---
title: "コンテキスト詰め込みすぎ"
tags:
  - "アンチパターン"
  - "程度の誤り"
---

# 5. コンテキスト詰め込みすぎ

!!! abstract "一言"
    関連しそうな情報を全てプロンプトに詰め込み、コンテキスト窓を圧迫して回答品質とコストの両方を悪化させるアンチパターン。

## よくある場面

あるチームがRAGベースの社内ドキュメント検索エージェントを構築した。「情報が足りないよりは多い方がよい」という判断で、検索の top-k を20に設定し、取得した全チャンクをプロンプトに投入した。初期テストでは回答品質が良好だったが、ドキュメントが増えるにつれ問題が表面化した。関連度の低いチャンクがノイズとなり、エージェントが無関係な情報を引用して誤った回答を生成するケースが増えた。

さらに、1リクエストあたりのトークン数が平均8,000から30,000に膨らみ、コストが4倍近くに増大した。レイテンシも悪化し、応答に5秒以上かかるようになった。

## 症状

- 1リクエストあたりの入力トークン数が想定の3倍以上
- RAGの検索結果に無関係な情報が混在し、回答が的外れになる
- コンテキスト窓の上限に頻繁に到達し、重要な情報が切り捨てられる
- レイテンシがコンテキスト量に比例して増大する
- コストがリクエスト数以上に増大する（トークン量の増加分）

## 根本原因

「コンテキストに情報を多く入れれば、モデルが適切に取捨選択してくれる」という期待が根底にある。しかし、研究によればLLMは長いコンテキストの中間部分を見落としやすく（Lost in the Middle問題）、ノイズが多いほど回答品質は低下する。

top-k の値やチャンクサイズの設計を `[F7]` コスト感度や `[F4]` レイテンシ予算と結びつけて検討していないことが原因である。「検索で取れるだけ取って全部入れる」というアプローチは、情報の選別コストをLLMに転嫁しているに過ぎない。

## 発見方法

- **入力トークン数の分布**: リクエストごとの入力トークン数をモニタリングし、増加傾向がないか確認する
- **検索チャンクの関連度分析**: 投入したチャンクの関連度スコアを確認し、低関連度のチャンクが含まれていないか検証する
- **回答品質と投入量の相関**: top-k の値を変えて回答品質を比較し、品質のピークを探す
- **メトリクス**: `input_tokens_per_request`、`retrieval_relevance_score`、`answer_quality_vs_topk`

## 対策

### ステップ1: top-k と関連度閾値を最適化する

top-k を固定値にせず、関連度スコアの閾値を設定する。閾値を超えたチャンクのみを投入する。

### ステップ2: コンテキスト組み立てロジックを導入する

取得したチャンクを関連度・重複度・情報量で評価し、限られたコンテキスト予算内に収まるよう選択・圧縮する。

### ステップ3: 段階的な情報取得を実装する

最初は少量のコンテキストで回答を試み、情報が不足している場合のみ追加検索する。

```python
# 段階的コンテキスト組み立ての例
context_budget = 4000  # トークン上限

# 関連度順にソートし、予算内で組み立て
chunks = retriever.search(query, top_k=20)
chunks = [c for c in chunks if c.relevance > 0.7]  # 閾値フィルタ
chunks = deduplicate(chunks)

assembled = []
token_count = 0
for chunk in chunks:
    if token_count + chunk.tokens > context_budget:
        break
    assembled.append(chunk)
    token_count += chunk.tokens
```

## 具体例

### Before（問題のある状態）

```python
# 取れるだけ取って全部投入
chunks = retriever.search(query, top_k=20)
context = "\n".join([c.text for c in chunks])  # 全チャンクを結合

response = llm.chat(
    system="以下のコンテキストに基づいて回答してください。",
    context=context,  # 平均30,000トークン
    query=user_query,
)
```

### After（改善後）

```python
from context_assembler import ContextPack

chunks = retriever.search(query, top_k=20)
pack = ContextPack(
    budget_tokens=4000,
    relevance_threshold=0.7,
)
context = pack.assemble(chunks)  # 関連度の高い上位のみ選択

response = llm.chat(
    system="以下のコンテキストに基づいて回答してください。",
    context=context,  # 平均4,000トークン
    query=user_query,
)
# コスト75%削減、回答品質は同等以上
```

## 関連するアンチパターン

- [最強モデル一択](03-strongest-model-only.md) — コンテキストを圧縮すれば小モデルでも対応可能になる
- [無限・過大タイムアウト](01-infinite-timeout.md) — 大量コンテキストによるレイテンシ増でタイムアウトと複合する

## 関連パターン

- [#24 Context Pack / Assembly](../patterns/05-memory-context/24-context-pack-assembly.md) — 関連度の高い情報のみを選択的に組み立てる
- [#23 Layered Memory](../patterns/05-memory-context/23-layered-memory.md) — メモリを階層化してアクセスパターンを最適化する
- [#25 Memory Write Gate](../patterns/05-memory-context/25-memory-write-gate.md) — 記憶する情報自体を選別する
