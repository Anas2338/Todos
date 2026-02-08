# Implementation Plan: AI Chatbot Integration for Todo Application

**Branch**: `3-ai-chatbot-integration` | **Date**: 2026-01-17 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/[3-ai-chatbot-integration]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless AI chatbot backend that enables natural language todo management. The system uses an OpenAI Agent that connects to a Gemini LLM via external HTTP client, with MCP tools exposing todo operations. Conversation state is persisted in the database and reconstructed on each request, with all operations authenticated through Better Auth.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Better Auth, UV
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Web backend
**Performance Goals**: AI responses delivered in under 3 seconds, support for 100 concurrent users
**Constraints**: <3 second p95 response time, stateless agent and MCP tools, no in-memory persistence
**Scale/Scope**: 100 concurrent users, 1000 messages per conversation session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Spec-Driven Development First**: Implementation follows the detailed specification created in `/specs/3-ai-chatbot-integration/spec.md`
- ✅ **Zero Manual Code Authoring**: All code will be generated via Claude Code
- ✅ **Iterative Refinement of Specs**: Specification has been clarified with 5 key questions answered
- ✅ **Natural Language Usability via AI Agents**: System implements AI agent for natural language todo management
- ✅ **Cloud-Native, Production-Aligned Architecture**: Architecture uses modern Python web stack with PostgreSQL
- ✅ **Spec-First Feature Development**: Feature has complete specification before implementation
- ✅ **Technology and Compliance Standards**: Uses required technologies (FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel)
- ✅ **Development Workflow and Quality Gates**: Building on Phase II backend as required

## Project Structure

### Documentation (this feature)

```text
specs/3-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
chatbot_backend/
├── src/
│   ├── main.py                  # FastAPI application entry point
│   ├── chat/
│   │   ├── api.py               # Chat endpoint implementation
│   │   ├── agent.py             # AI agent orchestration
│   │   └── models.py            # Chat-specific data models
│   ├── mcp_server/
│   │   ├── server.py            # MCP server implementation
│   │   ├── tools.py             # Todo MCP tools
│   │   └── models.py            # MCP-specific data models
│   ├── core/
│   │   ├── auth.py              # Better Auth integration
│   │   ├── database.py          # Database connection and session management
│   │   └── config.py            # Configuration management
│   ├── models/                  # Shared data models (SQLModel)
│   │   ├── user.py              # User model (from Phase II)
│   │   ├── task.py              # Task model (from Phase II)
│   │   ├── chat_session.py      # ChatSession model
│   │   ├── chat_message.py      # ChatMessage model
│   │   └── tool_invocation.py   # ToolInvocation model
│   └── services/
│       ├── todo_service.py      # Todo business logic (from Phase II)
│       ├── chat_service.py      # Chat session management
│       └── llm_client.py        # External Gemini client
├── tests/
│   ├── unit/
│   │   ├── test_mcp_tools.py    # Unit tests for MCP tools
│   │   ├── test_chat_api.py     # Unit tests for chat API
│   │   └── test_agent.py        # Unit tests for agent logic
│   ├── integration/
│   │   ├── test_chat_integration.py  # Integration tests for chat flow
│   │   └── test_mcp_integration.py   # Integration tests for MCP tools
│   └── contract/
│       └── test_api_contracts.py     # Contract tests for API endpoints
└── scripts/
    └── start_mcp_server.py      # Script to start MCP server
```

**Structure Decision**: Backend-only structure with clear separation of concerns between chat API, AI agent, MCP tools, and shared models/services. The structure supports the required architecture of Chat API → Agent → MCP Server → Database with proper authentication and authorization.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |