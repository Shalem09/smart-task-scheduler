# Smart Task Scheduler (Python CLI)

Smart Task Scheduler is a command-line (CLI) application built in Python as a professional learning project.
Its goal is to demonstrate clean Object-Oriented Programming (OOP), proper project structure, and the use of classic design patterns in a real, working system.

The application is designed to be executed **from the terminal only**.

---

## ✨ Key Features
- Task management with priorities
- Task lifecycle states: `BACKLOG`, `READY`, `IN_PROGRESS`, `BLOCKED`, `DONE`
- **State Pattern** – enforces valid state transitions
- **Strategy Pattern** – selects the next task based on priority
- **Rule Engine** – business rules such as overdue detection
- Due dates (`due_date`)
- Task statistics (`stats`)
- JSON-based persistence
- Clean and user-friendly CLI

---

## 📂 Project Structure
'''
smart_scheduler/
  README.md
  src/
    scheduler/
      __init__.py
      cli.py
      domain/
        __init__.py
        task.py
        states.py
      scheduling/
        __init__.py
        strategies.py
        scheduler.py
      rules/
        __init__.py
        rules.py
      persistence/
        __init__.py
        repository.py
        storage_json.py
      app/
        __init__.py
        service.py
'''
---

## ⚠️ Important – How *Not* to Run the Project
❌ Do **NOT** run `cli.py` using the ▶️ (Run) button in VS Code  
❌ Do **NOT** run `python cli.py`

### Why?
- The project is structured as a Python **package**
- It relies on relative imports
- Running it incorrectly will result in `ModuleNotFoundError`

---

## ▶️ Correct Way to Run the Project
The application must be executed from the terminal.

### 1️⃣ Navigate to the `src` directory
```powershell
cd src
```
### 2️⃣ Run using Python module execution
```
python -m scheduler.cli help
python -m scheduler.cli list
```

### 📌 Available CLI Commands
add "<title>" <priority>        Add a new task
list                            List all tasks
next                            Suggest the next task
start <id>                      Move task to IN_PROGRESS
block <id> "<reason>"           Block a task
unblock <id>                    Unblock a task
complete <id>                   Complete a task
due <id> "YYYY-MM-DD HH:MM"     Set due date
clear-due <id>                  Remove due date
stats                           Show task statistics
help                            Show help

---

Design Decisions

- dataclasses are used for domain models

- State Pattern avoids scattered conditional logic

- Rule Engine is separated from CLI and persistence

- CLI acts as a thin layer; business logic lives in the Service layer

- Execution via python -m follows Python best practices
---

🚀 Project Purpose

- This project was built as a personal portfolio project to:

- Strengthen Python OOP skills

- Demonstrate clean architecture and design patterns

- Serve as a showcase project for Backend / Python roles
