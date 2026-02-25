from __future__ import annotations

from datetime import datetime
from urllib.error import URLError
from urllib.request import Request, urlopen
import json

from runtime.session import SessionState


def render_status_template(
    session: SessionState,
    task_id: str,
    platform_status: dict[str, str],
    timestamp: str,
) -> str:
    lines = [
        "[中央] 投资中控状态播报",
        f"1) 当前交易时段：{session.label}({session.code})",
        "2) 主执行平台状态：",
        f"   - BigQuant：{platform_status.get('bigquant', '状态缺失')}",
        "3) 两党策略验证平台状态：",
        f"   - Qwen党 iFinD：{platform_status.get('ifind_qwen', '状态缺失')}",
        f"   - DeepSeek党 iFinD：{platform_status.get('ifind_deepseek', '状态缺失')}",
        "4) Watchdog：待机（本演示未启用盘中应急）",
        "5) 风险/异常：见平台状态字段",
        "6) 治理附注：支持率模块待下一阶段接入",
        f"7) task_id={task_id} | timestamp={timestamp}",
    ]
    return "\n".join(lines)


def send_feishu_status(webhook: str | None, text: str) -> dict:
    if not webhook:
        return {
            "sent": False,
            "channel": "feishu_webhook",
            "reason": "缺少 FEISHU_WEBHOOK，未发送",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

    body = json.dumps({"msg_type": "text", "content": {"text": text}}).encode("utf-8")
    req = Request(webhook, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=8) as resp:
            payload = resp.read().decode("utf-8")[:300]
            return {
                "sent": True,
                "channel": "feishu_webhook",
                "status_code": resp.status,
                "body": payload,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }
    except URLError as e:
        return {
            "sent": False,
            "channel": "feishu_webhook",
            "reason": str(e),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
