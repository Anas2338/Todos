# MCP Contract: Todo Operations for AI Chatbot Integration

## Overview
This document specifies the Model Context Protocol (MCP) contracts for todo operations exposed as MCP tools. These tools enable the AI agent to perform todo management operations through standardized interfaces.

## Tool: create_task

### Description
Creates a new todo task for the authenticated user.

### Parameters
```json
{
  "title": {
    "type": "string",
    "description": "Title of the task to create",
    "required": true
  },
  "description": {
    "type": "string",
    "description": "Optional description of the task",
    "required": false
  }
}
```

### Example Request
```json
{
  "method": "tools/call",
  "params": {
    "id": "tool-call-123",
    "name": "create_task",
    "arguments": {
      "title": "Buy groceries",
      "description": "Need to buy milk, bread, and eggs"
    }
  }
}
```

### Example Response
```json
{
  "result": {
    "success": true,
    "task": {
      "id": "task-uuid",
      "title": "Buy groceries",
      "description": "Need to buy milk, bread, and eggs",
      "is_completed": false,
      "created_at": "2026-01-17T10:30:00Z"
    }
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "CREATE_TASK_FAILED",
    "message": "Failed to create task: reason for failure"
  }
}
```

## Tool: list_tasks

### Description
Lists all todo tasks for the authenticated user, with optional filtering.

### Parameters
```json
{
  "status": {
    "type": "string",
    "description": "Filter tasks by status ('all', 'completed', 'pending'). Defaults to 'all'",
    "required": false,
    "default": "all"
  },
  "limit": {
    "type": "integer",
    "description": "Maximum number of tasks to return. Defaults to 100",
    "required": false,
    "default": 100
  },
  "offset": {
    "type": "integer",
    "description": "Number of tasks to skip. Defaults to 0",
    "required": false,
    "default": 0
  }
}
```

### Example Request
```json
{
  "method": "tools/call",
  "params": {
    "id": "tool-call-124",
    "name": "list_tasks",
    "arguments": {
      "status": "pending",
      "limit": 10
    }
  }
}
```

### Example Response
```json
{
  "result": {
    "success": true,
    "tasks": [
      {
        "id": "task-uuid-1",
        "title": "Buy groceries",
        "description": "Need to buy milk, bread, and eggs",
        "is_completed": false,
        "created_at": "2026-01-17T10:30:00Z",
        "updated_at": "2026-01-17T10:30:00Z"
      }
    ],
    "total_count": 1
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "LIST_TASKS_FAILED",
    "message": "Failed to list tasks: reason for failure"
  }
}
```

## Tool: get_task

### Description
Retrieves a specific todo task by its ID.

### Parameters
```json
{
  "task_id": {
    "type": "string",
    "description": "ID of the task to retrieve",
    "required": true
  }
}
```

### Example Request
```json
{
  "method": "tools/call",
  "params": {
    "id": "tool-call-125",
    "name": "get_task",
    "arguments": {
      "task_id": "task-uuid-1"
    }
  }
}
```

### Example Response
```json
{
  "result": {
    "success": true,
    "task": {
      "id": "task-uuid-1",
      "title": "Buy groceries",
      "description": "Need to buy milk, bread, and eggs",
      "is_completed": false,
      "created_at": "2026-01-17T10:30:00Z",
      "updated_at": "2026-01-17T10:30:00Z"
    }
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "GET_TASK_FAILED",
    "message": "Failed to get task: reason for failure"
  }
}
```

## Tool: update_task

### Description
Updates properties of an existing todo task.

### Parameters
```json
{
  "task_id": {
    "type": "string",
    "description": "ID of the task to update",
    "required": true
  },
  "title": {
    "type": "string",
    "description": "New title for the task (optional)",
    "required": false
  },
  "description": {
    "type": "string",
    "description": "New description for the task (optional)",
    "required": false
  }
}
```

### Example Request
```json
{
  "method": "tools/call",
  "params": {
    "id": "tool-call-126",
    "name": "update_task",
    "arguments": {
      "task_id": "task-uuid-1",
      "title": "Buy weekly groceries",
      "description": "Need to buy milk, bread, eggs, and vegetables"
    }
  }
}
```

### Example Response
```json
{
  "result": {
    "success": true,
    "task": {
      "id": "task-uuid-1",
      "title": "Buy weekly groceries",
      "description": "Need to buy milk, bread, eggs, and vegetables",
      "is_completed": false,
      "created_at": "2026-01-17T10:30:00Z",
      "updated_at": "2026-01-17T10:35:00Z"
    }
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "UPDATE_TASK_FAILED",
    "message": "Failed to update task: reason for failure"
  }
}
```

## Tool: delete_task

### Description
Deletes a specific todo task by its ID.

### Parameters
```json
{
  "task_id": {
    "type": "string",
    "description": "ID of the task to delete",
    "required": true
  }
}
```

### Example Request
```json
{
  "method": "tools/call",
  "params": {
    "id": "tool-call-127",
    "name": "delete_task",
    "arguments": {
      "task_id": "task-uuid-1"
    }
  }
}
```

### Example Response
```json
{
  "result": {
    "success": true,
    "deleted_task_id": "task-uuid-1"
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "DELETE_TASK_FAILED",
    "message": "Failed to delete task: reason for failure"
  }
}
```

## Tool: set_task_complete

### Description
Sets the completion status of a specific todo task.

### Parameters
```json
{
  "task_id": {
    "type": "string",
    "description": "ID of the task to update",
    "required": true
  },
  "is_completed": {
    "type": "boolean",
    "description": "Whether the task is completed or not",
    "required": true
  }
}
```

### Example Request
```json
{
  "method": "tools/call",
  "params": {
    "id": "tool-call-128",
    "name": "set_task_complete",
    "arguments": {
      "task_id": "task-uuid-1",
      "is_completed": true
    }
  }
}
```

### Example Response
```json
{
  "result": {
    "success": true,
    "task": {
      "id": "task-uuid-1",
      "title": "Buy weekly groceries",
      "description": "Need to buy milk, bread, eggs, and vegetables",
      "is_completed": true,
      "created_at": "2026-01-17T10:30:00Z",
      "updated_at": "2026-01-17T10:40:00Z"
    }
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "SET_TASK_COMPLETE_FAILED",
    "message": "Failed to set task completion: reason for failure"
  }
}
```

## Common Error Codes
- `AUTHENTICATION_FAILED`: User authentication failed
- `AUTHORIZATION_FAILED`: User is not authorized to perform the operation
- `VALIDATION_ERROR`: Request parameters failed validation
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `DATABASE_ERROR`: Database operation failed
- `INTERNAL_ERROR`: Unexpected internal error occurred

## Security Considerations
- All tools enforce user authentication and authorization
- Users can only operate on their own tasks
- Input validation prevents injection attacks
- Rate limiting applies to prevent abuse
- Detailed error messages do not expose internal system information