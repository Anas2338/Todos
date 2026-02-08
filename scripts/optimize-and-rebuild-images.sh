#!/bin/bash

# Script to optimize and rebuild all Docker images for the Todo + Chatbot application

set -e  # Exit on any error

echo "Optimizing and rebuilding Docker images for Todo + Chatbot application..."
echo

# Function to build an image with size optimization
build_image() {
    local service_name=$1
    local context_path=$2
    local dockerfile_path=$3

    echo "Building $service_name image..."

    # Build with size optimization flags
    docker build \
        --compress \
        --no-cache \
        --rm \
        -t "todo-$service_name:latest" \
        -f "$context_path/$dockerfile_path" \
        "$context_path"

    echo "✓ $service_name image built successfully"
    echo
}

# Build all services
build_image "frontend" "fullstack-todo/frontend" "Dockerfile"
build_image "backend" "fullstack-todo/backend" "Dockerfile"
build_image "chatbot" "fullstack-todo/chatbot_backend" "Dockerfile"

# Show final image sizes
echo "Final image sizes:"
echo "=================="
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep todo

echo
echo "Optimization completed! All images are now built with size optimizations:"
echo "- Multi-stage builds exclude build dependencies from final images"
echo "- Minimal base images (alpine) for smaller footprint"
echo "- Non-root users for security"
echo "- Proper .dockerignore files to exclude unnecessary files"
echo "- Production-only dependencies"
echo "- Cleanup of package manager caches"