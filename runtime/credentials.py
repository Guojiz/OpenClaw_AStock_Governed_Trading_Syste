from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CredentialPair:
    username: str | None
    password: str | None

    @property
    def present(self) -> bool:
        return bool(self.username and self.password)


@dataclass
class SystemCredentials:
    bigquant: CredentialPair
    ifind_qwen: CredentialPair
    ifind_deepseek: CredentialPair
    feishu_webhook: str | None


def _load_simple_yaml(path: Path) -> dict:
    """仅支持两层键值结构，满足本项目 secrets.yaml 示例。"""
    if not path.exists():
        return {}

    data: dict[str, dict[str, str] | str] = {}
    current: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not raw_line.startswith(" ") and line.endswith(":"):
            current = line[:-1]
            data[current] = {}
            continue
        if ":" in line and current:
            key, value = [x.strip() for x in line.split(":", 1)]
            value = value.strip('"').strip("'")
            if isinstance(data[current], dict):
                data[current][key] = value
    return data


def load_credentials() -> SystemCredentials:
    secrets = _load_simple_yaml(Path("secrets.yaml"))

    def pick(section: str, env_user: str, env_pwd: str) -> CredentialPair:
        s = secrets.get(section, {}) if isinstance(secrets.get(section), dict) else {}
        return CredentialPair(
            username=os.getenv(env_user) or s.get("username"),
            password=os.getenv(env_pwd) or s.get("password"),
        )

    feishu_cfg = secrets.get("feishu", {}) if isinstance(secrets.get("feishu"), dict) else {}
    return SystemCredentials(
        bigquant=pick("bigquant", "BIGQUANT_USERNAME", "BIGQUANT_PASSWORD"),
        ifind_qwen=pick("ifind_qwen", "IFIND_QWEN_USERNAME", "IFIND_QWEN_PASSWORD"),
        ifind_deepseek=pick("ifind_deepseek", "IFIND_DEEPSEEK_USERNAME", "IFIND_DEEPSEEK_PASSWORD"),
        feishu_webhook=os.getenv("FEISHU_WEBHOOK") or feishu_cfg.get("webhook"),
    )


def credential_presence_report() -> dict[str, bool]:
    creds = load_credentials()
    return {
        "bigquant": creds.bigquant.present,
        "ifind_qwen": creds.ifind_qwen.present,
        "ifind_deepseek": creds.ifind_deepseek.present,
        "feishu_webhook": bool(creds.feishu_webhook),
    }
