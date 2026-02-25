from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    CREATED = "CREATED"
    DISPATCHED = "DISPATCHED"
    ACKED = "ACKED"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    VERIFIED = "VERIFIED"
    SUMMARIZED = "SUMMARIZED"


@dataclass
class Evidence:
    kind: str
    summary: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskEvent:
    status: TaskStatus
    actor: str
    timestamp: str
    note: str


@dataclass
class TaskRecord:
    task_id: str
    initiator: str
    executor: str
    created_at: str
    events: list[TaskEvent] = field(default_factory=list)
    evidences: list[Evidence] = field(default_factory=list)

    def add_event(self, status: TaskStatus, actor: str, note: str) -> None:
        self.events.append(
            TaskEvent(
                status=status,
                actor=actor,
                timestamp=datetime.now().isoformat(timespec="seconds"),
                note=note,
            )
        )

    def add_evidence(self, kind: str, summary: str, detail: dict[str, Any]) -> None:
        self.evidences.append(Evidence(kind=kind, summary=summary, detail=detail))
