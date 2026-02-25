from __future__ import annotations

import json
from pathlib import Path


def load_agents_registry(path: str = "agents/agents.json") -> list[dict]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return raw["agents"]
