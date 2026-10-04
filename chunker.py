"""Split a long text into overlapping chunks of ~N words.

Why overlap? If a sentence falls on a chunk boundary, part of its meaning
lives in two chunks — so a question that quotes the sentence can still
match. 50 words of overlap is enough in practice for 500-word chunks.

A chunk is just a slice of words joined by spaces. We don't try to split
on sentence boundaries here — Chroma's embedder handles slightly ragged
chunks fine, and keeping the code simple is more valuable to the reader
than a 5% retrieval quality bump.
"""


def chunk(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks of about `size` words each.

    Returns a list of chunk strings in order. The last chunk may be shorter.
    Overlap must be smaller than size (we assert this to catch beginner typos).
    """
    assert overlap < size, "overlap must be smaller than chunk size"
    words = text.split()
    if not words:
        return []
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        piece = words[start : start + size]
        if not piece:
            break
        chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks
