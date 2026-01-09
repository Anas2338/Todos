---
id: "002"
title: "Fix Date Display Issue in Dashboard"
stage: "general"
date_iso: "2026-01-08"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "1-jwt-todo"
user: "user"
command: "fix-date-display-issue"
labels: ["bug-fix", "date-formatting", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\giaic\Agentic-AI\Todos\fullstack-todo\frontend\src\lib\api\tasks.ts
tests_yaml: |
  - Verify dashboard shows real dates instead of 'Date not available'
prompt_text: |
  in http://localhost:3000/dashboard in all tasks show ""created: Date not available"" and in completed tasks show ""completed: Date not available"" i want to show real date
response_text: |
  Fixed the date display issue by adding transformation functions to convert the API response from snake_case string dates to camelCase Date objects that match the frontend Task interface. The backend returns created_at and updated_at as strings in snake_case format, but the frontend expected createdAt and updatedAt as Date objects in camelCase format. Added transformTaskResponse and transformTaskResponseArray functions to handle the conversion and proper date parsing.
outcome: "Successfully fixed the date display issue and real dates are now shown on the dashboard."
evaluation: "Verified that the transformation functions properly convert API response to match the Task interface and dates are displayed correctly."
---

# Fix Date Display Issue in Dashboard

## Problem
The dashboard was showing "Date not available" instead of real dates for created and completed tasks. This happened because the API response format didn't match the frontend Task interface expectations.

## Root Cause
- Backend API returns dates as strings in snake_case format (`created_at`, `updated_at`)
- Frontend Task interface expects Date objects in camelCase format (`createdAt`, `updatedAt`)
- No transformation was happening between API response and frontend consumption

## Solution
Updated the task API client to include transformation functions that:
- Convert snake_case properties to camelCase
- Parse date strings into JavaScript Date objects
- Handle invalid dates gracefully with fallbacks

## Files Modified
- `frontend/src/lib/api/tasks.ts` - Added transformation functions and updated all API methods to use them

## Result
Dashboard now shows real dates instead of "Date not available" messages.