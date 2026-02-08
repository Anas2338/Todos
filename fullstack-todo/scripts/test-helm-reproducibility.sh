#!/bin/bash

# Script to test Helm chart reproducibility

NAMESPACE="todo-app-test"
CHART_PATH="./k8s/charts/todo-app"

echo "Testing Helm chart reproducibility..."

# Create test namespace
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Install the chart
echo "Installing Helm chart..."
helm install todo-test $CHART_PATH --namespace $NAMESPACE --wait --timeout=5m

if [ $? -ne 0 ]; then
    echo "❌ Helm install failed"
    exit 1
fi

echo "✅ Helm install succeeded"

# Check if all resources are ready
echo "Checking if all resources are ready..."
kubectl wait --for=condition=Ready pods --all -n $NAMESPACE --timeout=300s

if [ $? -eq 0 ]; then
    echo "✅ All pods are ready"
else
    echo "⚠️ Some pods may not be ready, continuing with test"
fi

# Uninstall the chart
echo "Uninstalling Helm chart..."
helm uninstall todo-test --namespace $NAMESPACE

if [ $? -ne 0 ]; then
    echo "❌ Helm uninstall failed"
    exit 1
fi

echo "✅ Helm uninstall succeeded"

# Install the chart again to test reproducibility
echo "Re-installing Helm chart to test reproducibility..."
helm install todo-test $CHART_PATH --namespace $NAMESPACE --wait --timeout=5m

if [ $? -ne 0 ]; then
    echo "❌ Second Helm install failed - chart is not reproducible"
    kubectl delete namespace $NAMESPACE
    exit 1
fi

echo "✅ Second Helm install succeeded - chart is reproducible"

# Clean up
helm uninstall todo-test --namespace $NAMESPACE
kubectl delete namespace $NAMESPACE

echo "✅ Helm reproducibility test completed successfully!"