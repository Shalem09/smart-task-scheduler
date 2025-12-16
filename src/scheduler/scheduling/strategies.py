#strategies.py

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from ..domain.task import Task

class SchedulingStrategy(ABC):
    @abstractmethod
    def select_next(self, tasks: List[Task], now: datetime) -> Optional[Task]:
        pass


class HighestPriorityFirst(SchedulingStrategy):
    def select_next(self, tasks: List[Task], now: datetime) -> Optional[Task]:
        eligible = [
            t for t in tasks
            if t.status in ("READY", "IN_PROGRESS")
        ]
        if not eligible:
            return None

        return sorted(
            eligible,
            key=lambda t: t.priority,
            reverse=True
        )[0]
