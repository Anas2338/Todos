---
name: helm-charts-packager
description: This skill helps package Kubernetes applications with Helm charts from hello world examples to professional production charts. It provides best practices for chart structure, templates, values, dependencies, and security.
---

# Helm Charts Packager

This skill should be used when users need to package Kubernetes applications with Helm charts from simple hello world examples to professional production charts.

## Overview

Helm is the package manager for Kubernetes that helps you manage Kubernetes applications. This skill provides guidance for creating production-ready Helm charts with proper structure, templates, values management, dependencies, and security practices.

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing Kubernetes manifests, application structure, existing Helm charts if any |
| **Conversation** | User's specific packaging requirements, target environments, security constraints |
| **Skill References** | Helm patterns from `references/` (charts, templates, dependencies, security) |
| **User Guidelines** | Team-specific conventions, naming standards, security policies |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Helm Chart Structure

A standard Helm chart follows this directory structure:

```
mychart/
  Chart.yaml          # Chart metadata
  values.yaml         # Default configuration values
  charts/             # Subcharts (dependencies)
  templates/          # Kubernetes manifest templates
  ...
```

### Chart.yaml Specification

Required fields:
- `apiVersion`: Chart API version (v2 for Helm 3+, v1 for older)
- `name`: Chart name
- `version`: Chart version (SemVer 2)

Optional fields:
- `kubeVersion`: Kubernetes version constraints
- `description`: Chart description
- `type`: Chart type (application/library)
- `keywords`: List of keywords
- `home`: Project homepage
- `sources`: Source code URLs
- `dependencies`: Chart dependencies
- `maintainers`: Maintainer information
- `icon`: Icon URL
- `appVersion`: Application version
- `deprecated`: Boolean indicating deprecation
- `annotations`: Custom metadata

## Basic Chart Creation

### Hello World Chart

Create a starter chart:
```bash
helm create mychart
```

This generates a basic chart structure with common templates.

### Minimal Chart.yaml

```yaml
apiVersion: v2
name: my-chart
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
```

### Basic values.yaml

```yaml
# Default values for the chart
replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: ""

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: ""
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific

resources: {}
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

nodeSelector: {}

tolerations: []

affinity: []
```

## Templates and Values

### Template Syntax

Helm templates use Go template language with Sprig functions:
- `{{ .Values.key.subkey }}` - Access values
- `{{ include "template.name" . }}` - Include named templates
- `{{ required "Error message" .Values.requiredValue }}` - Require values
- `{{ quote .Values.string }}` - Quote strings safely

### Named Templates

Define reusable templates in `templates/_helpers.tpl`:

```go-template
{{/*
Expand the name of the chart.
*/}}
{{- define "my-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "my-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "my-chart.labels" -}}
helm.sh/chart: {{ include "my-chart.chart" . }}
{{ include "my-chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "my-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## Dependencies

### Declaring Dependencies

In `Chart.yaml`:

```yaml
dependencies:
- name: nginx
  version: "1.2.3"
  repository: "https://example.com/charts"
- name: memcached
  version: "3.2.1"
  repository: "https://another.example.com/charts"
```

Or local dependencies:
```yaml
dependencies:
- name: nginx
  version: "1.2.3"
  repository: "file://../dependency_chart/nginx"
```

### Managing Dependencies

```bash
# Update dependencies
helm dependency update

# View dependency tree
helm dependency list
```

## Production Best Practices

### 1. Chart Testing

Create test templates in `templates/tests/test-connection.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include \"my-chart.fullname\" . }}-test-connection"
  labels:
    {{- include \"my-chart.labels\" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include \"my-chart.fullname\" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

Test the chart:
```bash
helm test <release-name>
```

### 2. Linting

Check chart for best practices:
```bash
helm lint
```

### 3. Template Evaluation

Render templates locally to verify:
```bash
helm template . --debug
```

### 4. Security

#### RBAC Configuration

Separate RBAC concerns in values:

```yaml
rbac:
  # Specifies whether RBAC resources should be created
  create: true

serviceAccount:
  # Specifies whether a ServiceAccount should be created
  create: true
  # The name of the ServiceAccount to use.
  # If not set and create is true, a name is generated using the fullname template
  name:
```

### 5. Chart Signing and Provenance

Package and sign charts:
```bash
helm package --sign --key 'John Smith' --keyring path/to/keyring.secret mychart
```

Verify charts:
```bash
helm verify mychart-0.1.0.tgz
helm install --verify mychart-0.1.0.tgz
```

## Advanced Template Techniques

### Conditional Logic

```go-template
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
...
{{- end }}
```

### Loops

```go-template
{{- range .Values.hosts }}
- host: {{ .name }}
  paths:
    - path: {{ .path }}
      pathType: ImplementationSpecific
{{- end }}
```

### Using tpl Function

For dynamic template evaluation:
```go-template
{{ tpl .Values.externalConfig . }}
```

## Chart Development Workflow

1. **Initialize Chart**
   ```bash
   helm create my-chart
   ```

2. **Customize Templates**
   - Modify `templates/` files
   - Update `values.yaml` defaults
   - Add helper templates in `_helpers.tpl`

3. **Test Locally**
   ```bash
   helm lint
   helm template . --debug
   ```

4. **Add Dependencies** (if needed)
   - Update `Chart.yaml` with dependencies
   - Run `helm dependency update`

5. **Package for Distribution**
   ```bash
   helm package .
   ```

6. **Sign for Security** (production)
   ```bash
   helm package --sign --key 'Maintainer Name' mychart
   ```

## Chart Types

### Application Charts
- Default chart type
- Deploys applications to Kubernetes
- Uses `type: application` in Chart.yaml

### Library Charts
- Reusable templates/components
- Not installable independently
- Uses `type: library` in Chart.yaml

## Security Considerations

- Use `required` function for mandatory values
- Validate input with conditionals
- Separate RBAC and ServiceAccount configuration
- Sign charts for integrity verification
- Follow least-privilege principles for RBAC
- Sanitize user-provided values