# Research: In-Memory Todo Python Console Application

## Phase 0: Technical Research and Decision Log

### Decision: Task Data Structure
**Rationale**: Using a Python class for Task objects provides better structure, validation, and extensibility than dictionaries. Classes allow for methods to manage state transitions and provide better type safety.
**Alternatives considered**:
- Dictionary approach (simpler but less structured)
- NamedTuple (immutable but less flexible)

### Decision: In-Memory Storage Approach
**Rationale**: Using a Python dictionary with sequential numeric IDs as keys provides O(1) lookup performance and maintains the requirement for sequential IDs. The dictionary will be stored as an instance variable in a TodoManager class.
**Alternatives considered**:
- List-based storage (would require searching for specific IDs)
- Global variables (not recommended for maintainability)

### Decision: CLI Interaction Style
**Rationale**: Interactive command prompt interface allows continuous interaction without restarting the application. Users can enter commands like "add", "list", "update", etc. with appropriate arguments.
**Alternatives considered**:
- Menu-driven interface with numbered options (less flexible)
- Single command with arguments (requires restarting for each operation)

### Decision: Error Handling Strategy
**Rationale**: Implement a custom exception hierarchy with clear, user-friendly messages that explain what went wrong and suggest how to fix it. This aligns with the specification requirement for clear error feedback.
**Alternatives considered**:
- Generic error handling (less informative)
- Technical error codes (not user-friendly)

### Decision: Separation of Concerns
**Rationale**:
- `models.py`: Contains Task class and related data models
- `storage.py`: Handles in-memory storage operations (add, retrieve, update, delete)
- `cli.py`: Manages user input/output and command parsing
- `main.py`: Orchestrates the application and handles the main loop
This separation ensures each module has a single responsibility and improves testability.
**Alternatives considered**:
- Monolithic approach (harder to maintain)
- Different separation boundaries (less clear responsibilities)

### Decision: Python Packaging
**Rationale**: Using pyproject.toml with a console script entry point allows users to run the application with a simple command like "todo-app". This follows Python packaging best practices and aligns with UV conventions.
**Alternatives considered**:
- Direct script execution (less user-friendly)
- Setup.py (older approach, pyproject.toml is preferred)

### Decision: Dependency Management
**Rationale**: For this Phase I implementation, using only Python standard library modules (stdlib-only) keeps the application lightweight and eliminates external dependencies. This aligns with the constraint of no external libraries.
**Alternatives considered**:
- Minimal dependencies for enhanced functionality (violates Phase I constraint of no external libraries)
- Third-party CLI frameworks (would require external dependencies)

### Decision: Entry Point Configuration
**Rationale**: Configuring a console script entry point in pyproject.toml as "todo-app = src.todo_app.main:main" provides a clean CLI interface for users to run the application.
**Alternatives considered**:
- Direct module execution (python -m src.todo_app.main)
- Multiple entry points (unnecessary for single application)