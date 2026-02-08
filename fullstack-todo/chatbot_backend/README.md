# AI Chatbot Backend for Todo Application

This is an AI-powered chatbot backend that enables natural language interaction with todo management functionality. The system uses an OpenAI Agent that connects to a Gemini LLM via external HTTP client, with MCP tools exposing todo operations.

## Features

- Natural language processing for todo management
- MCP (Model Context Protocol) server for tool-based operations
- Secure authentication using Better Auth
- Rate limiting to prevent abuse
- Persistent conversation history

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLModel
- **AI Framework**: OpenAI Agents SDK
- **LLM**: Google Gemini (via external HTTP client)
- **Authentication**: Better Auth
- **Package Management**: UV

## Setup

1. Clone the repository
2. Install dependencies with UV:
   ```bash
   uv sync
   ```

3. Set up environment variables by copying `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

   Then update the values in `.env`:
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `BETTER_AUTH_SECRET`: Secret for authentication
   - `BETTER_AUTH_URL`: Better Auth server URL

4. Run the application:
   ```bash
   uv run python src/main.py
   ```

## API Endpoints

- `POST /api/v1/chat/sessions` - Create or continue a chat session
- `GET /api/v1/chat/sessions` - Get user's chat sessions
- `GET /api/v1/chat/sessions/{session_id}/messages` - Get messages from a session
- `GET /health` - Health check endpoint

## Architecture

The system follows a layered architecture:
- **Chat API**: Handles user requests and authentication
- **AI Agent**: Interprets natural language and selects appropriate tools
- **MCP Server**: Exposes todo operations as tools
- **Services**: Business logic layer
- **Database**: Data persistence with SQLModel

## Usage Examples

### Starting a Chat Session
```bash
curl -X POST http://localhost:8001/api/v1/chat/sessions \
  -H "Authorization: Bearer <auth-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a task to buy groceries"
  }'
```

### Continuing a Chat Session
```bash
curl -X POST http://localhost:8001/api/v1/chat/sessions \
  -H "Authorization: Bearer <auth-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me my tasks",
    "session_id": "session-uuid-from-previous-response"
  }'
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL database URL
- `GEMINI_API_KEY`: Google Gemini API key
- `BETTER_AUTH_SECRET`: Authentication secret
- `BETTER_AUTH_URL`: Better Auth server URL
- `MCP_SERVER_HOST`: MCP server hostname
- `MCP_SERVER_PORT`: MCP server port
- `RATE_LIMIT_REQUESTS_PER_HOUR`: Rate limit for requests per hour
- `APP_ENV`: Application environment (development/production)
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.