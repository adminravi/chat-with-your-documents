"""Ingest one or more documents into the local Chroma store.

Usage:
    python ingest.py file1.pdf file2.docx notes.md
"""
import sys
from pathlib import Path

from loaders import load, LOADERS
from chunker import chunk
from store import open_store, add_chunks


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: python ingest.py <file1> [<file2> ...]")
        print(f"Supported file types: {', '.join(sorted(LOADERS.keys()))}")
        return 1

    collection = open_store()
    for arg in argv:
        path = Path(arg)
        if not path.exists():
            print(f"Skipping {arg!r}: file not found")
            continue
        if path.suffix.lower() not in LOADERS:
            print(f"Skipping {arg!r}: unsupported type {path.suffix}")
            continue

        print(f"Loading {path.name} ...", end=" ", flush=True)
        text = load(path)
        print(f"{len(text):,} chars")

        print(f"Chunking ...", end=" ", flush=True)
        chunks = chunk(text)
        print(f"{len(chunks)} chunks")

        print(f"Embedding + storing ...", end=" ", flush=True)
        add_chunks(collection, chunks, source=path.name)
        print("done.")

    print(f"\nStore now holds {collection.count()} chunks total.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
