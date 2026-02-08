# API Contract: Chat Endpoint for AI Chatbot Integration

## Overview
This document specifies the API contract for the chat endpoint that enables natural language interaction with the todo management system.

## Base URL
`/api/v1/chat`

## Authentication
All endpoints require authentication via Better Auth. The authentication token must be provided in the `Authorization` header as a Bearer token.

## Endpoints

### POST /sessions
Start a new chat session or continue an existing one.

#### Request
```json
{
  "message": "Create a task to buy groceries",
  "session_id": "optional-session-uuid"
}
```

**Headers**:
- `Authorization`: Bearer {token}
- `Content-Type`: application/json

**Request Body**:
- `message` (string, required): The user's message in natural language
- `session_id` (string, optional): UUID of existing session to continue, or null for new session

#### Response
```json
{
  "session_id": "session-uuid",
  "response": "I've created a task 'buy groceries' for you.",
  "timestamp": "2026-01-17T10:30:00Z"
}
```

**Response Fields**:
- `session_id` (string): UUID of the chat session (new or existing)
- `response` (string): AI-generated response to the user's message
- `timestamp` (string): ISO 8601 timestamp of the response

**Status Codes**:
- `200 OK`: Successfully processed the message
- `400 Bad Request`: Invalid request body or parameters
- `401 Unauthorized`: Missing or invalid authentication token
- `429 Too Many Requests`: Rate limit exceeded (100 messages/hour per user)
- `500 Internal Server Error`: Server error during processing

### GET /sessions/{session_id}/messages
Retrieve messages from a specific chat session.

#### Path Parameters
- `session_id` (string): UUID of the chat session

#### Request
```http
GET /api/v1/chat/sessions/session-uuid/messages
Authorization: Bearer {token}
```

#### Response
```json
{
  "messages": [
    {
      "id": "message-uuid",
      "role": "user",
      "content": "Create a task to buy groceries",
      "timestamp": "2026-01-17T10:29:00Z"
    },
    {
      "id": "message-uuid",
      "role": "assistant",
      "content": "I've created a task 'buy groceries' for you.",
      "timestamp": "2026-01-17T10:29:05Z"
    }
  ],
  "total_count": 2
}
```

**Status Codes**:
- `200 OK`: Successfully retrieved messages
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not have access to this session
- `404 Not Found`: Session does not exist
- `500 Internal Server Error`: Server error during retrieval

### GET /sessions
Retrieve a list of user's chat sessions.

#### Request
```http
GET /api/v1/chat/sessions
Authorization: Bearer {token}
```

#### Response
```json
{
  "sessions": [
    {
      "id": "session-uuid",
      "title": "Grocery tasks",
      "created_at": "2026-01-17T10:29:00Z",
      "updated_at": "2026-01-17T10:29:05Z",
      "is_active": true
    }
  ],
  "total_count": 1
}
```

**Status Codes**:
- `200 OK`: Successfully retrieved sessions
- `401 Unauthorized`: Missing or invalid authentication token
- `500 Internal Server Error`: Server error during retrieval

## Rate Limiting
- Maximum 100 messages per hour per authenticated session
- Expressed in the response headers:
  - `X-RateLimit-Limit`: 100 (requests allowed per window)
  - `X-RateLimit-Remaining`: Number of requests remaining
  - `X-RateLimit-Reset`: Unix timestamp for when the rate limit resets

## Error Responses
All error responses follow the same structure:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```

## Security Considerations
- All requests must be authenticated
- Users can only access their own sessions and messages
- Input sanitization applied to prevent injection attacks
- Rate limiting enforced to prevent abuse
- Sensitive data is not logged in plain text