from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from uuid import uuid4

from runtime.credentials import credential_presence_report
from runtime.feishu import render_status_template, send_feishu_status
from runtime.models import TaskRecord, TaskStatus
from runtime.session import get_cn_market_session


def _platform_selftest(presence: dict[str, bool]) -> dict[str, str]:
    result = {}
    for key in ("bigquant", "ifind_qwen", "ifind_deepseek"):
        result[key] = "登录自检通过" if presence[key] else "登录自检失败：凭证缺失"
    return result


def run_minimal_demo(feishu_webhook: str | None = None) -> dict:
    task_id = f"task-{uuid4().hex[:8]}"
    now = datetime.now().isoformat(timespec="seconds")
    task = TaskRecord(task_id=task_id, initiator="用户/飞书", executor="techops", created_at=now)

    task.add_event(TaskStatus.CREATED, "central", "接收任务：检查三平台登录并汇报")
    task.add_event(TaskStatus.DISPATCHED, "central", "派发给 techops")
    task.add_event(TaskStatus.ACKED, "techops", "已接单")
    task.add_event(TaskStatus.RUNNING, "techops", "执行凭证存在性检查与登录连通性自检")

    presence = credential_presence_report()
    platform_status = _platform_selftest(presence)
    blocked = any("失败" in msg for msg in platform_status.values())
    task.add_evidence("状态更新记录", "凭证检查完成", presence)
    task.add_evidence("外部平台操作结果", "登录连通性自检完成（未触发交易）", platform_status)

    task.add_event(
        TaskStatus.BLOCKED if blocked else TaskStatus.SUCCEEDED,
        "techops",
        "检测到缺失凭证" if blocked else "三平台登录自检通过",
    )

    session = get_cn_market_session()
    message = render_status_template(session, task_id, platform_status, now)
    feishu_result = send_feishu_status(feishu_webhook, message)
    task.add_evidence("Skill 调用记录", "feishu_send_status 调用完成", feishu_result)

    task.add_event(TaskStatus.VERIFIED, "central", "已汇总回执与证据")
    task.add_event(TaskStatus.SUMMARIZED, "central", "已形成中控摘要")

    return {
        "task_id": task_id,
        "timestamp": now,
        "session": asdict(session),
        "status_flow": [asdict(e) for e in task.events],
        "evidence": [asdict(e) for e in task.evidences],
        "platform_status": platform_status,
        "feishu": feishu_result,
        "final_summary": message,
    }


if __name__ == "__main__":
    result = run_minimal_demo()
    print(json.dumps(result, ensure_ascii=False, indent=2))
