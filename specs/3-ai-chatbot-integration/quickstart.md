# Quickstart: AI Chatbot Integration for Todo Application

## Overview
This guide provides instructions for setting up and running the AI Chatbot backend for todo management.

## Prerequisites
- Python 3.11+
- UV package manager
- Access to Gemini API (with API key)
- PostgreSQL database (Neon Serverless recommended)
- Better Auth configuration

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies with UV
```bash
uv sync
```

### 3. Environment Configuration
Create a `.env` file with the following variables:
```bash
# Database
DATABASE_URL="postgresql://username:password@host:port/database"

# Better Auth
BETTER_AUTH_SECRET="your-better-auth-secret"
BETTER_AUTH_URL="http://localhost:8000"

# Gemini API
GEMINI_API_KEY="your-gemini-api-key"

# MCP Server
MCP_SERVER_HOST="localhost"
MCP_SERVER_PORT=8001

# Rate limiting
RATE_LIMIT_REQUESTS_PER_HOUR=100
```

### 4. Database Setup
Run the database migrations:
```bash
uv run alembic upgrade head
```

### 5. Start the Services

#### Option A: Start MCP Server
```bash
uv run python scripts/start_mcp_server.py
```

#### Option B: Start Main Application (includes embedded MCP server)
```bash
uv run uvicorn src.main:app --reload --port 8000
```

## Usage Examples

### Starting a Chat Session
```bash
curl -X POST http://localhost:8000/api/v1/chat/sessions \
  -H "Authorization: Bearer <auth-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a task to buy groceries"
  }'
```

### Continuing a Chat Session
```bash
curl -X POST http://localhost:8000/api/v1/chat/sessions \
  -H "Authorization: Bearer <auth-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me my tasks",
    "session_id": "session-uuid-from-previous-response"
  }'
```

## Testing
Run the test suite:
```bash
uv run pytest
```

For specific test categories:
```bash
# Unit tests
uv run pytest tests/unit/

# Integration tests
uv run pytest tests/integration/

# Contract tests
uv run pytest tests/contract/
```

## Development
To run in development mode with hot reloading:
```bash
uv run uvicorn src.main:app --reload --port 8000
```

## Architecture Components

### Chat API Layer
- Located in `src/chat/api.py`
- Handles authentication and rate limiting
- Manages chat session state

### AI Agent
- Located in `src/chat/agent.py`
- Connects to Gemini LLM via external client
- Selects appropriate MCP tools based on user intent

### MCP Server
- Located in `src/mcp_server/server.py`
- Exposes todo operations as MCP tools
- Enforces user authorization

### Models
- Shared SQLModel entities in `src/models/`
- Includes both Phase II entities (User, Task) and new chat entities (ChatSession, ChatMessage, ToolInvocation)

## Troubleshooting

### Common Issues
1. **Authentication failures**: Verify Better Auth configuration and token validity
2. **Gemini API errors**: Check API key and rate limits
3. **Database connection issues**: Confirm DATABASE_URL is correctly set
4. **MCP tool execution failures**: Ensure MCP server is running and accessible

### Logs
Application logs are available in the console when running in development mode.