---
id: 3
title: architecture-plan
stage: plan
date_iso: 2026-01-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: 3-ai-chatbot-integration
branch: 3-ai-chatbot-integration
user: claude
command: /sp.plan
labels: ["plan", "architecture", "ai", "chatbot", "mcp", "backend"]
link_spec: ./spec.md
link_ticket: null
link_adr: null
link_pr: null
files_yaml:
  - "specs/3-ai-chatbot-integration/plan.md"
  - "specs/3-ai-chatbot-integration/research.md"
  - "specs/3-ai-chatbot-integration/data-model.md"
  - "specs/3-ai-chatbot-integration/contracts/chat-api-contract.md"
  - "specs/3-ai-chatbot-integration/contracts/mcp-todo-tools-contract.md"
  - "specs/3-ai-chatbot-integration/quickstart.md"
tests_yaml: []
---

# Architecture Plan for AI Chatbot Integration

## Prompt Text

```
/sp.plan

Create:
- High-level architecture sketch for Phase III AI chatbot backend layered on Phase II
- Component interaction diagram (Chat API → Agent → MCP Server → Database)
- Spec breakdown for Phase III backend (chat API, agent logic, MCP tools, persistence)
- Data flow for stateless chat with database-backed conversation state
- Dependency and package layout aligned with UV

Decisions needing documentation:
- MCP server topology (embedded vs. standalone service)
- Tool granularity (one tool per action vs. grouped operations)
- Agent prompting strategy (single-agent vs. multi-step reasoning)
- Gemini LLM integration approach via external client
- Conversation state persistence model (session-based vs. message-based)
- Authorization enforcement point (API, agent, or MCP layer)
- Reuse strategy for Phase II domain logic vs. direct DB access
- Error handling strategy for ambiguous or unsupported user intents

Testing strategy:
- Acceptance criteria mapping for:
  - Natural language → MCP tool selection
  - Correct task CRUD via chat
  - Stateless request handling with persisted history
  - Multi-user data isolation
  - Authentication and authorization failures
- Unit tests for MCP tools
- Integration tests for agent + MCP + database
- End-to-end tests for chat endpoint behavior
- Test database setup and teardown strategy
- Test execution via UV

Technical details:
- Strict spec-driven workflow (spec → Claude Code → validate → refine spec)
- Backend only; frontend explicitly excluded
- Use latest stable versions of all dependencies
- Project and dependency management using UV
- FastAPI for chat endpoint
- OpenAI Agents SDK for agent orchestration
- Gemini LLM accessed via external client (no generative AI SDK)
- Official MCP SDK for tool exposure
- SQLModel + Neon Serverless PostgreSQL for persistence
- Better Auth for authentication
- No in-memory state in agent or MCP tools

Planning structure:
- Phase III only
- Organize specs by:
  - Chat API layer
  - Agent behavior and prompts
  - MCP tool
```

## Response Text

Completed comprehensive architecture plan for AI Chatbot Integration feature, including:

1. Research document resolving key architectural decisions:
   - MCP server topology (embedded approach)
   - Tool granularity (individual tools per operation)
   - Agent prompting strategy (single-agent approach)
   - Gemini LLM integration via external HTTP client
   - Session-based conversation persistence
   - Authorization enforcement at API layer
   - Reuse of Phase II domain logic
   - Error handling for ambiguous intents

2. Implementation plan with technical context, constitution check, and project structure

3. Data model specification defining entities: ChatSession, ChatMessage, ToolInvocation (plus reused User and Task from Phase II)

4. API contracts for chat endpoints with authentication, rate limiting, and error handling

5. MCP contracts for all todo operations (create_task, list_tasks, get_task, update_task, delete_task, set_task_complete)

6. Quickstart guide with setup instructions, environment configuration, and usage examples

The plan establishes a clear architecture: Chat API → AI Agent → MCP Tools → Database with proper authentication at each layer and stateless operation backed by database persistence.