# API Contracts: Backend & Testing Todo API

## Authentication Endpoints

### POST /auth/signup
**Description**: Create a new user account

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z"
}
```

**Response (400 Bad Request):**
```json
{
  "error_code": "INVALID_INPUT",
  "message": "Invalid email format or password too short",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### POST /auth/signin
**Description**: Authenticate user and return JWT token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer",
  "user_id": "uuid-string"
}
```

**Response (401 Unauthorized):**
```json
{
  "error_code": "INVALID_CREDENTIALS",
  "message": "Invalid email or password",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Task Management Endpoints

### GET /api/{user_id}/tasks
**Description**: Get all tasks for a user

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task Title",
      "description": "Task description",
      "completed": false,
      "user_id": "uuid-string",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

**Response (401 Unauthorized):**
```json
{
  "error_code": "UNAUTHORIZED",
  "message": "Authentication required",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

**Response (403 Forbidden):**
```json
{
  "error_code": "FORBIDDEN",
  "message": "Access denied to this user's tasks",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### POST /api/{user_id}/tasks
**Description**: Create a new task for a user

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
```json
{
  "title": "New Task",
  "description": "Task description"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "user_id": "uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (422 Unprocessable Entity):**
```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Title must be between 1 and 100 characters",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### GET /api/{user_id}/tasks/{task_id}
**Description**: Get a specific task by ID

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Task Title",
  "description": "Task description",
  "completed": false,
  "user_id": "uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (404 Not Found):**
```json
{
  "error_code": "TASK_NOT_FOUND",
  "message": "Task with specified ID not found",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### PUT /api/{user_id}/tasks/{task_id}
**Description**: Update a specific task

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
```json
{
  "title": "Updated Task",
  "description": "Updated description"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Updated Task",
  "description": "Updated description",
  "completed": false,
  "user_id": "uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### DELETE /api/{user_id}/tasks/{task_id}
**Description**: Delete a specific task

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (204 No Content)**

### PATCH /api/{user_id}/tasks/{task_id}/complete
**Description**: Mark a task as complete or incomplete

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
```json
{
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Task Title",
  "description": "Task description",
  "completed": true,
  "user_id": "uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Common Error Responses

### 400 Bad Request
```json
{
  "error_code": "INVALID_INPUT",
  "message": "Request contains invalid data",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### 401 Unauthorized
```json
{
  "error_code": "UNAUTHORIZED",
  "message": "Authentication required",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### 403 Forbidden
```json
{
  "error_code": "FORBIDDEN",
  "message": "Access denied to requested resource",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### 429 Too Many Requests
```json
{
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded, please try again later",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### 500 Internal Server Error
```json
{
  "error_code": "INTERNAL_ERROR",
  "message": "An unexpected error occurred",
  "timestamp": "2023-01-01T00:00:00Z"
}
```