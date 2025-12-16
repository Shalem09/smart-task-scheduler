from datetime import datetime
from ..domain.task import Task
from .storage_json import JsonStorage


class TaskRepository:
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def _deserialize(self, raw: dict) -> Task:
        return Task(
            id = raw["id"],
            title = raw["title"],
            priority = raw["priority"],
            created_at = datetime.fromisoformat(raw["created_at"]),
            due_date = datetime.fromisoformat(raw["due_date"]) if raw.get("due_date") else None,
            tags = raw.get("tags", []),
            status = raw.get("status", "BACKLOG"),
            blocked_reason = raw.get("blocked_reason"),
        )

    def _serialize(self, task: Task) -> dict:
        return {
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "created_at": task.created_at.isoformat(),
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags,
            "status": task.status,
            "blocked_reason": task.blocked_reason,
        }

    def list_all(self) -> list[Task]:
        return [self._deserialize(r) for r in self.storage.load()]

    def save_all(self, tasks: list[Task]) -> None:
        self.storage.save([self._serialize(t) for t in tasks])

    def next_id(self) -> int:
        tasks = self.list_all()
        if not tasks:
            return 1
        return max(t.id for t in tasks) + 1

    def get_by_id(self, task_id: int) -> Task | None:
        for t in self.list_all():
            if t.id == task_id:
                return t
        return None

    def update(self, updated_task: Task) -> None:
        tasks = self.list_all()
        for i, t in enumerate(tasks):
            if t.id == updated_task.id:
                tasks[i] = updated_task
                self.save_all(tasks)
                return
        raise ValueError(f"Task id {updated_task.id} not found")
