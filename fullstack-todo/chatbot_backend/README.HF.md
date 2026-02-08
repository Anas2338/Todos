---
title: Todo Chatbot Backend
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
app_port: 7860
---

# Todo Chatbot Backend

An intelligent AI chatbot backend for managing todos using Google Gemini and FastAPI.

## 🚀 Features

- **AI-Powered Chat** - Natural language todo management using Google Gemini
- **User Authentication** - Secure authentication with Better Auth integration
- **Task Management** - Create, update, and manage todos through conversation
- **Rate Limiting** - Protection against API abuse
- **Performance Monitoring** - Built-in performance tracking and logging
- **Input Sanitization** - Secure input validation and sanitization

## 📡 API Endpoints

### Chat
- `POST /chat` - Send messages to the AI chatbot
- `GET /chat/history` - Get chat history for authenticated user

### Health & Monitoring
- `GET /health` - Health check endpoint
- `GET /metrics` - Performance metrics (if enabled)

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)

## 🔧 Environment Variables

This Space requires the following environment variables to be configured in the Space settings:

### Database Configuration
- `DATABASE_URL` - PostgreSQL connection string (Neon or other PostgreSQL database)

### Authentication
- `BETTER_AUTH_SECRET` - Secret key for Better Auth
- `BETTER_AUTH_URL` - URL of the authentication service

### AI Configuration
- `GEMINI_API_KEY` - Google Gemini API key
- `GEMINI_MODEL_NAME` - Gemini model to use (default: gemini-2.5-flash)

### MCP Server (Optional)
- `MCP_SERVER_HOST` - MCP server host (default: localhost)
- `MCP_SERVER_PORT` - MCP server port (default: 8001)

### Application Settings
- `APP_ENV` - Environment (development/production)
- `LOG_LEVEL` - Logging level (INFO/DEBUG/WARNING/ERROR)
- `RATE_LIMIT_REQUESTS_PER_HOUR` - Rate limit threshold (default: 100)

## 📚 Technology Stack

- **FastAPI** - Modern Python web framework
- **Google Gemini** - AI language model for natural conversations
- **SQLModel** - SQL databases with Python types
- **Better Auth** - Authentication integration
- **Docker** - Containerized deployment
- **uv** - Fast Python package manager

## 🧪 Try It Out

1. Visit the `/docs` endpoint for interactive API documentation
2. Authenticate using your credentials
3. Start chatting with the AI to manage your todos
4. Use natural language like "Add a task to buy groceries" or "Show my tasks"

## 🔐 Security Features

- Input sanitization and validation
- Rate limiting per user
- Secure authentication integration
- Environment-based configuration
- Non-root container execution

## 📖 Full Documentation

For complete documentation, setup instructions, and contribution guidelines, visit the [GitHub repository](https://github.com/yourusername/yourrepo).
