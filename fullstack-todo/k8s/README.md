# Kubernetes Deployment for Todo + Chatbot Application

This directory contains all Kubernetes manifests and Helm charts for deploying the Todo + Chatbot application on a local Minikube cluster.

## Directory Structure

```
k8s/
├── charts/                 # Helm charts
│   └── todo-app/         # Main application Helm chart
│       ├── Chart.yaml    # Chart definition
│       ├── values.yaml   # Default configuration values
│       └── templates/    # Kubernetes resource templates
│           ├── _helpers.tpl          # Helper templates
│           ├── frontend-deployment.yaml
│           ├── backend-deployment.yaml
│           ├── chatbot-deployment.yaml
│           ├── db-deployment.yaml
│           ├── frontend-service.yaml
│           ├── backend-service.yaml
│           ├── chatbot-service.yaml
│           ├── db-service.yaml
│           ├── app-configmap.yaml
│           ├── db-configmap.yaml
│           ├── db-secret.yaml
│           └── rbac.yaml
└── manifests/            # Raw Kubernetes manifests (alternative to Helm)
    ├── namespace.yaml
    ├── db-pvc.yaml
    └── ingress.yaml
```

## Deployment Options

### Option 1: Using Helm (Recommended)
```bash
# Install the application
helm install todo-app ./charts/todo-app --namespace todo-app-ns --create-namespace

# Upgrade the application
helm upgrade todo-app ./charts/todo-app --namespace todo-app-ns

# Uninstall the application
helm uninstall todo-app --namespace todo-app-ns
```

### Option 2: Using Raw Manifests
```bash
# Apply all manifests
kubectl apply -f manifests/ --recursive

# Or apply individual manifests
kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/db-pvc.yaml
# ... etc
```

## Configuration

The Helm chart can be customized using the `values.yaml` file or by providing custom values during installation:

```bash
helm install todo-app ./charts/todo-app --namespace todo-app-ns --create-namespace \
  --set frontend.image.tag=v1.0.0 \
  --set backend.replicaCount=2
```

## Services

- **Frontend**: Exposed as NodePort for external access
- **Backend**: Exposed as ClusterIP for internal access
- **Chatbot**: Exposed as ClusterIP for internal access
- **Database**: Exposed as ClusterIP with persistent storage

## Service Communication

Services communicate using Kubernetes DNS service discovery:
- Frontend → Backend: `http://todo-app-backend-service:8000`
- Frontend → Chatbot: `http://todo-app-chatbot-service:8001`
- Backend/Chatbot → Database: `postgresql://todo-app-db-service:5432/todoapp`

## Security

- Service accounts and RBAC configuration provided
- Secrets for sensitive data (database credentials)
- Production-ready container images with non-root users
- Resource limits and requests configured
- Security contexts applied at both pod and container levels
- Health checks and monitoring configured

## Production Optimizations

- Multi-stage builds for all container images
- Alpine base images for minimal attack surface
- Proper signal handling with dumb-init
- Layer caching optimized for fast rebuilds
- Security best practices applied throughout
- Health monitoring and readiness probes configured