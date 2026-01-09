# Data Model: In-Memory Todo Python Console Application

## Core Entities

### Task
- **id**: int (sequential, starting from 1, unique within session)
- **title**: str (max 100 characters)
- **description**: str (max 500 characters)
- **completed**: bool (default: False)
- **created_at**: datetime (timestamp when task was created)

### Validation Rules
- Title must be 1-100 characters
- Description can be 0-500 characters
- ID must be positive integer
- Completed status is boolean (True/False)

## State Transitions

### Task Lifecycle
1. **Created**: Task is initialized with title, description, and completed=False
2. **Active**: Task exists in the system, can be viewed, updated, or marked complete/incomplete
3. **Completed**: Task marked as completed by user
4. **Deleted**: Task removed from the system (end of lifecycle)

### Status Changes
- Incomplete → Complete: When user marks task as complete
- Complete → Incomplete: When user marks task as incomplete