# Chat with Your Documents

Companion code for the book **"Build AI Chatbots with RAG"** by Ravi Verma.

A tiny desktop assistant that reads your own PDFs, Word files, and text notes, and answers questions about them. Everything runs on your laptop. The only paid service is Anthropic's Claude API — and you can get started for free with Anthropic's trial credits.

**Six files, about 150 lines of code.** You can read every line.

---

## What you need

- Python **3.10 or newer** (3.12 recommended).
- An Anthropic API key — https://console.anthropic.com/
- A document to chat with (any PDF, DOCX, TXT, or MD file you own).

Everything else installs with one command.

---

## Setup

### 1. Install `uv` (the Python package manager we'll use)

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS (Terminal):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen your terminal after installing so the `uv` command is on your PATH.

### 2. Clone this repo and enter the folder

```bash
git clone https://github.com/adminravi/chat-with-your-documents.git
cd chat-with-your-documents
```

### 3. Create a virtual environment and install packages

```bash
uv venv .venv
```

Then activate it:

**Windows:**
```powershell
.venv\Scripts\activate
```

**macOS:**
```bash
source .venv/bin/activate
```

Now install the four packages:

```bash
uv pip install -r requirements.txt
```

### 4. Add your API key

Copy the sample file:

**Windows:**
```powershell
copy .env.example .env
```

**macOS:**
```bash
cp .env.example .env
```

Open `.env` in any text editor and paste your Anthropic key where it says `sk-ant-replace-me`. Save and close.

Load it into your current shell:

**Windows (PowerShell):**
```powershell
Get-Content .env | ForEach-Object { if ($_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2]) } }
```

**macOS:**
```bash
set -a; source .env; set +a
```

---

## Usage

### Ingest one or more documents

```bash
python ingest.py path/to/your_file.pdf
```

You can pass multiple files at once, mixing types:

```bash
python ingest.py manual.pdf notes.md meeting.docx
```

The first run downloads a small embedding model (~79 MB). This happens once, cached on your machine. Future ingests are fast.

### Chat with your documents

```bash
python chat.py
```

Ask a question, press Enter. Type `quit` to exit.

Example:

```
you > What are the five key principles in chapter 3?

The five principles in chapter 3 are:
1. ...
2. ...
...

[source: your_file.pdf]
```

Every answer cites the source file it drew from. If the answer isn't in your documents, the assistant will say so instead of making something up.

### Reset the store

Delete the `chroma_db/` folder. The next `ingest.py` run starts fresh.

---

## What's in each file

| File | What it does |
|------|---------------|
| `loaders.py` | Reads a .pdf / .docx / .txt / .md file and returns plain text. |
| `chunker.py` | Splits text into overlapping ~500-word chunks. |
| `store.py` | Thin wrapper around a local Chroma vector collection. |
| `prompt.py` | Builds the "answer only from this context, and cite" prompt. |
| `ingest.py` | CLI entry — ingests one or more files. |
| `chat.py` | CLI entry — interactive question/answer loop. |

Open any file. There's nothing hidden.

---

## License

MIT. See [LICENSE](LICENSE).
