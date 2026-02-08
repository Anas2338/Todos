# Research: AI Chatbot Integration for Todo Application

## Decision: MCP Server Topology
**Rationale**: For tight integration with the existing Phase II backend and to minimize deployment complexity, an embedded MCP server within the same FastAPI application is preferred over a standalone service. This approach allows shared database connections and authentication mechanisms while maintaining the separation of concerns between the MCP tools and the chat API.
**Alternatives considered**: Standalone MCP service would provide better isolation but add network overhead and deployment complexity.

## Decision: Tool Granularity
**Rationale**: Individual tools for each todo operation (create_task, list_tasks, get_task, update_task, delete_task, set_task_complete) provide better observability and maintainability compared to grouped operations. This aligns with the requirement to expose specific MCP tools as defined in the spec.
**Alternatives considered**: Grouped operations (e.g., a single todo_operation tool with action parameter) would reduce the number of tools but decrease clarity.

## Decision: Agent Prompting Strategy
**Rationale**: A single-agent approach with structured prompting is sufficient for the todo management domain. The agent will receive conversation history and current user intent, then select appropriate MCP tools. Multi-step reasoning is not required for basic todo operations.
**Alternatives considered**: Multi-agent systems would add complexity without clear benefits for simple todo operations.

## Decision: Gemini LLM Integration Approach
**Rationale**: Using the Gemini API via HTTP client (requests/HTTPX) provides direct control over the integration while satisfying the requirement to avoid Google Generative AI SDK. The OpenAI Agent SDK can be configured to call this external client through custom tool integration.
**Alternatives considered**: Using Gemini via OpenAI-compatible API wrappers would simplify integration but might limit access to Gemini-specific features.

## Decision: Conversation State Persistence Model
**Rationale**: Session-based persistence with individual messages stored separately provides the right balance of performance and flexibility. Each ChatSession contains metadata, and ChatMessages are linked to sessions with timestamps for ordering. This enables reconstruction of conversation state on each request as required.
**Alternatives considered**: Storing entire conversation context as a single blob would be simpler but less flexible for querying and management.

## Decision: Authorization Enforcement Point
**Rationale**: Authorization will be enforced at the API layer (FastAPI chat endpoint) using Better Auth middleware. The MCP tools will receive authenticated user context from the API layer, ensuring that all operations are performed on behalf of a validated user.
**Alternatives considered**: Enforcing authorization at the MCP layer would duplicate authentication logic and add complexity.

## Decision: Phase II Domain Logic Reuse Strategy
**Rationale**: The existing Phase II domain logic will be imported and called directly from the MCP tools. This satisfies the requirement to reuse existing logic without reimplementing Todo CRUD operations. The MCP tools serve as a translation layer from natural language to structured API calls.
**Alternatives considered**: Direct database access would bypass existing validation and business logic, violating the spec requirements.

## Decision: Error Handling Strategy for Ambiguous Intents
**Rationale**: The AI agent will be designed to return clarifying questions when user intent is ambiguous, rather than guessing or failing silently. This provides a better user experience and prevents unintended operations. The agent will recognize when it lacks sufficient information to call an MCP tool safely.
**Alternatives considered**: Failing with an error would provide less helpful feedback to users.