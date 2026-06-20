"""Tool: pdf2txt -- extract text from a PDF into a .txt file."""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader

from ..index import OUTPUT_DIR, ensure_output_dir

NAME = "pdf2txt"
HELP = "Extract text from a PDF into a .txt file"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=f"pdftools {NAME}", description=HELP)
    parser.add_argument("input", type=Path, help="Path to the input PDF")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output .txt path (default: outputs/<input-name>.txt)",
    )
    parser.add_argument(
        "--page-separator",
        default="\n\n",
        help="String inserted between pages (default: blank line)",
    )
    return parser


def run(argv: list[str]) -> dict:
    """Extract text and return an index record describing the run."""
    args = _build_parser().parse_args(argv)

    input_path: Path = args.input.expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_path}")

    ensure_output_dir()
    if args.output is not None:
        output_path = args.output.expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = OUTPUT_DIR / f"{input_path.stem}.txt"

    reader = PdfReader(str(input_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = args.page_separator.join(pages)

    output_path.write_text(text, encoding="utf-8")

    return {
        "tool": NAME,
        "input": str(input_path),
        "output": str(output_path),
        "pages": len(reader.pages),
        "words": len(text.split()),
        "chars": len(text),
        "status": "ok",
    }
