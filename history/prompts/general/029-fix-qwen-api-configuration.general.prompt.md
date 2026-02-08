---
id: 029
title: "Fix Qwen API Configuration"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "3-chatbot-integration"
user: "user"
command: "Update Qwen API base URL and endpoint path"
labels: ["api", "llm", "qwen", "configuration", "bug"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

## Files Modified

- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\src\core\config.py
- E:\giaic\Agentic-AI\Todos\fullstack-todo\chatbot_backend\src\services\llm_client.py

## Tests Added/Modified

- N/A (Configuration fix, no new tests added)

## Prompt Text

Update the Qwen API configuration to use the correct base URL and endpoint path. The previous configuration was using an incorrect endpoint path that resulted in API errors.

## Response Text

Fixed the Qwen API configuration by updating both the base URL and endpoint path:

1. Updated configuration in `src/core/config.py`:
   - Changed QWEN_BASE_URL from "https://dashscope.aliyuncs.com/compatible-mode/v1" to "https://dashscope.aliyuncs.com/api/v1"

2. Updated endpoint paths in `src/services/llm_client.py`:
   - Changed both API call endpoints from "/chat/completions" to "/services/aigc/text-generation/generation" in QwenClient methods
   - This uses the correct Alibaba Cloud DashScope API endpoint for text generation

These changes align with the correct Alibaba Cloud DashScope API documentation for Qwen models, using the proper base URL and endpoint path for the text generation service.

## Outcome

The Qwen API should now use the correct endpoint configuration, allowing successful communication with the Alibaba Cloud API service.

## Evaluation

The fix addresses the configuration issue by updating to use the correct API endpoint structure for Alibaba Cloud's DashScope service.