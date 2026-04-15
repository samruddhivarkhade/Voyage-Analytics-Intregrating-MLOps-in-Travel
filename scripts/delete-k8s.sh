#!/bin/bash
set -e

echo "🗑️  Cleaning up Voyage ML Service from Kubernetes"
echo "================================================="

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed."
    exit 1
fi

# Check cluster connection
kubectl cluster-info > /dev/null || {
    echo "❌ Cannot connect to Kubernetes cluster."
    exit 1
}

# Delete resources
echo "Deleting Voyage ML Service namespace and resources..."
kubectl delete namespace voyage-ml --ignore-not-found=true

echo "✅ Cleanup complete"
