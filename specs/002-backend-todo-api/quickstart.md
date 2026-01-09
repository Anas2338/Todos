# Quickstart: Backend & Testing Todo API

## Prerequisites

- Python 3.11+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- UV package manager
- pip package manager (as backup)

## Setup

1. **Install UV package manager:**
   ```bash
   # Install UV globally
   pip install uv
   ```

2. **Set up the project using UV:**
   ```bash
   # Navigate to project directory
   cd backend

   # Install dependencies with UV
   uv pip install -r requirements.txt

   # Or if using pyproject.toml
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your specific values:
   DATABASE_URL="postgresql://user:password@localhost/dbname"
   SECRET_KEY="your-secret-key-here"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   UV_LICENSE="your-license-key"  # if applicable
   ```

4. **Initialize the database:**
   ```bash
   # Run database migrations to create tables
   python -m alembic upgrade head
   ```

## Running the API

1. **Start the development server:**
   ```bash
   uv run python -m main
   # Or using FastAPI's uvicorn directly:
   uv run uvicorn src.api.main:app --reload --port 8000
   ```

2. **The API will be available at:** `http://localhost:8000`

## API Usage Examples

### Authentication
```bash
# Sign up
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Sign in
curl -X POST "http://localhost:8000/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Todo Operations (with JWT token)
```bash
# Create a task
curl -X POST "http://localhost:8000/api/{user_id}/tasks" \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description"}'

# Get all tasks for user
curl -X GET "http://localhost:8000/api/{user_id}/tasks" \
  -H "Authorization: Bearer {jwt_token}"

# Update a task
curl -X PUT "http://localhost:8000/api/{user_id}/tasks/{task_id}" \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "Updated description"}'

# Complete a task
curl -X PATCH "http://localhost:8000/api/{user_id}/tasks/{task_id}/complete" \
  -H "Authorization: Bearer {jwt_token}" \
  -d '{"completed": true}'
```

## Running Tests

1. **Run the full test suite:**
   ```bash
   # Using UV
   uv run pytest tests/ -v

   # Or with specific options
   uv run pytest tests/ -v --cov=src
   ```

2. **Run specific test categories:**
   ```bash
   # Unit tests
   uv run pytest tests/unit/ -v

   # Integration tests
   uv run pytest tests/integration/ -v

   # Contract tests
   uv run pytest tests/contract/ -v
   ```

## Managing Dependencies with UV

1. **Add a new dependency:**
   ```bash
   uv pip install new-package
   uv pip freeze > requirements.txt
   ```

2. **Update dependencies:**
   ```bash
   uv pip sync requirements.txt
   ```

3. **Create virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token signing
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration time (default: 7)
- `UV_LICENSE`: UV license key if using licensed features