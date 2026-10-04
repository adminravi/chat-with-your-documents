"""A thin wrapper around a local Chroma collection.

Chroma does three things for us:
  1. Turns each chunk into a 384-number list (an "embedding") using its
     built-in default model — no API key needed, no internet needed after
     the first run that downloads the model.
  2. Saves the chunks + embeddings + source filename to a folder on disk.
  3. For any question, returns the chunks whose embeddings are closest
     to the question's embedding (cosine similarity under the hood).

Everything lives in ./chroma_db/ by default. Delete the folder and the
collection resets.
"""
from pathlib import Path

import chromadb

DEFAULT_DB_PATH = "./chroma_db"
COLLECTION_NAME = "my_documents"


def open_store(db_path: str = DEFAULT_DB_PATH):
    """Open (or create) the on-disk Chroma collection and return it."""
    client = chromadb.PersistentClient(path=db_path)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_chunks(collection, chunks: list[str], source: str) -> None:
    """Add a list of text chunks to the collection, tagged with their source."""
    if not chunks:
        return
    # One id per chunk — stable, so re-ingesting the same file replaces,
    # not duplicates. Format: "<source>::<index>".
    ids = [f"{source}::{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]
    collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)


def query(collection, question: str, k: int = 4) -> list[dict]:
    """Return the `k` chunks most relevant to `question`.

    Each result dict has: text, source, chunk_index, distance.
    """
    results = collection.query(query_texts=[question], n_results=k)
    out = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        out.append({
            "text": doc,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": dist,
        })
    return out


def reset(db_path: str = DEFAULT_DB_PATH) -> None:
    """Delete everything in the collection (useful during development)."""
    import shutil
    p = Path(db_path)
    if p.exists():
        shutil.rmtree(p)
