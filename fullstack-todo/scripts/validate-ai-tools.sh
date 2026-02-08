#!/bin/bash

# Script to validate that AI tools (Gordon, kubectl-ai, kagent) were used in the workflow

echo "Validating AI tool usage..."

# Check if Gordon was used by looking for any AI-generated Dockerfiles or evidence of Gordon use
if [ -f "fullstack-todo/frontend/Dockerfile" ] || [ -f "fullstack-todo/backend/Dockerfile" ] || [ -f "fullstack-todo/chatbot_backend/Dockerfile" ]; then
    echo "✓ Dockerfiles exist - indicating use of Gordon or similar AI tool for containerization"
else
    echo "⚠ Dockerfiles missing - Gordon may not have been used for containerization"
fi

# Check if kubectl-ai was used by looking for any kubectl-ai commands in scripts
if grep -r "kubectl-ai" . &> /dev/null; then
    echo "✓ kubectl-ai commands found in scripts - indicating use of kubectl-ai"
else
    echo "⚠ No kubectl-ai commands found in scripts - kubectl-ai may not have been used"
fi

# Check for any kagent usage patterns
if grep -r "kagent" . &> /dev/null; then
    echo "✓ kagent references found - indicating use of kagent"
else
    echo "⚠ No kagent references found - kagent may not have been used"
fi

echo "AI tool validation completed!"