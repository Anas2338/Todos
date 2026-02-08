# Quickstart: Kubernetes Deployment for Todo + Chatbot

## Prerequisites

- Docker Desktop installed and running
- Minikube installed and configured
- kubectl installed and pointing to Minikube cluster
- Helm 3.x installed
- (Optional) AI-assisted DevOps tools: Gordon, kubectl-ai, kagent

## Setup Steps

### 1. Start Minikube Cluster
```bash
minikube start
```

### 2. Build Docker Images
Use Gordon (Docker AI Agent) to generate and build Docker images for each service:

```bash
# Navigate to each service directory and generate Dockerfile using Gordon
cd fullstack-todo/frontend
# Use Gordon to generate Dockerfile
docker build -t todo-frontend:latest .

cd ../backend
# Use Gordon to generate Dockerfile
docker build -t todo-backend:latest .

cd ../chatbot_backend
# Use Gordon to generate Dockerfile
docker build -t todo-chatbot:latest .
```

### 3. Load Images into Minikube
```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
minikube image load todo-chatbot:latest
```

### 4. Install Helm Chart
```bash
cd fullstack-todo/k8s/charts/todo-app
helm install todo-app . --namespace todo-app-ns --create-namespace
```

### 5. Verify Installation
```bash
kubectl get pods -n todo-app-ns
kubectl get services -n todo-app-ns
```

### 6. Access the Application
```bash
# Get the frontend service URL
minikube service todo-app-frontend-service --namespace todo-app-ns --url
```

## AI-Assisted Operations

### Using kubectl-ai for Commands
```bash
# Get pod status
kubectl-ai "show me the status of all pods in the default namespace"

# Scale a deployment
kubectl-ai "scale the frontend deployment to 2 replicas"
```

### Using kagent for Diagnostics
```bash
# Check cluster health
kagent analyze cluster

# Resource optimization suggestions
kagent suggest optimizations
```

## Validation

### Run Final Validation Script
```bash
./fullstack-todo/scripts/final-validation.sh
```

### Test Helm Reproducibility
```bash
./fullstack-todo/scripts/test-helm-reproducibility.sh
```

## Troubleshooting

### Common Issues:
1. **Images not found**: Ensure images are loaded into Minikube with `minikube image load`
2. **Service not accessible**: Check that NodePort services are properly configured
3. **Database connection errors**: Verify database service is running and credentials are correct

### Diagnostic Commands:
```bash
# Check pod logs
kubectl logs deployment/todo-app-frontend -n todo-app-ns
kubectl logs deployment/todo-app-backend -n todo-app-ns
kubectl logs deployment/todo-app-chatbot -n todo-app-ns

# Check service connectivity
kubectl exec -it <pod-name> --namespace todo-app-ns -- nslookup todo-app-backend-service
```

## Next Steps

- Configure ingress for advanced routing (if needed)
- Set up monitoring and logging stack
- Configure horizontal pod autoscaling
- Implement CI/CD pipeline