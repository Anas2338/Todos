# Data Model: Frontend Todo Application

## Entities

### User
**Description**: Represents a registered user of the Todo application with authentication credentials and personal task data

**Fields**:
- `id`: string - Unique identifier for the user
- `email`: string - User's email address (required, unique)
- `name`: string - User's display name (optional)
- `createdAt`: Date - Timestamp when the user account was created
- `updatedAt`: Date - Timestamp when the user account was last updated

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Required fields: id, email

### Task
**Description**: Represents a todo item with attributes: id, title, description, completion status, and associated user ID

**Fields**:
- `id`: string - Unique identifier for the task
- `title`: string - Task title (required, max 100 characters)
- `description`: string - Task description (optional, max 1000 characters)
- `completed`: boolean - Whether the task is completed (default: false)
- `userId`: string - ID of the user who owns this task
- `createdAt`: Date - Timestamp when the task was created
- `updatedAt`: Date - Timestamp when the task was last updated

**Validation Rules**:
- Title is required and must be 1-100 characters
- Description is optional and can be up to 1000 characters
- Completed defaults to false
- UserId must reference a valid user
- Required fields: id, title, userId

## State Transitions

### Task State Transitions
- **Incomplete → Complete**: When user marks task as complete via PATCH /api/{user_id}/tasks/{id}/complete
- **Complete → Incomplete**: When user marks task as incomplete via PATCH /api/{user_id}/tasks/{id}/complete

### User Authentication States
- **Unauthenticated → Authenticated**: When user successfully logs in
- **Authenticated → Unauthenticated**: When user logs out or session expires

## Relationships
- **User → Task**: One-to-many (one user can have many tasks)
- **Task → User**: Many-to-one (many tasks belong to one user)

## API Data Contracts

### Task Creation Request
```
{
  "title": "string (required, 1-100 chars)",
  "description": "string (optional, 0-1000 chars)"
}
```

### Task Response
```
{
  "id": "string",
  "title": "string (1-100 chars)",
  "description": "string (0-1000 chars)",
  "completed": "boolean",
  "userId": "string",
  "createdAt": "Date",
  "updatedAt": "Date"
}
```

### Task Update Request
```
{
  "title": "string (optional, 1-100 chars)",
  "description": "string (optional, 0-1000 chars)"
}
```

### Task Completion Update Request
```
{
  "completed": "boolean"
}
```

### User Authentication Response
```
{
  "id": "string",
  "email": "string",
  "name": "string (optional)"
}
```