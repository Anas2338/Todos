# Quickstart Guide: In-Memory Todo Python Console Application

## Setup

1. Ensure Python 3.13+ is installed
2. Install UV package manager if not already installed: `pip install uv`
3. Install dependencies using UV: `uv sync`
4. Run the application: `uv run todo-app` or `python -m src.todo_app.main`

## Basic Usage

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

## Validation Steps

1. Verify all 5 core operations work correctly:
   - Add: Create tasks with titles and descriptions
   - View: List all tasks with proper ID and status indicators
   - Update: Modify existing tasks by ID
   - Delete: Remove tasks by ID
   - Mark: Toggle completion status

2. Test error handling:
   - Invalid task IDs
   - Empty commands
   - Commands with wrong number of arguments

3. Confirm in-memory persistence works during single session