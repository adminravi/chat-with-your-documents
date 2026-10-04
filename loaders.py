"""Document loaders — read a file from disk and return plain text.

One function per file type, so a beginner can read any single function
and understand everything it does. The dispatcher at the bottom picks
the right loader by file extension.
"""
from pathlib import Path

from pypdf import PdfReader
import docx


def load_pdf(path: Path) -> str:
    """Read a .pdf file and return the plain text of every page, joined."""
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)


def load_docx(path: Path) -> str:
    """Read a .docx file and return the plain text of every paragraph."""
    document = docx.Document(str(path))
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def load_txt(path: Path) -> str:
    """Read a .txt or .md file and return its contents."""
    return path.read_text(encoding="utf-8")


LOADERS = {
    ".pdf": load_pdf,
    ".docx": load_docx,
    ".txt": load_txt,
    ".md": load_txt,
}


def load(path: str | Path) -> str:
    """Pick the right loader for the file extension and run it.

    Raises ValueError if the extension is not one of .pdf, .docx, .txt, .md.
    """
    p = Path(path)
    loader = LOADERS.get(p.suffix.lower())
    if loader is None:
        supported = ", ".join(sorted(LOADERS.keys()))
        raise ValueError(
            f"Unsupported file type {p.suffix!r}. Supported: {supported}"
        )
    return loader(p)
