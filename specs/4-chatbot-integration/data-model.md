# Data Model: Chatbot Frontend Integration

## Entities

### Chat Message
Represents a single message in the conversation

**Fields**:
- `id`: string - Unique identifier for the message
- `content`: string - The text content of the message
- `sender`: 'user' | 'assistant' - Indicates the sender of the message
- `timestamp`: Date - When the message was sent
- `status`: 'sent' | 'sending' | 'error' - Current status of the message transmission
- `conversationId`: string - Reference to the conversation this message belongs to

**Validation rules**:
- `id` must be unique within the conversation
- `content` must not be empty
- `sender` must be either 'user' or 'assistant'
- `timestamp` must be in the past or present

### Conversation
Represents a collection of chat messages associated with a specific authenticated user, retained for 30 days

**Fields**:
- `id`: string - Unique identifier for the conversation
- `userId`: string - Reference to the authenticated user who owns this conversation
- `messages`: Array<ChatMessage> - List of messages in the conversation
- `createdAt`: Date - When the conversation was started
- `updatedAt`: Date - When the last message was added
- `expiresAt`: Date - When the conversation will expire (30 days after last activity)

**Validation rules**:
- `id` must be unique
- `userId` must correspond to an authenticated user
- `messages` must be an array of valid ChatMessage objects
- `createdAt` must be before `updatedAt`
- `expiresAt` must be 30 days after the last activity

### Todo Task
Represents a task entity that can be manipulated through chat commands, including title, description, due date, and completion status

**Fields**:
- `id`: string - Unique identifier for the task
- `title`: string - The main title of the task
- `description`: string - Optional detailed description of the task
- `dueDate`: Date | null - Optional due date for the task
- `completed`: boolean - Whether the task is completed or not
- `createdAt`: Date - When the task was created
- `updatedAt`: Date - When the task was last updated
- `userId`: string - Reference to the user who owns this task

**Validation rules**:
- `id` must be unique
- `title` must not be empty
- `completed` defaults to false
- `createdAt` must be before `updatedAt`
- `userId` must correspond to an authenticated user

### Chat Session
Represents the current chat session state for the user interface

**Fields**:
- `isActive`: boolean - Whether the chat modal is currently open
- `isLoading`: boolean - Whether the chat interface is loading
- `currentInput`: string - The current text in the chat input field
- `selectedConversationId`: string | null - The ID of the currently viewed conversation
- `error`: string | null - Any error message to display to the user
- `lastActivity`: Date - When the last interaction occurred

**Validation rules**:
- `currentInput` length should be reasonable (e.g., less than 1000 characters)
- `selectedConversationId` must correspond to an existing conversation if not null

## Relationships

- **User** (1) to **Conversations** (Many): Each user can have multiple conversations
- **Conversation** (1) to **Chat Messages** (Many): Each conversation contains multiple messages
- **User** (1) to **Todo Tasks** (Many): Each user can have multiple tasks
- **Chat Session** (1) to **Conversation** (1): Each session corresponds to one active conversation

## State Transitions

### Chat Message States
```
[Initial State] → sending → [sent/error]
                   ↓
                sent (final)
                   ↓
                delivered (backend)
```

### Chat Session States
```
closed → opening → open → closing → closed
   ↑                           ↓
   ←------ error handling ------
```

## API Endpoints

### Chat API Endpoints
- `POST /api/chat/send` - Send a new message to the backend
  - Request: `{message: string, conversationId?: string}`
  - Response: `{success: boolean, conversationId: string, message: ChatMessage}`
- `GET /api/chat/history` - Retrieve conversation history
  - Request: `{conversationId?: string}`
  - Response: `{conversation: Conversation}`
- `POST /api/chat/start` - Start a new conversation
  - Request: `{}`
  - Response: `{conversationId: string, initialMessage?: ChatMessage}`

### Todo API Endpoints (via chat commands)
- Commands are processed by the backend which interfaces with the existing Todo API
- Natural language commands like "Add task", "Complete task", etc. are translated to appropriate Todo API calls