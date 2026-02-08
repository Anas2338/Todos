---
id: 032
title: "Fix Gemini Tools Format Error"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "3-chatbot-integration"
user: "user"
command: "Fix tools format in Gemini API request"
labels: ["bug", "api", "llm", "gemini", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

## Files Modified

- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\src\services\llm_client.py

## Tests Added/Modified

- N/A (Configuration fix, no new tests added)

## Prompt Text

Fix the "Invalid JSON payload received. Unknown name \"tools\": Cannot find field." error in the Gemini API. The error indicates that the tools field format is incorrect according to the Gemini API specification.

## Response Text

Fixed the tools format in the Gemini API request by updating the payload structure:

1. Updated the tools format in both generate_response and chat_completions methods in GeminiClient
2. Changed from `{"type": "function", "function_declarations": tools}` to `{"function_declarations": tools}`
3. This aligns with the Google Gemini API specification for function declarations in tool calling

The Google Gemini API expects the tools field to contain an array of objects with function_declarations property, without the "type" field that was causing the validation error.

## Outcome

The Gemini API should now properly accept the tools parameter when function calling is used, resolving the 400 error related to invalid tools format.

## Evaluation

The fix addresses the root cause: incorrect tools field format in the API request. The solution uses the correct format expected by the Google Generative Language API.