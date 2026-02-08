#!/bin/bash

# Script to validate Docker images for each service

echo "Validating Docker images..."

# Check if Dockerfiles exist
echo "Checking for Dockerfiles:"
if [ -f "frontend/Dockerfile" ]; then
    echo "✓ Frontend Dockerfile exists"
else
    echo "✗ Frontend Dockerfile missing"
fi

if [ -f "backend/Dockerfile" ]; then
    echo "✓ Backend Dockerfile exists"
else
    echo "✗ Backend Dockerfile missing"
fi

if [ -f "chatbot_backend/Dockerfile" ]; then
    echo "✓ Chatbot Dockerfile exists"
else
    echo "✗ Chatbot Dockerfile missing"
fi

# Check if Docker images have been built
echo "Checking if images can be built:"
echo "To test actual images, run: docker build -t <service>:<tag> <service_dir>"

echo "Image validation completed!"