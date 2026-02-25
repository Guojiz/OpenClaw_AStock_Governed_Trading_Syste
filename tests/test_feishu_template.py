from datetime import datetime
from zoneinfo import ZoneInfo

from runtime.feishu import render_status_template
from runtime.session import get_cn_market_session


def test_template_render_by_session_contains_session_code():
    session = get_cn_market_session(datetime(2026, 1, 5, 9, 45, tzinfo=ZoneInfo("Asia/Shanghai")))
    text = render_status_template(
        session=session,
        task_id="task-123",
        platform_status={"bigquant": "通过", "ifind_qwen": "通过", "ifind_deepseek": "通过"},
        timestamp="2026-01-05T09:45:00",
    )
    assert "market_open" in text
    assert "task_id=task-123" in text
