import json
import os
from datetime import datetime

STORE_PATH = os.path.join(os.path.dirname(__file__), "..", "sessions.json")


def _load() -> list:
    if not os.path.isfile(STORE_PATH):
        return []
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save(data: list) -> None:
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_entry(module: str, prompt: str, response: str) -> None:
    entries = _load()
    entries.append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "module": module,
        "prompt": prompt,
        "response": response,
    })
    _save(entries)


def get_history(module: str | None = None, limit: int = 50) -> list:
    entries = _load()
    if module:
        entries = [e for e in entries if e.get("module") == module]
    return entries[-limit:]


def clear_history() -> None:
    _save([])
