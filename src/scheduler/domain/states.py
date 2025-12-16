from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Optional
from .task import Task

class InvalidTransition(Exception):
    pass

class TaskState(ABC):
    name: str

    def start(self, task: Task) -> Task:
        raise InvalidTransition(f"Cannot start from {task.status}")

    def block(self, task: Task, reason: str) -> Task:
        raise InvalidTransition(f"Cannot block from {task.status}")

    def unblock(self, task: Task) -> Task:
        raise InvalidTransition(f"Cannot unblock from {task.status}")

    def complete(self, task: Task) -> Task:
        raise InvalidTransition(f"Cannot complete from {task.status}")

class BacklogState(TaskState):
    name = "BACKLOG"

    def start(self, task: Task) -> Task:
        return replace(task, status="IN_PROGRESS")

    def block(self, task: Task, reason: str) -> Task:
        return replace(task, status="BLOCKED", blocked_reason=reason)

class ReadyState(TaskState):
    name = "READY"

    def start(self, task: Task) -> Task:
        return replace(task, status="IN_PROGRESS")

    def block(self, task: Task, reason: str) -> Task:
        return replace(task, status="BLOCKED", blocked_reason=reason)

class InProgressState(TaskState):
    name = "IN_PROGRESS"

    def block(self, task: Task, reason: str) -> Task:
        return replace(task, status="BLOCKED", blocked_reason=reason)

    def complete(self, task: Task) -> Task:
        return replace(task, status="DONE", blocked_reason=None)

class BlockedState(TaskState):
    name = "BLOCKED"

    def unblock(self, task: Task) -> Task:
        return replace(task, status="READY", blocked_reason=None)

class DoneState(TaskState):
    name = "DONE"

def get_state(status: str) -> TaskState:
    mapping = {
        "BACKLOG": BacklogState(),
        "READY": ReadyState(),
        "IN_PROGRESS": InProgressState(),
        "BLOCKED": BlockedState(),
        "DONE": DoneState(),
    }
    try:
        return mapping[status]
    except KeyError:
        raise ValueError(f"Unknown status: {status}")
