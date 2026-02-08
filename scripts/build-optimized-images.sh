#!/bin/bash

# Script to build all optimized Docker images for the Todo + Chatbot application

set -e  # Exit on any error

echo "🚀 Building optimized Docker images for Todo + Chatbot application..."
echo

# Function to build an image with size optimization
build_image() {
    local service_name=$1
    local context_path=$2
    local dockerfile_path=$3
    local tag=$4

    echo "📦 Building $service_name image (tag: $tag)..."

    # Build with optimization flags
    docker build \
        --compress \
        --no-cache \
        --rm \
        --file "$context_path/$dockerfile_path" \
        -t "todo-$service_name:$tag" \
        "$context_path"

    echo "✅ $service_name image built successfully"
    echo
}

# Build all services with v1 tag
build_image "frontend" "fullstack-todo/frontend" "Dockerfile" "v1"
build_image "backend" "fullstack-todo/backend" "Dockerfile" "v1"
build_image "chatbot" "fullstack-todo/chatbot_backend" "Dockerfile" "v1"

# Show final image sizes
echo "📊 Final image sizes:"
echo "=================="
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep todo

echo
echo "✨ Optimization highlights:"
echo "- Multi-stage builds exclude build dependencies from final images"
echo "- Minimal base images (alpine) for smaller footprint"
echo "- Non-root users for security"
echo "- Proper .dockerignore files exclude unnecessary files"
echo "- Production-only dependencies"
echo "- Cleanup of package manager caches"
echo "- Optimized layer caching with bind mounts for uv"
echo
echo "🎉 All images built with size and security optimizations!"