---
id: 028
title: "Switch to Qwen LLM API"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "3-chatbot-integration"
user: "user"
command: "Switch from Gemini to Qwen LLM API with multi-provider support"
labels: ["api", "llm", "qwen", "refactor", "integration"]
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

- N/A (Integration change, no new tests added)

## Prompt Text

Switch from Google Gemini API to Alibaba Cloud Qwen API for the LLM functionality, while maintaining multi-provider support capability.

## Response Text

Successfully switched from Google Gemini API to Alibaba Cloud Qwen API with multi-provider support:

1. Updated configuration in `src/core/config.py` to include Qwen API settings:
   - Added QWEN_API_KEY, QWEN_MODEL_NAME, and QWEN_BASE_URL configuration variables
   - Updated validation to allow either Gemini or Qwen API key to be provided

2. Completely refactored `src/services/llm_client.py` to support multiple LLM providers:
   - Added QwenClient class implementing the OpenAI-compatible API format
   - Updated GeminiClient to maintain existing functionality
   - Created LLMManager class to handle multiple providers and select primary client
   - Qwen API takes priority when available, falling back to Gemini if needed

3. Updated .env file to use Qwen API configuration instead of Gemini:
   - Removed Gemini API key and model settings
   - Added Qwen API key and model settings (currently empty for user to fill in)

The Qwen API implementation uses the OpenAI-compatible endpoint format at Alibaba Cloud's DashScope service, which follows the standard OpenAI API format with Bearer token authentication.

## Outcome

The chatbot backend now supports Qwen LLM API instead of Gemini, with the capability to support multiple providers simultaneously. The system can be easily switched between providers by configuring the appropriate API keys.

## Evaluation

The fix addresses the requirement to use Qwen API while maintaining flexibility for future provider changes. The implementation follows best practices with abstract interfaces and provider management.