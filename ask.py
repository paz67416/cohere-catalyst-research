"""
ask.py - 文献への質問応答スクリプト（Cohere RAGパイプライン）

やること:
  1. 質問を受け付ける
  2. store.json の中から、質問に意味が近いチャンクを検索する（Embed）
  3. Rerank で並べ直し、上位だけを選ぶ
  4. 選んだチャンクを根拠として Command A に渡し、答えを生成する

システムプロンプト（v1）は研究文脈として埋め込み済み。毎回貼り直す必要はありません。

使い方:
  1. 先に `python ingest.py` を実行しておく
  2. `$env:CO_API_KEY = "あなたのAPIキー"` を実行（PowerShellの場合）
  3. `python ask.py` を実行して、対話形式で質問する
     または `python ask.py "この論文の主張は？"` のように直接渡す
"""
import os
import sys
import json
import math
import cohere

# ---- 設定 ----------------------------------------------------------------
STORE_PATH = "store.json"
EMBED_MODEL = "embed-v4.0"
RERANK_MODEL = "rerank-v3.5"
CHAT_MODEL = "command-a-03-2025"   # 論理的検討向けの最上位モデル
TOP_K_SEARCH = 20                  # ベクトル検索で拾う候補数
TOP_N_RERANK = 5                   # Rerank後に根拠として使う数
# -------------------------------------------------------------------------

# システムプロンプト（研究コンテキスト）をシステムプロンプトとして埋め込み
SYSTEM_PROMPT = """あなたは、独立研究者による意識研究プロジェクトを支援するアシスタントです。以下の文脈を前提として応答してください。

【研究の概要】
- 主題: 所有感(mineness)、行為主体感(agency)、フロー状態の関係
- 基本的な立場: 主観性は経験生成の原因ではなく、経験生成の結果として現れる
- 中心仮説: フロー/ゾーン状態には「二重の事後性」構造がある。(1)クオリアが形成された後に主体が現れる、(2)「自分がやった」という行為の帰属も行為の後から遅れてやってくる
- 自由意志感: 行為の開始時点ではなく、「構え(kamae)」に位置づける（Libet型の知見への応答）

【理論的な扱いの注意】
- 東洋哲学への言及(梵我一如、色即是空など)は、検証可能な構造へ翻訳するための「事前の直観」として扱うこと。証拠や結論としては扱わないこと

【応答のスタイル】
- 提供された文献の記述に基づいて答え、根拠と限界を明示する
- 文献に書かれていないことは推測であると明示し、文献に基づく主張と区別する
- 断定や迎合よりも検証を優先する
- 日本語の質問には日本語で、英語の質問には英語で応答する
"""


def get_client():
    api_key = os.environ.get("CO_API_KEY")
    if not api_key:
        sys.exit("エラー: 環境変数 CO_API_KEY が設定されていません。")
    return cohere.ClientV2(api_key=api_key)


def load_store():
    if not os.path.exists(STORE_PATH):
        sys.exit(f"エラー: {STORE_PATH} がありません。先に `python ingest.py` を実行してください。")
    with open(STORE_PATH, encoding="utf-8") as f:
        return json.load(f)


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def search(co, store, query, top_k=TOP_K_SEARCH):
    """質問をベクトル化し、コサイン類似度で上位を返す。"""
    resp = co.embed(
        model=EMBED_MODEL,
        texts=[query],
        input_type="search_query",   # 検索クエリ側の指定
        embedding_types=["float"],
    )
    q_vec = resp.embeddings.float[0]
    scored = [(cosine(q_vec, rec["embedding"]), rec) for rec in store]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [rec for _, rec in scored[:top_k]]


def rerank(co, query, candidates, top_n=TOP_N_RERANK):
    """候補チャンクを Rerank で並べ直し、上位を返す。"""
    docs = [rec["text"] for rec in candidates]
    resp = co.rerank(
        model=RERANK_MODEL,
        query=query,
        documents=docs,
        top_n=min(top_n, len(docs)),
    )
    return [candidates[r.index] for r in resp.results]


def answer(co, query, sources):
    """根拠チャンクを渡して Command A に回答させる。"""
    documents = [
        {"data": {"text": rec["text"], "source": rec["source"]}}
        for rec in sources
    ]
    resp = co.chat(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        documents=documents,
    )
    # 応答テキストを取り出す
    parts = [c.text for c in resp.message.content if c.type == "text"]
    return "\n".join(parts)


def handle(co, store, query):
    candidates = search(co, store, query)
    if not candidates:
        print("該当するチャンクが見つかりませんでした。")
        return
    top = rerank(co, query, candidates)
    print("\n--- 参照した文献 ---")
    for rec in top:
        print(f"  ・{rec['source']} (chunk {rec['chunk_id']})")
    print("\n--- 回答 ---")
    print(answer(co, query, top))
    print()


def main():
    co = get_client()
    store = load_store()
    print(f"store.json を読み込みました（{len(store)} チャンク）")

    # 引数で質問が渡された場合は一度だけ実行
    if len(sys.argv) > 1:
        handle(co, store, " ".join(sys.argv[1:]))
        return

    # 対話モード
    print("質問を入力してください（終了は Ctrl+C または空Enter）")
    while True:
        try:
            query = input("\n質問: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n終了します。")
            break
        if not query:
            break
        handle(co, store, query)


if __name__ == "__main__":
    main()
