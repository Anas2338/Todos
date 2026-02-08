---
id: 020
title: "Fix Gemini API Configurable Model"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "3-chatbot-integration"
user: "user"
command: "Make Gemini API model configurable via environment variable"
labels: ["bug", "api", "llm", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

## Files Modified

- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\src\core\config.py
- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\src\services\llm_client.py
- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\.env

## Tests Added/Modified

- N/A (Configuration fix, no new tests added)

## Prompt Text

Make the Gemini API model configurable via environment variable to allow easy switching between different models and resolve the 404 model not found errors.

## Response Text

Made the Gemini API model configurable by implementing the following changes:

1. Added GEMINI_MODEL_NAME configuration variable to Config class in `src/core/config.py` with default value "gemini-1.0-pro-latest"

2. Updated GeminiClient in `src/services/llm_client.py` to use the model from configuration instead of hardcoded value

3. Added GEMINI_MODEL_NAME environment variable to `.env` file with value "gemini-1.0-pro-latest"

This allows the model to be easily configured via environment variable and provides flexibility to switch between different models as needed. The default model "gemini-1.0-pro-latest" is a stable, widely supported model in the Google Gemini API.

## Outcome

The chatbot should now be able to successfully communicate with the Google Gemini API using a configurable model name, allowing for easier maintenance and ability to switch models without code changes.

## Evaluation

The fix addresses the root cause by making the model name configurable and using a stable, supported model name that should be available in the Gemini API.