---
id: 023
title: "Fix Gemini API Current Model"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "3-chatbot-integration"
user: "user"
command: "Update to use currently supported Gemini model"
labels: ["bug", "api", "llm", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

## Files Modified

- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\.env

## Tests Added/Modified

- N/A (Configuration fix, no new tests added)

## Prompt Text

Update the Gemini API to use a currently supported model name. The previous attempts with "gemini-1.0-pro-latest" and "gemini-pro" were not working, so update to use "gemini-1.5-flash" which is currently supported.

## Response Text

Updated the Gemini API model name to use a currently supported model:

1. Changed GEMINI_MODEL_NAME from "gemini-pro" to "gemini-1.5-flash" in the .env file

This should resolve the ongoing 404 error that was occurring when the chatbot tried to process messages through the Gemini API, as "gemini-1.5-flash" is a currently supported and actively maintained model in the Google Gemini API.

Combined with the previous URL format fix, the API should now construct the correct endpoint format: https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}

## Outcome

The chatbot should now be able to successfully communicate with the Google Gemini API using the correct URL format and a currently supported model name, allowing the AI functionality to work properly.

## Evaluation

The fix addresses the continuing issue by using the "gemini-1.5-flash" model name which should be currently available in the Gemini API when combined with the correct URL format.