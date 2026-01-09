---
id: "007"
title: "Fix React State Update Error"
stage: "general"
date_iso: "2026-01-08"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "1-jwt-todo"
user: "user"
command: "fix-react-state-update-error"
labels: ["bug-fix", "react", "navigation", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\giaic\Agentic-AI\Todos\fullstack-todo\frontend\src\app\dashboard\page.tsx
  - E:\giaic\Agentic-AI\Todos\fullstack-todo\frontend\src\app\tasks\new\page.tsx
  - E:\giaic\Agentic-AI\Todos\fullstack-todo\frontend\src\app\tasks\[id]\edit\page.tsx
  - E:\giaic\Agentic-AI\Todos\fullstack-todo\frontend\src\app\tasks\[id]\page.tsx
tests_yaml: |
  - Verify no "Cannot update a component" errors occur
  - Verify navigation works properly after registration
prompt_text: |
  in http://localhost:3000/register when i create new user browser console show this error ""Cannot update a component (`Router`) while rendering a different component (`DashboardPage`). To locate the bad setState() call inside `DashboardPage`, follow the stack trace as described in https://react.dev/link/setstate-in-render""
response_text: |
  Fixed the React state update error by updating all protected pages to handle navigation properly. The issue was calling router.push() directly during the render phase, which violates React's rules. Updated all pages to use useEffect hooks for navigation after the component has rendered, ensuring navigation only occurs after authentication state is fully loaded.
outcome: "Successfully resolved the React state update error by fixing navigation during render."
evaluation: "Verified that router.push() is no longer called during render phase in any protected pages."
---

# Fix React State Update Error

## Problem
The application was throwing a React error: "Cannot update a component (`Router`) while rendering a different component (`DashboardPage`)" when navigating after registration. This occurred because navigation methods were being called directly during the render phase.

## Root Cause
Multiple protected pages (Dashboard, New Task, Edit Task, Task Detail) were calling `router.push('/login')` directly during render when the user wasn't authenticated, violating React's rendering rules.

## Solution
Updated all protected pages to handle navigation properly:
- Used useEffect hooks to perform navigation after component has rendered
- Separated loading state checks from navigation actions
- Ensured navigation only occurs after authentication state is fully loaded

## Files Modified
- frontend/src/app/dashboard/page.tsx - Fixed navigation during render
- frontend/src/app/tasks/new/page.tsx - Fixed navigation during render
- frontend/src/app/tasks/[id]/edit/page.tsx - Fixed navigation during render
- frontend/src/app/tasks/[id]/page.tsx - Fixed navigation during render

## Result
The React state update error has been eliminated and navigation works properly after registration.