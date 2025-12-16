from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Task:
    id: int
    title: str
    priority: int
    created_at: datetime
    due_date: Optional[datetime] = None
    is_overdue: bool = False
    tags: List[str] = field(default_factory=list)
    status: str = "BACKLOG"
    blocked_reason: Optional[str] = None