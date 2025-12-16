from datetime import datetime
from collections import Counter
from ..domain.task import Task
from ..persistence.repository import TaskRepository
from ..scheduling.scheduler import Scheduler
from ..domain.states import get_state, InvalidTransition
from ..rules.rules import RuleEngine, OverdueRule, BacklogAutoReadyRule


class TaskService:
    def __init__(self, repo: TaskRepository, scheduler: Scheduler):
        self.repo = repo
        self.scheduler = scheduler
        self.rule_engine = RuleEngine([OverdueRule(), BacklogAutoReadyRule()])

    def add_task(self, title: str, priority: int):
        tasks = self.repo.list_all()
        task = Task(
            id=self.repo.next_id(),
            title=title,
            priority=priority,
            created_at=datetime.now(),
            status="READY"
        )
        tasks.append(task)
        self.repo.save_all(tasks)
        return task

    def list_tasks(self):
        tasks = self.repo.list_all()
        tasks = self.rule_engine.apply_all(tasks, datetime.now())
        return tasks

    def next_task(self):
        tasks = self.repo.list_all()
        tasks = self.rule_engine.apply_all(tasks, datetime.now())
        return self.scheduler.next_task(tasks)
    
    def start_task(self, task_id: int):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        new_task = get_state(task.status).start(task)
        self.repo.update(new_task)
        return new_task

    def block_task(self, task_id: int, reason: str):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        new_task = get_state(task.status).block(task, reason)
        self.repo.update(new_task)
        return new_task

    def unblock_task(self, task_id: int):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        new_task = get_state(task.status).unblock(task)
        self.repo.update(new_task)
        return new_task

    def complete_task(self, task_id: int):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        new_task = get_state(task.status).complete(task)
        self.repo.update(new_task)
        return new_task
    
    def set_due_date(self, task_id: int, due_date: datetime | None):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        from dataclasses import replace
        updated = replace(task, due_date=due_date)

        self.repo.update(updated)
        return updated
    
    def stats(self) -> dict:
        tasks = self.repo.list_all()
        tasks = self.rule_engine.apply_all(tasks, datetime.now())

        status_counts = Counter(t.status for t in tasks)
        overdue_count = sum(1 for t in tasks if getattr(t, "is_overdue", False))

        return {
            "total": len(tasks),
            "overdue": overdue_count,
            "by_status": dict(status_counts),
        }
