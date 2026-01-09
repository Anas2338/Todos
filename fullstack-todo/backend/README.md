# Todo Backend API

A secure, multi-user Todo API backend with authentication built with FastAPI, SQLModel, and PostgreSQL.

## 🚀 Technology Stack

### Core Frameworks
- **FastAPI** - Modern, fast web framework for building APIs with automatic interactive documentation
- **SQLModel** - SQL databases in Python with Python types, combining SQLAlchemy and Pydantic
- **Pydantic** - Data validation and settings management using Python type hints

### Authentication & Security
- **JWT (JSON Web Tokens)** - Secure authentication and authorization
- **Passlib with bcrypt** - Password hashing and verification
- **python-jose** - JWT token creation and verification
- **Rate Limiting** - Protection against API abuse with configurable limits

### Database & Persistence
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping
- **PostgreSQL** - Robust, scalable relational database (with SQLite fallback)
- **Database Connection Pooling** - Efficient database connection management
- **Alembic** - Database migration management

### Testing & Development
- **pytest** - Testing framework with comprehensive test support
- **fastapi.testclient** - Testing client for FastAPI applications
- **uv** - Python package and project manager for dependency management

### Utilities & Tools
- **uvicorn** - ASGI server for running the application
- **python-dotenv** - Environment variable management
- **asyncpg** - Asynchronous PostgreSQL interface
- **slowapi** - Rate limiting middleware
- **python-multipart** - Form data parsing support

## 🌟 Key Features

### Authentication System
- User registration and login with email/password
- JWT token-based authentication
- Secure password hashing with bcrypt
- Token refresh mechanism
- User session management

### Task Management
- Create, read, update, delete (CRUD) operations for tasks
- User isolation (users can only access their own tasks)
- Task completion tracking
- Comprehensive input validation
- Rich task metadata (title, description, timestamps)

### Security Features
- Rate limiting to prevent API abuse
- Input validation with character limits
- User authentication for all task operations
- Secure password storage
- CORS middleware for web security

### Performance & Reliability
- Database connection pooling
- Comprehensive error handling
- Request/response logging
- Health check endpoints
- Database transaction support

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.13+
- PostgreSQL (or use SQLite for development, Neon for production)
- uv package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fullstack-todo/backend
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
   # For SQLite development: DATABASE_URL=sqlite:///./todo_app.db
   SECRET_KEY=your-super-secret-key-here-replace-with-actual-secure-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Run the application**
   ```bash
   uv run python main.py
   ```

### Alternative Installation Methods

**Using pip (if uv is not available):**
```bash
pip install -r requirements.txt
python main.py
```

**Using uv with specific Python version:**
```bash
uv python install 3.13
uv sync
uv run python main.py
```

## 📡 API Endpoints

### Authentication Endpoints
- `POST /auth/signup` - Create a new user account
- `POST /auth/signin` - Authenticate user and return JWT token

### Task Management Endpoints
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a specific task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Mark a task as complete/incomplete

### Health & Utility Endpoints
- `GET /health` - Basic health check
- `GET /health/extended` - Extended health check with system info
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /openapi.json` - OpenAPI specification

## 🧪 Running Tests

### Run all tests
```bash
uv run pytest
```

### Run specific test file
```bash
uv run pytest tests/test_basic.py
```

### Run tests with verbose output
```bash
uv run pytest -v
```

## 🚀 Deployment

### Environment Configuration
- Set `DATABASE_URL` to your production database
- Use a strong, unique `SECRET_KEY`
- Configure appropriate rate limiting settings
- Set up proper logging

### Production Deployment
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔧 Configuration Options

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string (Neon/PostgreSQL/SQLite) | `sqlite:///./todo_app.db` |
| `SECRET_KEY` | JWT signing key | Required |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration time | `30` |

### Neon Database Setup

1. **Sign up for Neon**
   - Go to [Neon Console](https://console.neon.tech/)
   - Create a new project
   - Note your connection string from the project dashboard

2. **Configure your Neon database**
   - Create a new database in your Neon project
   - Create a new user with appropriate permissions
   - Copy the connection string from the "Connection Details" section

3. **Update your `.env` file**
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   SECRET_KEY=your-super-secret-key-here-replace-with-actual-secure-key
   ```

4. **Neon-specific connection parameters**
   - Use `?sslmode=require` in your connection string for Neon
   - Neon supports serverless scaling and automatic pause
   - Connection pooling works automatically with Neon's connection pooling

5. **Neon best practices**
   - Neon databases automatically pause when inactive (save costs)
   - Use connection pooling to handle warm-up times after pause
   - Monitor connection usage in the Neon dashboard

## 📋 API Usage Examples

### User Registration
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

### User Authentication
```bash
curl -X POST "http://localhost:8000/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

### Create a Task (with authentication)
```bash
curl -X POST "http://localhost:8000/api/{user_id}/tasks" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the Todo API backend"
  }'
```

## 📊 Project Structure

```
backend/
├── src/
│   ├── api/           # API route definitions
│   │   ├── auth_routes.py
│   │   ├── task_routes.py
│   │   ├── health.py
│   │   └── middleware.py
│   ├── models/        # Database models
│   │   ├── user.py
│   │   ├── task.py
│   │   └── auth.py
│   ├── services/      # Business logic
│   │   ├── user_service.py
│   │   └── task_service.py
│   ├── utils/         # Utility functions
│   │   ├── security.py
│   │   ├── validators.py
│   │   ├── connection_pool.py
│   │   ├── rate_limiter.py
│   │   └── observability.py
│   └── config/        # Configuration
│       └── settings.py
├── tests/             # Test files
│   ├── unit/
│   ├── integration/
│   └── test_*.py
├── alembic/           # Database migrations
├── main.py            # Application entry point
├── requirements.txt   # Dependencies
├── pyproject.toml     # Project configuration
└── .env.example       # Environment variables example
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run tests (`uv run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the repository or contact the development team.