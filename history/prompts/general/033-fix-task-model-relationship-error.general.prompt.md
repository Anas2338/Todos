---
id: 033
title: "Fix Task Model Relationship Error"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "3-chatbot-integration"
user: "user"
command: "Fix Task model relationship with undefined User class"
labels: ["bug", "database", "sqlmodel", "relationship"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

## Files Modified

- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\src\models\task.py
- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\src\core\database.py

## Tests Added/Modified

- N/A (Bug fix, no new tests added)

## Prompt Text

Fix the Task model relationship error where the Task model was trying to reference a User class that doesn't exist in the chatbot backend, causing "expression 'User' failed to locate a name" error.

## Response Text

Fixed the Task model relationship error by removing the undefined User relationship:

1. Updated `src/models/task.py`:
   - Removed the `Relationship` import since no relationships are needed
   - Removed the `user: Optional["User"] = Relationship(back_populates="tasks")` field
   - Removed the foreign key reference to "users.id" and changed to direct user_id field
   - Simplified the model to only include the necessary fields without undefined relationships

2. Updated `src/core/database.py`:
   - Added import for the Task model in the init_db function
   - Ensured the Task model is registered with SQLModel for table creation

The Task model now properly defines user_id as a simple UUID field without trying to create a relationship with an undefined User class, resolving the SQLAlchemy mapper initialization error.

## Outcome

The database can now properly initialize without mapper errors, allowing the chatbot backend to start successfully.

## Evaluation

The fix addresses the root cause: undefined class reference in model relationships. The solution removes the problematic relationship and keeps only the essential fields.