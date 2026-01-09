---
id: "009"
title: "Fix Sign-in Redirect Loop Issue"
stage: "general"
date_iso: "2026-01-08"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "1-jwt-todo"
user: "user"
command: "fix-signin-redirect-loop"
labels: ["bug-fix", "authentication", "cookies", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\giaic\Agentic-AI\Todos\fullstack-todo\frontend\src\lib\auth\client.ts
  - E:\giaic\Agentic-AI\Todos\fullstack-todo\frontend\src\hooks\use-auth.ts
tests_yaml: |
  - Verify user stays on dashboard after sign-in
  - Verify session is established before redirect
prompt_text: |
  now when i sign in it return to signin page again and when i mnually write http://localhost:3000/ in browser it goto dashboard with signedin
response_text: |
  Fixed the sign-in redirect loop by updating cookie attributes from SameSite=Strict to SameSite=Lax and enhancing session validation. Modified the auth client to use consistent cookie attributes and updated the useAuth hook to verify session establishment before redirecting to dashboard. This ensures the session is properly established before navigation occurs.
outcome: "Successfully resolved the sign-in redirect loop issue."
evaluation: "Verified that session is properly established before redirecting after login."
---

# Fix Sign-in Redirect Loop Issue

## Problem
After signing in, users were being redirected back to the login page instead of staying on the dashboard. However, manually navigating to http://localhost:3000/ would show the user as signed in on the dashboard.

## Root Cause
The redirect to dashboard was happening too quickly after login, before the session was fully established. The session validation was failing when the dashboard loaded, causing a redirect back to login.

## Solution
1. Updated cookie attributes from SameSite=Strict to SameSite=Lax to allow cookies with navigation requests
2. Enhanced session validation in useAuth hook to verify session establishment before redirecting
3. Added delays to ensure cookies are properly set before redirecting
4. Modified both login and register functions to check session validity before redirecting

## Files Modified
- frontend/src/lib/auth/client.ts - Updated cookie attributes to SameSite=Lax
- frontend/src/hooks/use-auth.ts - Enhanced session validation before redirecting

## Result
Users now stay on the dashboard after successful sign-in as the session is properly established before navigation.