#!/bin/bash

# Build the optimized frontend Docker image
echo "Building optimized todo-frontend image..."

# Build with multi-stage build and proper tagging
docker build -t todo-frontend:optimized -f Dockerfile .

echo "Build completed. Check the image size with: docker images | grep todo-frontend"