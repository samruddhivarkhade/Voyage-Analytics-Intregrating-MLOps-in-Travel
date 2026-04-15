#!/bin/bash
set -e

echo "🚀 Deploying Voyage ML Service to Kubernetes"
echo "============================================"

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check cluster connection
echo "Checking Kubernetes cluster connection..."
kubectl cluster-info > /dev/null || {
    echo "❌ Cannot connect to Kubernetes cluster. Please configure kubectl."
    exit 1
}

# Check if kustomize is available
KUSTOMIZE_CMD="kubectl kustomize"
if command -v kustomize &> /dev/null; then
    KUSTOMIZE_CMD="kustomize"
fi

echo "Using kustomize: $KUSTOMIZE_CMD"

# Deploy resources
echo "Deploying Voyage ML Service resources..."
$KUSTOMIZE_CMD build ./kubernetes | kubectl apply -f -

echo "✅ Deployment initiated"
echo ""
echo "Watch deployment status:"
echo "  kubectl get pods -n voyage-ml --watch"
echo ""
echo "Get service endpoint:"
echo "  kubectl get svc voyage-ml-service -n voyage-ml"
echo ""
echo "View logs:"
echo "  kubectl logs -f -n voyage-ml -l app=voyage-ml-service"
