---
id: 1
title: ai-chatbot-integration-spec
stage: spec
date_iso: 2026-01-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: 3-ai-chatbot-integration
branch: 3-ai-chatbot-integration
user: claude
command: /sp.specify
labels: ["spec", "ai", "chatbot", "todo", "backend"]
link_spec: null
link_ticket: null
link_adr: null
link_pr: null
files_yaml:
  - "specs/3-ai-chatbot-integration/spec.md"
  - "specs/3-ai-chatbot-integration/checklists/requirements.md"
tests_yaml: []
---

# AI Chatbot Integration Specification

## Prompt Text

```
Phase III — Backend AI Chatbot Integration for Todo Application

Target audience:
- Developers and reviewers evaluating AI-native backend architectures
- Hackathon judges assessing MCP usage, agent correctness, and system design

Objective:
- Extend the existing Phase II Todo backend with an AI-powered chatbot interface
- Enable natural-language Todo management via MCP tools and AI agents
- Reuse the Phase II web application backend and database
- Entire implementation must be generated via Claude Code using Spec-Kit Plus

Scope:
- Backend only
- AI chatbot integration layered on top of Phase II backend
- No frontend or UI implementation in this phase
- Stateless AI + MCP architecture with database-backed state

Baseline assumptions:
- Phase II backend already exists with:
  - FastAPI
  - SQLModel
  - Neon Serverless PostgreSQL
  - Better Auth authentication
  - REST endpoints for Todo CRUD
- Phase III must NOT reimplement existing Todo REST APIs
- Phase III must call existing domain logic or persistence layer

Architecture requirements:
- Backend: Python FastAPI (latest stable)
- AI Framework: OpenAI Agents SDK (latest stable)
- LLM Provider: Gemini (via external HTTP client)
- MCP Server: Official MCP SDK (latest stable)
- ORM: SQLModel (latest stable)
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth
- Project & dependency management: UV

LLM integration requirements:
- Use Gemini as the language model
- Gemini must be accessed via an external client (direct HTTP or SDK-level client)
- Do NOT use Google Generative AI SDK or `generativeai` libraries
- OpenAI Agents SDK must treat Gemini as an external model provider
- All prompts, tool calls, and responses must be explicitly defined in specs

Functional requirements:
- Support all 5 Basic Level Todo features via natural language:
  1. Create a task
  2. List tasks
  3. Update a task
  4. Delete a task
  5. Mark a task complete or incomplete
- User messages may be free-form natural language
- AI agent must translate intent into structured MCP tool calls
- AI agent must not modify data directly

MCP server requirements:
- Implement an MCP server using the Official MCP SDK
- Expose Todo operations as stateless MCP tools:
  - create_task
  - list_tasks
  - get_task
  - update_task
  - delete_task
  - set_task_complete
- MCP tools must:
  - Be stateless
  - Persist all state via the database
  - Enforce user ownership and authorization
  - Reuse Phase II domain logic where possible

AI agent requirements:
- Implement an OpenAI Agent that:
  - Receives user messages
  - Determines intent
  - Selects appropriate MCP tool(s)
  - Calls MCP tools with validated arguments
  - Produces a natural-language response based on tool output
- Agent must never hallucinate task data
- Agent must never bypass MCP tools
- Agent must not maintain in-memory state between requests

Chat API requirements:
- Implement a stateless FastAPI chat endpoint:
  - Accepts user message
  - Loads conversation history from database
  - Invokes AI agent
  - Persists new messages and tool calls
- Conversation state must be reconstructed on every request
- Chat must be authenticated using Better Auth
- Chat data must be scoped per user

Data model requirements:
- Persist the following entities:
  - ChatSession
  - ChatMessage
  - ToolInvocation (optional but recommended)
- Reuse existing User and Task models from Phase II
- Enforce strict multi-user isolation at all layers

Testing requirements:
- Implement automated backend tests generated via Claude Code
- Tests must validate:
  - Natural language → correct MCP tool selection
  - Correct task mutations via chat
  - Stateless chat behavior with persisted history
  - User isolation and authorization
  - Failure handling for ambiguous or invalid commands
- Tests must be runnable via UV

UV and dependency requirements:
- Use UV for all dependency and project management
- Use latest stable versions of:
  - FastAPI
  - OpenAI Agents SDK
  - Official MCP SDK
  - SQLModel
- Define runtime and test dependencies in `pyproject.toml`
- No undeclared or implicit dependencies

Non-functional requirements:
- Strict spec-driven development
- No manual code writing or editing
- Clear separation of:
  - Chat API
  - Agent logic
  - MCP tools
  - Persistence
- Deterministic regeneration from specs

Deliverables:
- Phase III backend specs stored in `specs/`
- Claude-generated FastAPI chatbot backend
- MCP server implementation
- OpenAI Agent configuration using Gemini via external client
- SQLModel schemas for chat persistence
- Automated backend test suite
- Documentation describing how to run chatbot backend using UV

Success criteria:
- Users can manage Todos entirely via natural language
- AI agent uses MCP tools exclusively
- Gemini LLM is used via external client
- No in-memory state exists in agent or MCP tools
- All tests pass
- Backend can be regenerated solely from specs

Constraints:
- No frontend or UI implementation
- No reimplementation of Phase II Todo APIs
- No manual code authoring
- No use of Google Generative AI SDK
- No deviation fro
```

## Response Text

Created comprehensive specification for AI Chatbot Integration feature, including user scenarios, functional requirements, key entities, and success criteria. The spec defines a natural language interface for todo management using AI agents and MCP tools, with proper authentication, data persistence, and user isolation.
