"""Interactive chat loop against the ingested documents.

Usage:
    python chat.py

Prerequisites:
    - At least one document ingested via `ingest.py`.
    - ANTHROPIC_API_KEY set in your environment.
"""
import os
import sys

from anthropic import Anthropic

from store import open_store, query
from prompt import SYSTEM_PROMPT, build_user_message


MODEL = "claude-sonnet-4-6"
TOP_K = 4


def answer(client: Anthropic, collection, question: str) -> str:
    hits = query(collection, question, k=TOP_K)
    if not hits:
        return "The document store is empty — run `ingest.py` first."
    user_message = build_user_message(question, hits)
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY before running chat.py.")
        return 1

    collection = open_store()
    if collection.count() == 0:
        print("No documents in the store yet. Run `ingest.py <file>` first.")
        return 1

    client = Anthropic()
    print(f"Loaded {collection.count()} chunks. Ask a question (or 'quit').\n")

    try:
        while True:
            question = input("you > ").strip()
            if not question:
                continue
            if question.lower() in {"quit", "exit", "q"}:
                print("Bye.")
                break
            print()
            print(answer(client, collection, question))
            print()
    except (KeyboardInterrupt, EOFError):
        print("\nBye.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
