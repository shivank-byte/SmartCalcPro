"""
history.py
-----------
Saves and loads calculation history to a local text file so it persists
between sessions.
"""

from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path(__file__).parent / "history.txt"


def add_entry(expression: str, result: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {expression} = {result}\n"
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def load_entries() -> list[str]:
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def clear_history() -> None:
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
