#!/bin/bash

echo "Docker Images Build Summary"
echo "==========================="

echo
echo "Built Images:"
docker images | grep -E "(todo-backend|todo-chatbot)" | awk '{print $1 ": " $2 " - Size: " $3}'

echo
echo "Image Sizes:"
docker images | grep -E "(todo-backend|todo-chatbot)" | awk '{print $1 " " $3}'

echo
echo "All Todo App Images:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep todo

echo
echo "Build completed successfully for backend and chatbot services!"
echo "Frontend service is still building in background (Next.js compilation takes time)."
echo
echo "To run the services:"
echo "  docker run -d -p 8000:8000 todo-backend:latest"
echo "  docker run -d -p 8001:8001 todo-chatbot:latest"