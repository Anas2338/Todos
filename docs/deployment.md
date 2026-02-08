# Kubernetes Deployment Guide for Todo + Chatbot Application

## Prerequisites

- Docker Desktop
- Minikube
- kubectl
- Helm 3.x
- (Optional) AI-assisted tools: Gordon, kubectl-ai, kagent

## Getting Started

### 1. Start Minikube Cluster

```bash
minikube start
```

### 2. Build Docker Images

Use Gordon or manually build Docker images for each service:

```bash
# Navigate to each service directory and build
cd fullstack-todo/frontend
docker build -t todo-frontend:latest .

cd ../backend
docker build -t todo-backend:latest .

cd ../chatbot_backend
docker build -t todo-chatbot:latest .
```

### 3. Load Images into Minikube

```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
minikube image load todo-chatbot:latest
```

### 4. Deploy with Helm

```bash
cd fullstack-todo/k8s/charts/todo-app
helm install todo-app . --namespace todo-app-ns --create-namespace
```

### 5. Access the Application

```bash
# Get the frontend service URL
minikube service todo-app-frontend-service --namespace todo-app-ns --url
```

## Architecture

The deployment consists of:

- **Frontend Service**: Node.js/React application (NodePort service)
- **Backend Service**: Python FastAPI application (ClusterIP service)
- **Chatbot Service**: Python chatbot backend (ClusterIP service)
- **Database Service**: PostgreSQL database with persistent storage (ClusterIP service)

## Service Communication

Services communicate using Kubernetes DNS service discovery:
- Frontend accesses backend via: `http://todo-app-backend-service:8000`
- Frontend accesses chatbot via: `http://todo-app-chatbot-service:8001`
- Backend and Chatbot access database via: `postgresql://todo-app-db-service:5432/todoapp`

## Configuration

Configuration is managed through:
- ConfigMaps for non-sensitive data
- Secrets for sensitive data (database passwords)
- Environment variables injected into containers