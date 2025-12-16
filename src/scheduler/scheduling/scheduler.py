#scheduler.py

from datetime import datetime
from .strategies import SchedulingStrategy
from ..domain.task import Task


class Scheduler:
    def __init__(self, strategy: SchedulingStrategy):
        self.strategy = strategy

    def next_task(self, tasks: list[Task]) -> Task | None:
        return self.strategy.select_next(tasks, datetime.now())
