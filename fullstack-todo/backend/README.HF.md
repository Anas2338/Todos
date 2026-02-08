---
title: Todo Backend API
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 8000
---

# Todo Backend API

A secure, multi-user Todo API backend with authentication built with FastAPI, SQLModel, and PostgreSQL.

## 🚀 Features

- **JWT Authentication** - Secure user registration and login
- **Task Management** - Full CRUD operations for tasks
- **User Isolation** - Users can only access their own tasks
- **Rate Limiting** - Protection against API abuse
- **Health Checks** - Monitor application status

## 📡 API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/signin` - Authenticate and get JWT token

### Tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks` - Get all tasks
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /health` - Health check endpoint

## 🔧 Environment Variables

This Space requires the following environment variables to be configured in the Space settings:

- `DATABASE_URL` - Database connection string (PostgreSQL or SQLite)
- `SECRET_KEY` - JWT signing key (use a strong random string)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)

## 📚 Technology Stack

- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL databases with Python types
- **JWT** - Secure authentication
- **Docker** - Containerized deployment
- **uv** - Fast Python package manager

## 🧪 Try It Out

1. Visit the `/docs` endpoint for interactive API documentation
2. Register a new user via `/auth/signup`
3. Sign in via `/auth/signin` to get your JWT token
4. Use the token to create and manage tasks

## 📖 Full Documentation

For complete documentation, setup instructions, and contribution guidelines, visit the [GitHub repository](https://github.com/yourusername/yourrepo).
