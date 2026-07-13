"""
ingest.py — 文献取り込みスクリプト（Cohere RAGパイプライン）

やること:
  1. papers/ フォルダ内のPDFを読み込む
  2. テキストを抽出し、扱いやすい断片（チャンク）に分割する
  3. 各チャンクを Cohere Embed でベクトル化する
  4. ベクトルと元テキストを store.json に保存する

使い方:
  1. このフォルダに papers/ を作り、論文PDFを入れる
  2. `export CO_API_KEY=あなたのAPIキー` を実行（または .env を使う）
  3. `python ingest.py` を実行

出力: store.json（ask.py がこれを読む）
"""

import os
import sys
import json
import glob
import cohere
from pypdf import PdfReader

# ---- 設定 ----------------------------------------------------------------
PAPERS_DIR = "papers"          # PDFを置くフォルダ
STORE_PATH = "store.json"      # 保存先
EMBED_MODEL = "embed-v4.0"     # 埋め込みモデル（多言語対応）
CHUNK_SIZE = 1000              # 1チャンクあたりのおおよその文字数
CHUNK_OVERLAP = 150            # チャンク間の重なり（文脈を切らないため）
EMBED_BATCH = 96               # 一度にEmbedへ送るチャンク数
# -------------------------------------------------------------------------


def get_client():
    api_key = os.environ.get("CO_API_KEY")
    if not api_key:
        sys.exit("エラー: 環境変数 CO_API_KEY が設定されていません。"
                 "\n  export CO_API_KEY=あなたのキー を実行してください。")
    return cohere.ClientV2(api_key=api_key)


def extract_text(pdf_path):
    """PDFから全ページのテキストを取り出す。"""
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """テキストを重なりつきの断片に分割する。"""
    text = " ".join(text.split())  # 余分な空白・改行を圧縮
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def embed_chunks(co, chunks):
    """チャンクのリストをベクトル化して返す。"""
    vectors = []
    for i in range(0, len(chunks), EMBED_BATCH):
        batch = chunks[i:i + EMBED_BATCH]
        resp = co.embed(
            model=EMBED_MODEL,
            texts=batch,
            input_type="search_document",  # 保存する文書側の指定
            embedding_types=["float"],
        )
        vectors.extend(resp.embeddings.float)
        print(f"  ... 埋め込み {min(i + EMBED_BATCH, len(chunks))}/{len(chunks)}")
    return vectors


def main():
    co = get_client()

    pdf_paths = sorted(glob.glob(os.path.join(PAPERS_DIR, "*.pdf")))
    if not pdf_paths:
        sys.exit(f"エラー: {PAPERS_DIR}/ にPDFが見つかりません。"
                 f"\n  {PAPERS_DIR}/ フォルダを作り、論文PDFを入れてください。")

    records = []
    for pdf_path in pdf_paths:
        name = os.path.basename(pdf_path)
        print(f"[取り込み] {name}")
        text = extract_text(pdf_path)
        chunks = chunk_text(text)
        if not chunks:
            print(f"  （テキストを抽出できませんでした。スキャンPDFかもしれません）")
            continue
        print(f"  {len(chunks)} チャンクに分割")
        vectors = embed_chunks(co, chunks)
        for idx, (chunk, vec) in enumerate(zip(chunks, vectors)):
            records.append({
                "source": name,
                "chunk_id": idx,
                "text": chunk,
                "embedding": vec,
            })

    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)

    print(f"\n完了: {len(records)} チャンクを {STORE_PATH} に保存しました。")
    print("次は `python ask.py` で質問してみてください。")


if __name__ == "__main__":
    main()
