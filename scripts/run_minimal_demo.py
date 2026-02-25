from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.credentials import load_credentials
from runtime.minimal_demo import run_minimal_demo

if __name__ == "__main__":
    creds = load_credentials()
    print(run_minimal_demo(feishu_webhook=creds.feishu_webhook))
