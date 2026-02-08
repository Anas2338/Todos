# Data Model: AI Chatbot Integration for Todo Application

## Entity: ChatSession
**Description**: Represents a user's chat session with metadata for managing conversation context

**Fields**:
- id (UUID/Integer): Primary key, unique identifier for the session
- user_id (UUID/Integer): Foreign key linking to User entity from Phase II
- created_at (DateTime): Timestamp when session was created
- updated_at (DateTime): Timestamp when session was last updated
- title (String): Optional title for the conversation (derived from first message or user-provided)
- is_active (Boolean): Flag indicating if session is currently active

**Relationships**:
- Belongs to: User (many-to-one)
- Has many: ChatMessage (one-to-many)
- Has many: ToolInvocation (one-to-many, optional)

**Validation Rules**:
- user_id must reference an existing User
- created_at must be in the past
- updated_at must be >= created_at

## Entity: ChatMessage
**Description**: Represents individual messages in a conversation between user and assistant

**Fields**:
- id (UUID/Integer): Primary key, unique identifier for the message
- session_id (UUID/Integer): Foreign key linking to ChatSession
- role (String): Message role ('user' or 'assistant')
- content (Text): The actual message content
- timestamp (DateTime): When the message was sent/received
- message_metadata (JSON): Additional metadata (token counts, etc.)

**Relationships**:
- Belongs to: ChatSession (many-to-one)
- Belongs to: User (through session, many-to-one)

**Validation Rules**:
- session_id must reference an existing ChatSession
- role must be either 'user' or 'assistant'
- content must not be empty
- timestamp must be in the past

**Constraints**:
- Limited to 1000 most recent messages per session (with oldest auto-archived as per spec)

## Entity: ToolInvocation
**Description**: Represents calls made to MCP tools, including arguments, results, and execution context

**Fields**:
- id (UUID/Integer): Primary key, unique identifier for the invocation
- session_id (UUID/Integer): Foreign key linking to ChatSession
- tool_name (String): Name of the MCP tool invoked
- arguments (JSON): Arguments passed to the tool
- result (JSON): Result returned by the tool
- timestamp (DateTime): When the tool was invoked
- status (String): Status of the invocation ('success', 'error', 'pending')

**Relationships**:
- Belongs to: ChatSession (many-to-one)

**Validation Rules**:
- session_id must reference an existing ChatSession
- tool_name must be one of the defined MCP tools
- timestamp must be in the past
- status must be one of the allowed values

## Entity: User (Reused from Phase II)
**Description**: Represents authenticated users (reused from existing Phase II implementation)

**Fields**:
- id (UUID/Integer): Primary key
- email (String): User's email address
- [Additional fields as defined in Phase II]

## Entity: Task (Reused from Phase II)
**Description**: Represents todo items (reused from existing Phase II implementation)

**Fields**:
- id (UUID/Integer): Primary key
- title (String): Task title
- description (Text): Optional task description
- is_completed (Boolean): Whether the task is completed
- user_id (UUID/Integer): Owner of the task
- created_at (DateTime): When the task was created
- updated_at (DateTime): When the task was last updated
- [Additional fields as defined in Phase II]

## State Transitions

### ChatSession
- Created when user starts a new chat session
- Updated when new messages are added
- Deactivated when user ends session or after inactivity period

### ChatMessage
- Created when user sends a message or agent responds
- Immutable once created (no updates allowed)

### ToolInvocation
- Created when agent invokes an MCP tool
- Status updated to 'success' or 'error' after execution
- Result populated after execution

### Task (from Phase II)
- Created via create_task MCP tool
- Updated via update_task or set_task_complete MCP tools
- Deleted via delete_task MCP tool

## Relationships and Access Control

- Users can only access their own ChatSessions and associated ChatMessages
- Users can only perform operations on their own Tasks
- ToolInvocations are scoped to the user's session
- Foreign key constraints ensure referential integrity
- Database-level cascading deletes may be used to maintain consistency