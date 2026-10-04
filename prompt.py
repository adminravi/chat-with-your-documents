"""Build the prompt we send to Claude.

The pattern is called "stuffed context": we glue the retrieved chunks
into the user message, with a strict instruction to answer only from
them and to cite the source filenames.

Why strict? Without the "only from context" rule, Claude will cheerfully
fall back to its training data and answer from general knowledge. That
would defeat the whole point of RAG — we would never know whether an
answer came from the reader's document or from Claude's memory.
"""


SYSTEM_PROMPT = """You are a careful assistant that answers questions \
strictly from the context provided in the user's message.

Rules:
1. Use ONLY the facts in the <context> blocks. Do not use outside knowledge.
2. If the context does not contain the answer, say exactly: \
"I could not find that in the documents you gave me."
3. At the end of every answer, cite the sources you used on a new line, \
in the form: [source: filename.pdf]
4. Be concise. Prefer short, direct answers over long summaries."""


def build_user_message(question: str, hits: list[dict]) -> str:
    """Glue the retrieved chunks into a single user message for Claude."""
    blocks = []
    for i, h in enumerate(hits, start=1):
        blocks.append(
            f"<context source=\"{h['source']}\" chunk=\"{h['chunk_index']}\">\n"
            f"{h['text']}\n"
            f"</context>"
        )
    context_text = "\n\n".join(blocks)
    return f"{context_text}\n\nQuestion: {question}"
