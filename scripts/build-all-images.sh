#!/bin/bash

# Build script for all three services

set -e  # Exit on any error

echo "Building all Docker images for Todo + Chatbot application..."
echo

# Build frontend image
echo "1. Building frontend image..."
cd fullstack-todo/frontend
docker build -t todo-frontend:latest .
echo "✓ Frontend image built successfully"
echo

# Build backend image
echo "2. Building backend image..."
cd ../backend
docker build -t todo-backend:latest .
echo "✓ Backend image built successfully"
echo

# Build chatbot backend image
echo "3. Building chatbot backend image..."
cd ../chatbot_backend
docker build -t todo-chatbot:latest .
echo "✓ Chatbot backend image built successfully"
echo

# Show built images
echo "4. Built images:"
docker images | grep -E "(todo-frontend|todo-backend|todo-chatbot)"
echo

echo "All images built successfully!"
echo "You can now run: docker run -d -p 3000:3000 todo-frontend:latest"
echo "                  docker run -d -p 8000:8000 todo-backend:latest"
echo "                  docker run -d -p 8001:8001 todo-chatbot:latest"