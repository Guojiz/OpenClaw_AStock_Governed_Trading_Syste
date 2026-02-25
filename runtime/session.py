from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class SessionState:
    code: str
    label: str


def get_cn_market_session(now: datetime | None = None) -> SessionState:
    now = now or datetime.now(ZoneInfo("Asia/Shanghai"))
    t = now.time()

    if time(9, 0) <= t < time(9, 30):
        return SessionState("pre_market", "盘前")
    if time(9, 30) <= t < time(11, 30):
        return SessionState("market_open", "盘中")
    if time(11, 30) <= t < time(13, 0):
        return SessionState("midday_break", "午间休市")
    if time(13, 0) <= t < time(15, 0):
        return SessionState("market_open", "盘中")
    if time(15, 0) <= t < time(20, 0):
        return SessionState("after_close", "盘后治理")
    return SessionState("night_off_market", "夜间非交易时段")
