from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import replace
from datetime import datetime
from typing import Iterable, List

from ..domain.task import Task


class Rule(ABC):
    @abstractmethod
    def apply(self, task: Task, now: datetime) -> Task:
        """Return (possibly) updated task"""
        raise NotImplementedError


class OverdueRule(Rule):
    def apply(self, task: Task, now: datetime) -> Task:
        overdue = bool(task.due_date and task.due_date < now and task.status != "DONE")
        if task.is_overdue != overdue:
            return replace(task, is_overdue=overdue)
        return task


class BacklogAutoReadyRule(Rule):
    def apply(self, task: Task, now: datetime) -> Task:
        if task.status != "BACKLOG":
            return task

        title_ok = bool(task.title and task.title.strip())
        priority_ok = 1 <= int(task.priority) <= 5

        if title_ok and priority_ok:
            return replace(task, status="READY")
        return task


class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def apply_all(self, tasks: Iterable[Task], now: datetime) -> List[Task]:
        out: List[Task] = []
        for t in tasks:
            for r in self.rules:
                t = r.apply(t, now)
            out.append(t)
        return out
