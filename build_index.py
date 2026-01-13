#!/usr/bin/env python3
"""
build_index.py
Builds a local RAG index using:
- sentence-transformers for embeddings (local, no API keys)
- ChromaDB for storage (persistent)

Run:
  python3 build_index.py

Output:
  ./chroma_db/  (persistent vector store)
"""

import os
import glob
import hashlib
from typing import List, Dict

import chromadb
from sentence_transformers import SentenceTransformer


# -----------------------------
# Config
# -----------------------------
KB_DIR = "kb_docs"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "fincorp_kb"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# -----------------------------
# Helpers
# -----------------------------
def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()[:16]


def load_docs(kb_dir: str) -> List[Dict]:
    docs: List[Dict] = []

    print(f"📂 Scanning directory: {kb_dir}")

    for path in glob.glob(os.path.join(kb_dir, "*")):
        if not os.path.isfile(path):
            continue

        if not path.lower().endswith((".md", ".txt")):
            continue

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

        print(f"📄 Loaded {os.path.basename(path)} ({len(raw_text)} chars)")

        if len(raw_text) == 0:
            continue

        docs.append(
            {
                "path": path,
                "filename": os.path.basename(path),
                "text": raw_text,
                "hash": file_hash(path),
            }
        )

    return docs


def chunk_text(text: str) -> List[str]:
    chunks: List[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + CHUNK_SIZE, n)
        chunk = text[start:end]

        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)

        start = end - CHUNK_OVERLAP
        if start < 0:
            start = 0
        if end == n:
            break

    return chunks


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    print("📚 Loading documents...")

    if not os.path.isdir(KB_DIR):
        raise SystemExit(f"❌ KB directory not found: {KB_DIR}")

    docs = load_docs(KB_DIR)

    if not docs:
        raise SystemExit("❌ No documents found (or all empty).")

    print("CHECKPOINT 1: after load_docs")

    print("🧠 Loading local embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("CHECKPOINT 2: before chunking")

    texts: List[str] = []
    metadatas: List[Dict] = []
    ids: List[str] = []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            cid = f"{doc['filename']}::{doc['hash']}::{i}"
            ids.append(cid)
            texts.append(chunk)
            metadatas.append(
                {
                    "source_file": doc["filename"],
                    "source_path": doc["path"],
                    "chunk_index": i,
                }
            )

    print(f"✂️ Created {len(texts)} chunks")

    print("📐 Creating embeddings locally...")
    embeddings = model.encode(texts, show_progress_bar=True)

    print("CHECKPOINT 3: before chroma write")

    print("💾 Storing in ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Fresh rebuild for demo simplicity
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
    )

    print("🎉 RAG index built successfully!")
    print(f"   Collection: {COLLECTION_NAME}")
    print(f"   Stored at: {CHROMA_DIR}/")


if __name__ == "__main__":
    main()