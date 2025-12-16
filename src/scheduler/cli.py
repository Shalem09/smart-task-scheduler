#cli.py

import sys
from datetime import datetime
from .persistence.storage_json import JsonStorage
from .persistence.repository import TaskRepository
from .scheduling.strategies import HighestPriorityFirst
from .scheduling.scheduler import Scheduler
from .app.service import TaskService

def print_help():
    print("""
Smart Task Scheduler CLI

Usage:
  sched help
  sched add "<title>" <priority>
  sched list
  sched next
  sched start <id>
  sched block <id> "<reason>"
  sched unblock <id>
  sched complete <id>
  sched due <id> "YYYY-MM-DD HH:MM"
  sched clear-due <id>
  sched stats

Examples:
  sched add "Learn OOP Python" 5
  sched start 1
  sched block 1 "Waiting for review"
  sched complete 1
  sched due 1 "2025-01-01 12:01"

""".strip())

def parse_due_date(s: str) -> datetime:
    s = s.strip()

    formats = [
        "%Y-%m-%d %H:%M",  # 2025-12-15 16:20
        "%y-%m-%d %H:%M",  # 25-12-15 16:20
    ]

    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue

    raise ValueError(
        "Invalid date format. Use 'YYYY-MM-DD HH:MM' (e.g. 2025-12-15 16:20) "
        "or 'YY-MM-DD HH:MM' (e.g. 25-12-15 16:20)."
    )

def format_task(t) -> str:
    overdue = " OVERDUE!" if getattr(t, "is_overdue", False) else ""
    blocked = f" (blocked: {t.blocked_reason})" if getattr(t, "blocked_reason", None) else ""
    due = f" due date = {t.due_date.strftime('%Y-%m-%d %H:%M')}" if getattr(t, "due_date", None) else ""
    pr = f"(p = {'●' * t.priority})"
    return f"{t.id}. {t.title} [{t.status}]{overdue}{blocked}{due} {pr}"


def main():
    storage = JsonStorage("tasks.json")
    repo = TaskRepository(storage)
    scheduler = Scheduler(HighestPriorityFirst())
    service = TaskService(repo, scheduler)
    
    if len(sys.argv) < 2 or sys.argv[1] in ("help", "-h", "--help"):
        print_help()
        return

    cmd = sys.argv[1]
    
    if cmd == "add":
        title = sys.argv[2]
        priority = int(sys.argv[3])
        task = service.add_task(title, priority)
        print(f"Added task #{task.id}")
            
    elif cmd == "list":
        tasks = service.list_tasks()
        for t in tasks:
            print(format_task(t))

    elif cmd == "next":
        task = service.next_task()
        if task:
            print("Next: " + format_task(task))
        else:
            print("No eligible tasks")
            
    elif cmd == "start":
        task_id = int(sys.argv[2])
        t = service.start_task(task_id)
        print(f"Task #{t.id} -> {t.status}")

    elif cmd == "block":
        task_id = int(sys.argv[2])
        reason = sys.argv[3]
        t = service.block_task(task_id, reason)
        print(f"Task #{t.id} -> {t.status} (reason={t.blocked_reason})")

    elif cmd == "unblock":
        task_id = int(sys.argv[2])
        t = service.unblock_task(task_id)
        print(f"Task #{t.id} -> {t.status}")

    elif cmd == "complete":
        task_id = int(sys.argv[2])
        t = service.complete_task(task_id)
        print(f"Task #{t.id} -> {t.status}")
        
    elif cmd == "due":
        task_id = int(sys.argv[2])
        due = parse_due_date(sys.argv[3])
        t = service.set_due_date(task_id, due)
        print(f"Task #{t.id} due_date set to {t.due_date}")

    elif cmd == "clear-due":
        task_id = int(sys.argv[2])
        t = service.set_due_date(task_id, None)
        print(f"Task #{t.id} due_date cleared")

    elif cmd == "stats":
        s = service.stats()
        print(f"Total: {s['total']}")
        print(f"Overdue: {s['overdue']}")
        print("By status:")
        for status, count in sorted(s["by_status"].items()):
            print(f"  {status}: {count}")

if __name__ == "__main__":
    main()
