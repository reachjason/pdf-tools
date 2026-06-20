"""Run index: records every tool invocation so you have an audit trail.

The index is a JSON array stored alongside the outputs (and gitignored), since
it references local file paths. Each record describes one tool run.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Repo root is two levels up from this file (pdftools/index.py -> repo root).
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "outputs"
INDEX_PATH = OUTPUT_DIR / "index.json"


def ensure_output_dir() -> Path:
    """Make sure the outputs directory exists and return it."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def load_index() -> list[dict[str, Any]]:
    """Load the index, returning an empty list if it doesn't exist yet."""
    if not INDEX_PATH.exists():
        return []
    try:
        with INDEX_PATH.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def add_record(record: dict[str, Any]) -> dict[str, Any]:
    """Append a record to the index and persist it.

    A timestamp is added automatically if the caller didn't provide one.
    """
    ensure_output_dir()
    record.setdefault("timestamp", datetime.now(timezone.utc).isoformat())

    index = load_index()
    index.append(record)
    with INDEX_PATH.open("w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2)
        fh.write("\n")
    return record
