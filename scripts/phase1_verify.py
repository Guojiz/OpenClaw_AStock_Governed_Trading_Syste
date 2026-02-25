from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.agents_registry import load_agents_registry
from runtime.credentials import credential_presence_report, load_credentials
from runtime.minimal_demo import run_minimal_demo
from runtime.session import get_cn_market_session


if __name__ == "__main__":
    agents = load_agents_registry()
    creds = load_credentials()
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "agents": [
            {
                "name": a["name"],
                "skills": a["skills"],
                "sandbox": a["sandbox"],
                "workspace": a["workspace"],
            }
            for a in agents
        ],
        "credential_presence": credential_presence_report(),
        "current_session": get_cn_market_session().__dict__,
        "feishu_chain": "Central -> Comms_Reports(feishu_send_status) -> Feishu webhook",
        "minimal_demo": run_minimal_demo(feishu_webhook=creds.feishu_webhook),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
