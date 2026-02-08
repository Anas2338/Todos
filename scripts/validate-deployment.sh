#!/bin/bash

# Script to validate services connectivity in the Kubernetes deployment

echo "Validating services connectivity..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "Minikube is not running. Please start minikube first."
    exit 1
fi

# Wait for all pods to be running
echo "Waiting for all pods to be running..."
kubectl wait --for=condition=Ready pods --all -n todo-app-ns --timeout=300s

# Check if all deployments are ready
echo "Checking deployment status..."
kubectl get deployments -n todo-app-ns

# Check if all services are available
echo "Checking service status..."
kubectl get services -n todo-app-ns

# Validate service-to-service connectivity
echo "Validating service connectivity..."
kubectl run connectivity-test --image=curlimages/curl -n todo-app-ns --rm -it --restart='Never' -- \
  curl -s -o /dev/null -w "%{http_code}" http://todo-frontend-service:3000 || echo "Frontend connectivity test failed"

kubectl run connectivity-test --image=curlimages/curl -n todo-app-ns --rm -it --restart='Never' -- \
  curl -s -o /dev/null -w "%{http_code}" http://todo-backend-service:8000/health || echo "Backend connectivity test failed"

kubectl run connectivity-test --image=curlimages/curl -n todo-app-ns --rm -it --restart='Never' -- \
  curl -s -o /dev/null -w "%{http_code}" http://todo-chatbot-service:8001/health || echo "Chatbot connectivity test failed"

echo "Deployment validation completed!"