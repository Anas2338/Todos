#!/bin/bash

echo "Docker Image Size Optimization Report"
echo "====================================="

echo
echo "Backend Dockerfile (fullstack-todo/backend/Dockerfile):"
echo "------------------------------------------------------"
wc -l fullstack-todo/backend/Dockerfile
echo

echo "Chatbot Backend Dockerfile (fullstack-todo/chatbot_backend/Dockerfile):"
echo "--------------------------------------------------------------------"
wc -l fullstack-todo/chatbot_backend/Dockerfile
echo

echo "Frontend Dockerfile (fullstack-todo/frontend/Dockerfile):"
echo "-------------------------------------------------------"
wc -l fullstack-todo/frontend/Dockerfile
echo

echo "Size optimization improvements made:"
echo "1. Removed unnecessary runtime dependencies (curl, dumb-init) from production stages where possible"
echo "2. Used explicit group creation to ensure proper ownership"
echo "3. Used --no-cache flag for all apk installations"
echo "4. Optimized health checks to use Python instead of curl where possible"
echo "5. Maintained uv for fast dependency installation while keeping image small"
echo "6. Used Alpine base images for minimal footprint"
echo "7. Multi-stage builds to exclude build dependencies from final image"