---
id: 027
title: "Fix Gemini API Tools Format"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "3-chatbot-integration"
user: "user"
command: "Fix tools format for Gemini API"
labels: ["bug", "api", "llm", "configuration"]
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

Fix the tools format in the Gemini API request. The API was returning a 400 error with "Invalid JSON payload received. Unknown name 'tools': Cannot find field." This indicates that the tools field format was incorrect.

## Response Text

Fixed the tools format in the Gemini API request by updating the structure to match Google's API specification:

1. Changed the tools format from `{"function_declarations": tools}` to `{"type": "function", "function_declarations": tools}` in both generate_response and chat_completions methods

This corrects the JSON payload structure to match what the Google Generative Language API expects for function calling, resolving the 400 error related to invalid tools format.

## Outcome

The Gemini API should now properly accept the tools parameter when function calling is used, with the correct field structure.

## Evaluation

The fix addresses the root cause: incorrect tools field format in the API request. The solution uses the correct format expected by the Google Generative Language API.