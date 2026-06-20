"""Tool registry.

Each tool is a module exposing:
  NAME:  str  -- the subcommand used on the CLI
  HELP:  str  -- one-line description
  run(argv: list[str]) -> dict  -- does the work, returns an index record

To add a new tool: create a module under pdftools/tools/, give it those three
names, and register it in TOOLS below.
"""

from __future__ import annotations

from . import pdf_to_txt

# Map subcommand name -> module. Add new tools here as the toolkit evolves.
TOOLS = {
    pdf_to_txt.NAME: pdf_to_txt,
}
