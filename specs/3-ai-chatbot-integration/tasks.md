# Implementation Tasks: AI Chatbot Integration for Todo Application

**Feature**: AI Chatbot Integration for Todo Application
**Branch**: `3-ai-chatbot-integration`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Implementation Strategy

Build the AI chatbot integration in phases following the user story priorities (P1, P2, P3). Start with core functionality for natural language todo management (User Story 1), then add persistent conversation context (User Story 2), and finally secure multi-user isolation (User Story 3). Each phase builds incrementally and remains independently testable.

**MVP Scope**: Complete User Story 1 (Natural Language Todo Management) with minimal viable functionality including chat API, basic AI agent, and core MCP tools for task creation, listing, and completion.

## Phase 1: Setup Tasks

Initialize project structure and dependencies for the chatbot backend.

- [x] T001 Create project directory structure per plan: chatbot_backend/src/, chatbot_backend/tests/, chatbot_backend/scripts/
- [x] T002 Initialize pyproject.toml with required dependencies: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Better Auth, python-dotenv
- [x] T003 Create .env template with required environment variables (DATABASE_URL, GEMINI_API_KEY, BETTER_AUTH_SECRET, etc.)
- [x] T004 Set up basic configuration module at chatbot_backend/src/core/config.py
- [x] T005 Configure logging at chatbot_backend/src/core/logging.py
- [x] T006 Create database connection module at chatbot_backend/src/core/database.py

## Phase 2: Foundational Tasks

Core infrastructure and shared components that all user stories depend on.

- [x] T007 [P] Create SQLModel base model at chatbot_backend/src/models/base.py
- [x] T008 [P] Create ChatSession model at chatbot_backend/src/models/chat_session.py
- [x] T009 [P] Create ChatMessage model at chatbot_backend/src/models/chat_message.py
- [x] T010 [P] Create ToolInvocation model at chatbot_backend/src/models/tool_invocation.py
- [x] T011 [P] Import and reference existing User and Task models from Phase II
- [x] T012 Create database session management at chatbot_backend/src/core/database.py
- [x] T013 Implement authentication middleware using Better Auth at chatbot_backend/src/core/auth.py
- [x] T014 Create rate limiting middleware at chatbot_backend/src/core/rate_limiter.py
- [x] T015 Create gemini LLM client at chatbot_backend/src/services/llm_client.py
- [x] T016 Create chat service at chatbot_backend/src/services/chat_service.py
- [x] T017 Create todo service wrapper for Phase II logic at chatbot_backend/src/services/todo_service.py

## Phase 3: User Story 1 - Natural Language Todo Management (Priority: P1)

Enable users to manage tasks using natural language. This is the core value proposition of the feature.

**Goal**: Users can create, list, and update tasks using natural language phrases like "Create a task to buy groceries" or "Show me my tasks".

**Independent Test**: Can be fully tested by sending natural language messages to the chat endpoint and verifying that the appropriate todo operations are performed, delivering the core AI-powered todo management functionality.

### Tests for User Story 1
- [ ] T018 [P] [US1] Create unit test for create_task MCP tool
- [ ] T019 [P] [US1] Create unit test for list_tasks MCP tool
- [ ] T020 [P] [US1] Create unit test for update_task MCP tool
- [ ] T021 [P] [US1] Create integration test for chat API with create_task
- [ ] T022 [P] [US1] Create integration test for chat API with list_tasks

### Models for User Story 1
- [x] T023 [P] [US1] Implement validation logic in ChatSession model
- [x] T024 [P] [US1] Implement validation logic in ChatMessage model
- [x] T025 [P] [US1] Implement validation logic in ToolInvocation model

### Services for User Story 1
- [x] T026 [US1] Enhance chat service to handle session creation and message persistence
- [x] T027 [US1] Enhance todo service to handle task operations from MCP tools

### MCP Tools for User Story 1
- [x] T028 [P] [US1] Create MCP server module at chatbot_backend/src/mcp_server/server.py
- [x] T029 [P] [US1] Create MCP tools module at chatbot_backend/src/mcp_server/tools.py
- [x] T030 [P] [US1] Implement create_task MCP tool
- [x] T031 [P] [US1] Implement list_tasks MCP tool
- [x] T032 [P] [US1] Implement get_task MCP tool
- [x] T033 [P] [US1] Implement update_task MCP tool
- [x] T034 [P] [US1] Implement set_task_complete MCP tool
- [x] T035 [P] [US1] Implement delete_task MCP tool

### Agent for User Story 1
- [x] T036 [US1] Create AI agent module at chatbot_backend/src/chat/agent.py
- [x] T037 [US1] Implement intent recognition for todo operations
- [x] T038 [US1] Connect agent to MCP tools
- [x] T039 [US1] Connect agent to Gemini LLM client

### API for User Story 1
- [x] T040 [US1] Create chat API module at chatbot_backend/src/chat/api.py
- [x] T041 [US1] Implement POST /sessions endpoint with authentication
- [x] T042 [US1] Implement GET /sessions endpoint with authentication
- [x] T043 [US1] Implement GET /sessions/{session_id}/messages endpoint with authentication

### Integration for User Story 1
- [x] T044 [US1] Integrate chat API with AI agent
- [x] T045 [US1] Add authentication to all chat endpoints
- [x] T046 [US1] Add rate limiting to chat endpoints

## Phase 4: User Story 2 - Persistent Conversation Context (Priority: P2)

Provide conversation memory across multiple messages and sessions.

**Goal**: Users have conversations with the AI that remember context across multiple messages, and can continue where they left off when returning later.

**Independent Test**: Can be tested by creating a conversation, performing multiple todo operations, ending the session, and resuming to verify that context and conversation history are properly maintained.

### Tests for User Story 2
- [ ] T046 [P] [US2] Create test for session continuation functionality
- [ ] T047 [P] [US2] Create test for conversation history reconstruction
- [ ] T048 [P] [US2] Create test for message ordering and retrieval

### Services for User Story 2
- [ ] T049 [US2] Enhance chat service to handle conversation history reconstruction
- [ ] T050 [US2] Implement message history pagination and limits
- [ ] T051 [US2] Add message archival functionality for sessions exceeding 1000 messages

### Agent for User Story 2
- [ ] T052 [US2] Enhance agent to utilize conversation history context
- [ ] T053 [US2] Implement context-aware intent recognition

### API for User Story 2
- [ ] T054 [US2] Enhance GET /sessions/{session_id}/messages with pagination
- [ ] T055 [US2] Add session metadata endpoints for titles and activity status

## Phase 5: User Story 3 - Secure Multi-User Isolation (Priority: P1)

Ensure complete isolation of user data and conversations.

**Goal**: Users can be confident that their todo data and conversations are completely isolated from other users, with proper authentication and authorization.

**Independent Test**: Can be tested by having multiple users interact with the system simultaneously, verifying that each user only sees their own data and cannot access others' information.

### Tests for User Story 3
- [ ] T056 [P] [US3] Create test for user data isolation in chat sessions
- [ ] T057 [P] [US3] Create test for user data isolation in tasks
- [ ] T058 [P] [US3] Create test for authorization failures
- [ ] T059 [P] [US3] Create test for cross-user data access prevention

### Models for User Story 3
- [x] T060 [US3] Enhance all models with user ownership validation
- [x] T061 [US3] Add foreign key constraints to enforce user ownership

### Services for User Story 3
- [x] T062 [US3] Enhance chat service to enforce user ownership checks
- [x] T063 [US3] Enhance todo service to enforce user ownership checks

### MCP Tools for User Story 3
- [x] T064 [US3] Add user ownership validation to all MCP tools
- [x] T065 [US3] Enhance error handling for unauthorized access attempts

### API for User Story 3
- [x] T066 [US3] Add user ownership validation to all chat endpoints
- [x] T067 [US3] Enhance authentication middleware to include user context in requests

## Phase 6: Polish & Cross-Cutting Concerns

Final touches, error handling, and additional features to enhance the system.

### Error Handling & Edge Cases
- [x] T068 Create error handling module at chatbot_backend/src/core/errors.py
- [x] T069 Enhance MCP tools with proper error responses for all failure cases
- [x] T070 Implement graceful handling for Gemini LLM unavailability
- [x] T071 Add input sanitization to prevent injection attacks
- [ ] T072 Implement proper error responses for ambiguous user intents

### Performance & Monitoring
- [x] T073 Add performance monitoring to measure response times
- [x] T074 Implement proper logging for debugging and monitoring
- [x] T075 Add health check endpoint at /health

### MCP Server Enhancement
- [x] T076 [P] Create MCP server startup script at chatbot_backend/scripts/start_mcp_server.py
- [x] T077 Add MCP server configuration options
- [x] T078 Add MCP server monitoring and health checks

### Documentation & Configuration
- [x] T079 Create main application entry point at chatbot_backend/src/main.py
- [x] T080 Configure application lifespan and startup/shutdown events
- [x] T081 Update documentation and README with setup instructions

## Dependencies

User Story 2 (Persistent Conversation Context) depends on User Story 1 (Natural Language Todo Management) being implemented first, as it builds upon the basic chat functionality. User Story 3 (Secure Multi-User Isolation) can be developed in parallel with User Story 1 but requires authentication to be in place first.

## Parallel Execution Opportunities

Many tasks can be executed in parallel, particularly:
- Model creation (T008-T011) can be done simultaneously
- MCP tool implementation (T030-T035) can be done in parallel
- Test creation can happen alongside implementation
- All tasks marked with [P] can be executed in parallel as they work on different components

## Acceptance Criteria

- Users can manage todos entirely via natural language (SC-001)
- System supports authenticated chat sessions with proper user isolation (SC-002)
- 90% of valid natural language todo commands result in correct MCP tool selection (SC-003)
- Chat conversation state persists correctly between requests (SC-004)
- All automated backend tests pass (SC-005)
- System integrates with Gemini LLM via external client (SC-006)
- AI responses delivered in under 3 seconds, supporting 100 concurrent users (SC-007)