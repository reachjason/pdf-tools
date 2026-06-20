# pdf-tools

A small, **local** toolkit for working with PDFs — no third-party services, no
uploads. Built to evolve: each tool is one self-contained module, and every run
is recorded in an index so you have an audit trail of what's been processed.

## Tools

| Tool | Description |
|------|-------------|
| `pdf2txt` | Extract text from a PDF into a `.txt` file |

More tools (split, merge, OCR, PDF→images, …) can be dropped in over time — see
[Adding a tool](#adding-a-tool).

## Install

Install once with [pipx](https://pipx.pypa.io/) — it puts a global `pdftools`
command on your PATH in an isolated environment (no venv juggling):

```bash
pipx install --editable .
```

`--editable` means new subtools added to the registry are available immediately,
with no reinstall.

> Prefer not to install? You can still run it from the repo with
> `python -m pdftools <tool> ...` (requires `pip install -r requirements.txt`).

## Usage

```bash
# Extract text -> outputs/<name>.txt
pdftools pdf2txt path/to/document.pdf

# Custom output path
pdftools pdf2txt document.pdf -o /tmp/out.txt

# List tools / get help
pdftools --help
pdftools pdf2txt --help
```

## Outputs & the index

- Extracted files are written to `outputs/` (created on first run).
- Every run appends a record to `outputs/index.json`:

  ```json
  {
    "tool": "pdf2txt",
    "input": "/abs/path/document.pdf",
    "output": "/abs/path/outputs/document.txt",
    "pages": 12,
    "chars": 18432,
    "status": "ok",
    "timestamp": "2026-06-20T17:00:00+00:00"
  }
  ```

- `outputs/` (including the index) is **gitignored** — only the tool code is
  pushed to GitHub.

## Notes

- `pdf2txt` uses [`pypdf`](https://pypdf.readthedocs.io/), which extracts text
  from *digital* PDFs. It does **not** OCR scanned/image-only PDFs — that's a
  candidate for a future tool.

## Adding a tool

1. Create `pdftools/tools/<your_tool>.py` exposing `NAME`, `HELP`, and
   `run(argv: list[str]) -> dict` (the dict is recorded in the index).
2. Register it in `pdftools/tools/__init__.py` (`TOOLS`).
3. Done — because the install is editable, it's instantly available as
   `pdftools <NAME>`. No reinstall needed.
