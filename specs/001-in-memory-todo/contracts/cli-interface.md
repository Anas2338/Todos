# CLI Interface Contract: Todo Application

## Command Specifications

### Add Command
- **Syntax**: `add "title" "description"`
- **Input**: Title (string, 1-100 chars), Description (string, 0-500 chars)
- **Output**: Success message with assigned ID and task details
- **Error Cases**: Invalid syntax, title too long, missing arguments

### List Command
- **Syntax**: `list` or `ls`
- **Input**: None
- **Output**: Formatted list of all tasks with IDs, status indicators, titles, and descriptions
- **Error Cases**: None (shows empty list if no tasks)

### Update Command
- **Syntax**: `update <id> "new title" "new description"`
- **Input**: Task ID (positive integer), new title and description
- **Output**: Success confirmation
- **Error Cases**: Invalid ID, task not found, invalid syntax

### Complete Command
- **Syntax**: `complete <id>`
- **Input**: Task ID (positive integer)
- **Output**: Success confirmation
- **Error Cases**: Invalid ID, task not found

### Incomplete Command
- **Syntax**: `incomplete <id>`
- **Input**: Task ID (positive integer)
- **Output**: Success confirmation
- **Error Cases**: Invalid ID, task not found

### Delete Command
- **Syntax**: `delete <id>`
- **Input**: Task ID (positive integer)
- **Output**: Success confirmation
- **Error Cases**: Invalid ID, task not found

### Help Command
- **Syntax**: `help`
- **Input**: None
- **Output**: List of available commands with brief descriptions
- **Error Cases**: None

### Quit Command
- **Syntax**: `quit` or `exit`
- **Input**: None
- **Output**: Exit confirmation message
- **Error Cases**: None