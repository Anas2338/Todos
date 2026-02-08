# Data Model: Kubernetes Resources for Todo + Chatbot Deployment

## Kubernetes Resource Definitions

### Namespace
- **name**: Name of the namespace for the deployment
- **labels**: Metadata labels for identification and grouping

### Deployments
#### Frontend Deployment
- **name**: Deployment name
- **replicas**: Number of pod replicas (1 for local)
- **image**: Docker image reference for frontend
- **ports**: Container port mapping
- **environment**: Environment variables (API endpoints, etc.)
- **resources**: CPU/memory requests and limits
- **healthChecks**: Liveness and readiness probe configurations

#### Backend Deployment
- **name**: Deployment name
- **replicas**: Number of pod replicas (1 for local)
- **image**: Docker image reference for backend
- **ports**: Container port mapping
- **environment**: Environment variables (database connection, etc.)
- **resources**: CPU/memory requests and limits
- **healthChecks**: Liveness and readiness probe configurations

#### Chatbot Backend Deployment
- **name**: Deployment name
- **replicas**: Number of pod replicas (1 for local)
- **image**: Docker image reference for chatbot backend
- **ports**: Container port mapping
- **environment**: Environment variables (database, API endpoints)
- **resources**: CPU/memory requests and limits
- **healthChecks**: Liveness and readiness probe configurations

#### Database Deployment
- **name**: Deployment name
- **replicas**: Number of pod replicas (1 for local)
- **image**: Database Docker image reference
- **ports**: Container port mapping
- **environment**: Database configuration variables
- **storage**: Persistent volume claim reference
- **resources**: CPU/memory requests and limits
- **healthChecks**: Liveness and readiness probe configurations

### Services
#### Frontend Service
- **name**: Service name
- **type**: Service type (NodePort for local access)
- **selector**: Label selector to connect to frontend pods
- **ports**: Port mappings (external and internal)

#### Backend Service
- **name**: Service name
- **type**: Service type (ClusterIP for internal access)
- **selector**: Label selector to connect to backend pods
- **ports**: Port mappings (external and internal)

#### Chatbot Service
- **name**: Service name
- **type**: Service type (ClusterIP for internal access)
- **selector**: Label selector to connect to chatbot pods
- **ports**: Port mappings (external and internal)

#### Database Service
- **name**: Service name
- **type**: Service type (ClusterIP for internal access)
- **selector**: Label selector to connect to database pods
- **ports**: Port mappings (external and internal)

### ConfigMaps
#### Application ConfigMap
- **name**: ConfigMap name
- **data**: Key-value pairs for application configuration
- **connectionStrings**: Database connection details
- **apiEndpoints**: Internal service endpoint addresses

#### Database ConfigMap
- **name**: ConfigMap name
- **data**: Database configuration parameters
- **initScripts**: Initialization scripts

### Secrets
#### Database Credentials Secret
- **name**: Secret name
- **data**: Encoded sensitive information
- **username**: Database username
- **password**: Database password

#### API Keys Secret
- **name**: Secret name
- **data**: Encoded API keys and tokens
- **keys**: Various API authentication tokens

### PersistentVolumeClaims
#### Database PVC
- **name**: PVC name
- **storageClassName**: Storage class identifier
- **accessModes**: Access modes (ReadWriteOnce)
- **resources**: Storage capacity request

### Ingress (optional for local)
#### Main Ingress
- **name**: Ingress name
- **rules**: Path-based routing rules
- **tls**: TLS certificate configuration

## Relationships

- **Frontend Deployment** → connects to → **Backend Service** (via environment variables)
- **Frontend Deployment** → connects to → **Chatbot Service** (via environment variables)
- **Chatbot Deployment** → connects to → **Database Service** (via environment variables)
- **Backend Deployment** → connects to → **Database Service** (via environment variables)
- **Deployments** → mount → **ConfigMaps** (as environment variables or volumes)
- **Deployments** → mount → **Secrets** (as environment variables or volumes)
- **Database Deployment** → uses → **PersistentVolumeClaim** (for data persistence)
- **Services** ← selects → **Deployments** (via label selectors)