# In-Memory Todo Python Console Application

A simple console-based todo application that stores tasks in memory during a single runtime session.

## Features

- Add tasks with titles and descriptions
- View all tasks with unique IDs and status indicators
- Update existing tasks by ID
- Delete tasks by ID
- Mark tasks as complete or incomplete
- Interactive command prompt interface
- Sequential numeric task IDs
- Clear visual status indicators ([✓] for complete, [ ] for incomplete)

## Setup

1. Ensure Python 3.13+ is installed
2. Install UV package manager if not already installed: `pip install uv`
3. Install dependencies using UV: `uv sync`
4. Run the application: `uv run todo-app` or `python -m src.todo_app.main`

## Usage

### Available Commands

- `add "title" "description"` - Add a new task
- `list` or `ls` - View all tasks
- `update <id> "new title" "new description"` - Update a task
- `complete <id>` - Mark a task as complete
- `incomplete <id>` - Mark a task as incomplete
- `delete <id>` - Delete a task
- `help` - Show available commands
- `quit` or `exit` - Exit the application

### Example Workflow

```
> add "Buy groceries" "Milk, bread, eggs"
Task #1 added successfully: [ ] Buy groceries - Milk, bread, eggs

> add "Finish report" "Complete the quarterly report"
Task #2 added successfully: [ ] Finish report - Complete the quarterly report

> list
1. [ ] Buy groceries - Milk, bread, eggs
2. [ ] Finish report - Complete the quarterly report

> complete 1
Task #1 marked as complete: [✓] Buy groceries - Milk, bread, eggs

> list
1. [✓] Buy groceries - Milk, bread, eggs
2. [ ] Finish report - Complete the quarterly report

> quit
Goodbye!
```

## Technical Details

- Built with Python 3.13+
- No external dependencies (stdlib only)
- In-memory storage (tasks are lost when application exits)
- Clean architecture with separation of concerns:
  - `models.py`: Task data model
  - `storage.py`: In-memory storage operations
  - `cli.py`: Command-line interface logic
  - `main.py`: Application entry point

## Project Structure

```
src/
├── todo_app/
│   ├── __init__.py
│   ├── main.py          # Entry point with CLI interface
│   ├── models.py        # Task data model
│   ├── storage.py       # In-memory storage implementation
│   ├── cli.py           # Command-line interface logic
│   └── exceptions.py    # Custom exception classes
├── tests/
│   └── manual_test_plan.md  # Manual validation steps
└── pyproject.toml       # Project configuration
```