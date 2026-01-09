# Data Model: Backend & Testing Todo API

## User Entity

**Fields:**
- `id` (UUID): Unique identifier for the user
- `email` (String): User's email address (unique, required)
- `password_hash` (String): Hashed password using bcrypt (required)
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Validation:**
- Email: Valid email format, unique across all users
- Password: At least 8 characters with complexity requirements (handled by bcrypt)

**Relationships:**
- One-to-Many: User has many Tasks

## Task Entity

**Fields:**
- `id` (UUID): Unique identifier for the task
- `title` (String): Task title (1-100 characters, required)
- `description` (String): Task description (0-1000 characters, optional)
- `completed` (Boolean): Completion status (default: false)
- `user_id` (UUID): Foreign key to User (required)
- `created_at` (DateTime): Task creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Validation:**
- Title: 1-100 characters
- Description: 0-1000 characters
- User ID: Must reference an existing user

**Relationships:**
- Many-to-One: Task belongs to one User

## Database Schema Constraints

- **Foreign Key Constraints**: Task.user_id references User.id
- **Unique Constraints**: User.email must be unique
- **Indexing**: Index on User.email for fast lookups, indexes on created_at fields
- **Referential Integrity**: Cascade delete on User deletion removes associated Tasks
- **Connection Pooling**: Configured for performance with concurrent access