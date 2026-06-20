"""Command-line entry point: `python -m pdftools <tool> [args...]`."""

from __future__ import annotations

import sys

from . import __version__
from .index import add_record
from .tools import TOOLS


def _usage() -> str:
    lines = [
        f"pdf-tools {__version__}",
        "",
        "Usage: pdftools <tool> [args...]",
        "",
        "Available tools:",
    ]
    for name, module in TOOLS.items():
        lines.append(f"  {name:<12} {getattr(module, 'HELP', '')}")
    lines.append("")
    lines.append("Run a tool with -h for its options, e.g. pdftools pdf2txt -h")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in ("-h", "--help"):
        print(_usage())
        return 0
    if argv[0] in ("-v", "--version"):
        print(__version__)
        return 0

    tool_name, tool_args = argv[0], argv[1:]
    module = TOOLS.get(tool_name)
    if module is None:
        print(f"Unknown tool: {tool_name}\n", file=sys.stderr)
        print(_usage(), file=sys.stderr)
        return 2

    try:
        record = module.run(tool_args)
    except Exception as exc:  # noqa: BLE001 - record failure then surface it
        add_record({"tool": tool_name, "status": "error", "error": str(exc)})
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    add_record(record)
    print(f"OK: {record.get('output', '(no output)')}")
    if "pages" in record and "chars" in record:
        print(f"     {record['pages']} pages, {record['chars']} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
