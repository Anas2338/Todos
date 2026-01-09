# Research: Backend & Testing Todo API

## Decision: FastAPI with SQLModel and Better Auth Stack
**Rationale**: FastAPI provides high performance with automatic API documentation, SQLModel offers SQL database integration with Pydantic compatibility, and Better Auth handles secure authentication flows. This stack is well-maintained and provides all required functionality for the todo API.

**Alternatives considered**:
- Flask with SQLAlchemy: Less performant and requires more manual work for documentation
- Django: More heavyweight than needed for this API-only application
- Express.js: Would require different language ecosystem

## Decision: Bcrypt for Password Hashing
**Rationale**: Bcrypt is the industry standard for password hashing, providing built-in salting and adjustable work factors. It's well-supported in Python and provides excellent security characteristics for password storage.

**Alternatives considered**:
- Argon2: Also secure but less commonly used in Python ecosystem
- PBKDF2: Less secure than bcrypt/Argon2
- Scrypt: Good security but bcrypt is more established

## Decision: Alembic for Database Migrations
**Rationale**: Alembic is the standard migration tool for SQLAlchemy-based applications (which SQLModel is built on). It provides automated migration generation and supports complex database schema changes across environments.

**Alternatives considered**:
- Manual SQL scripts: Error-prone and difficult to manage across environments
- Raw SQLModel migrations: Doesn't exist, SQLModel uses SQLAlchemy under the hood
- Third-party tools: Less integrated with the SQLAlchemy ecosystem

## Decision: pytest for Testing Framework
**Rationale**: Pytest is the standard Python testing framework with excellent FastAPI integration. It provides powerful fixtures, parameterized testing, and clear test reporting that works well with API testing.

**Alternatives considered**:
- unittest: More verbose and less feature-rich than pytest
- nose: No longer actively maintained
- doctest: Not appropriate for complex API testing

## Decision: UV for Project Management
**Rationale**: UV is a modern, fast Python package manager that provides reproducible installs and dependency management. It's faster than pip-tools and integrates well with modern Python development workflows.

**Alternatives considered**:
- pip-tools: Slower than UV and less modern
- Poetry: More complex than needed for this project
- pip + requirements.txt: Less reliable for reproducible installs

## Decision: Per-User/IP Rate Limiting with Standard Thresholds
**Rationale**: Implementing rate limiting per user/IP with standard thresholds (100 requests per minute) provides good protection against abuse while allowing normal usage patterns. This is a common and effective approach for API protection.

**Alternatives considered**:
- No rate limiting: Would leave the API vulnerable to abuse
- Different thresholds per endpoint: More complex to implement and manage
- IP-only (not per-user): Would limit legitimate users sharing IPs

## Decision: Structured Logging, Metrics, and Request Tracing
**Rationale**: Implementing comprehensive observability with structured logging, metrics collection, and request tracing is essential for monitoring system health, debugging issues, and maintaining reliability in production systems.

**Alternatives considered**:
- Basic logging only: Insufficient for production monitoring needs
- Metrics only: Missing debugging capabilities
- No specific observability: Would make troubleshooting difficult