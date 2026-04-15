# Voyage Analytics ML Service - Complete Deployment Guide

This guide covers running the Voyage Analytics project from **basic local setup** to **production Kubernetes deployment**.

---

## Table of Contents

1. [Level 1: Local Development (Basic)](#level-1-local-development-basic)
2. [Level 2: Docker Compose (Intermediate)](#level-2-docker-compose-intermediate)
3. [Level 3: Kubernetes with Kind (Advanced)](#level-3-kubernetes-with-kind-advanced)
4. [MLflow Model Tracking](#mlflow-model-tracking)
5. [Testing & Validation](#testing--validation)
6. [Troubleshooting](#troubleshooting)

---

## Level 1: Local Development (Basic)

### 1.1 Prerequisites

- Python 3.11+
- Git
- pip/virtualenv

### 1.2 Setup

```powershell
# Navigate to project
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install -r ml-service/requirements.txt
```

### 1.3 Run ML Training (Basic)

```powershell
# Train flight price model (no MLflow)
python regerssion_model_train.py

# Train gender classification model (no MLflow)
python components/gender_classification_model.py

# Run tests
python -m pytest test_regression_model.py
python -m pytest test_classfication_Model.py
```

**Output:**
- Models saved to `models/` directory
- Reports saved to `reports/` directory
- Can verify accuracy/performance metrics

### 1.4 Run ML Service Locally

```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Start ML service (FastAPI)
cd ml-service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Access Service:**
- API Docs: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/v1/health
- Predict Flight Price: POST http://127.0.0.1:8000/v1/predict
- Predict Gender: POST http://127.0.0.1:8000/v1/predict-gender

### 1.5 Test API Locally

```powershell
# Health check
curl http://127.0.0.1:8000/v1/health

# Flight price prediction
curl -X POST http://127.0.0.1:8000/v1/predict `
  -H "Content-Type: application/json" `
  -d '{
    "flightType": "economic",
    "agency": "Rainbow",
    "gender": "male",
    "distance": 200,
    "time": 120,
    "age": 30
  }'

# Gender prediction
curl -X POST http://127.0.0.1:8000/v1/predict-gender `
  -H "Content-Type: application/json" `
  -d '{"age": 30, "distance": 200, "time": 120, "flightType": "economic"}'
```

---

## Level 2: Docker Compose (Intermediate)

### 2.1 Prerequisites

- Docker Desktop (with Docker Engine & Docker Compose v2)
- Port availability: 80, 5000, 8000, 443

### 2.2 Quick Start with Docker Compose

```powershell
# Navigate to project root
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel

# Start all services (MLflow server + ML service + nginx)
docker-compose up -d

# View running services
docker-compose ps
```

**Services Started:**
- **mlflow-server**: http://127.0.0.1:5000 (Model tracking)
- **ml-service**: http://127.0.0.1:8000 (API endpoint)
- **nginx**: http://127.0.0.1:80 (Load balancer)

### 2.3 View Logs

```powershell
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f ml-service
docker-compose logs -f mlflow-server
docker-compose logs -f nginx
```

### 2.4 Access UIs

- **ML Service Docs**: http://127.0.0.1:80/docs
- **MLflow UI**: http://127.0.0.1:5000
- **API Health**: http://127.0.0.1:80/v1/health

### 2.5 Stop Services

```powershell
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Level 3: Kubernetes with Kind (Advanced)

### 3.1 Prerequisites

- Docker Desktop (WSL2 enabled)
- kubectl configured
- Kind installed (automatically installed in setup)
- ~5 min for cluster initialization

### 3.2 Create Kubernetes Cluster

```powershell
# Install Kind (one-time)
$kindPath = "$env:USERPROFILE\AppData\Local\kind"
if (-not (Test-Path $kindPath)) { New-Item -ItemType Directory -Path $kindPath | Out-Null }
curl.exe -Lo "$kindPath\kind.exe" https://kind.sigs.k8s.io/dl/v0.20.0/kind-windows-amd64
$env:PATH += ";$kindPath"

# Verify Kind installation
& "$kindPath\kind.exe" --version

# Create cluster (uses kind-cluster-config.yaml)
& "$kindPath\kind.exe" create cluster --config kind-cluster-config.yaml --wait 10m
```

**Status:**
```powershell
kubectl cluster-info --context kind-voyage-ml-cluster
kubectl get nodes --context kind-voyage-ml-cluster
```

### 3.3 Build and Load Docker Image

```powershell
# Build Docker image
docker build -f ./ml-service/Dockerfile -t voyage-ml-service:latest .

# Load image into Kind cluster
& "$env:USERPROFILE\AppData\Local\kind\kind.exe" load docker-image voyage-ml-service:latest --name voyage-ml-cluster

# Verify image loaded
kubectl describe nodes --context kind-voyage-ml-cluster | grep -i "voyage-ml-service"
```

### 3.4 Deploy to Kubernetes

```powershell
# Apply all resources (kustomize)
kubectl apply -k kubernetes/ --context kind-voyage-ml-cluster

# Verify deployment
kubectl get all -n voyage-ml --context kind-voyage-ml-cluster
```

**Expected Output:**
```
deployment.apps/voyage-ml-service   2/2     Running
service/voyage-ml-service           LoadBalancer
horizontalpodautoscaler.autoscaling/voyage-ml-service-hpa
```

### 3.5 Access Service (Port-Forward)

```powershell
# Port-forward to local machine
kubectl port-forward -n voyage-ml svc/voyage-ml-service 8888:80 --context kind-voyage-ml-cluster
```

**Access Points:**
- API Docs: http://127.0.0.1:8888/docs
- Health Check: http://127.0.0.1:8888/v1/health
- Predictions: http://127.0.0.1:8888/v1/predict

### 3.6 Monitor Deployment

```powershell
# Watch pods
kubectl get pods -n voyage-ml -w --context kind-voyage-ml-cluster

# View logs
kubectl logs -n voyage-ml -l app=voyage-ml-service --context kind-voyage-ml-cluster

# Monitor auto-scaling (HPA)
kubectl get hpa -n voyage-ml -w --context kind-voyage-ml-cluster

# Describe deployment
kubectl describe deployment voyage-ml-service -n voyage-ml --context kind-voyage-ml-cluster
```

### 3.7 Scale Deployment

```powershell
# Manual scaling
kubectl scale deployment voyage-ml-service -n voyage-ml --replicas=5 --context kind-voyage-ml-cluster

# Check HPA thresholds (CPU 70%, Memory 80%)
kubectl describe hpa voyage-ml-service-hpa -n voyage-ml --context kind-voyage-ml-cluster
```

### 3.8 Update Deployment (Rolling Update)

```powershell
# Update image
kubectl set image deployment/voyage-ml-service ml-service=voyage-ml-service:latest -n voyage-ml --context kind-voyage-ml-cluster

# Check rollout status
kubectl rollout status deployment/voyage-ml-service -n voyage-ml --context kind-voyage-ml-cluster

# Rollback if needed
kubectl rollout undo deployment/voyage-ml-service -n voyage-ml --context kind-voyage-ml-cluster
```

### 3.9 Cleanup Kubernetes Cluster

```powershell
# Delete resources
kubectl delete -k kubernetes/ --context kind-voyage-ml-cluster

# Delete entire cluster
& "$env:USERPROFILE\AppData\Local\kind\kind.exe" delete cluster --name voyage-ml-cluster
```

---

## MLflow Model Tracking

### Prerequisites: Install MLflow

```powershell
pip install mlflow==2.22.0
```

### Training with MLflow (One-Command)

#### Flight Price Model

```powershell
# Navigate to repo root
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel

# Activate venv
.\.venv\Scripts\Activate.ps1

# Train with MLflow tracking and auto-launch UI
.\scripts\train_with_mlflow.ps1 -StartUi
```

**What happens:**
- Detects `.venv` auto-magically
- Trains all 4 models (LinearRegression, Ridge, RandomForest, GradientBoosting)
- Logs metrics, parameters, and models to MLflow
- Auto-registers best model to MLflow registry
- Launches MLflow UI on http://127.0.0.1:5000

#### Gender Classification Model

```powershell
# Train gender classifier with MLflow
.\scripts\train_gender_with_mlflow.ps1 -StartUi
```

### Access MLflow UI

```powershell
# If not auto-launched, start manually
python -m mlflow ui --host 127.0.0.1
```

**Features:**
- View experiments and runs
- Compare model metrics
- Track model versions
- Promote models to Production/Staging

---

## Testing & Validation

### 1. Unit Tests

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run all tests
pytest test_regression_model.py
pytest test_classfication_Model.py

# Run with verbose output
pytest test_regression_model.py -v

# Run specific test
pytest test_regression_model.py::test_model_training -v
```

### 2. Integration Tests (K8s)

```powershell
# Run integration tests on deployed service
cd ml-service/tests/integration

pytest test_routes.py -v --context kind-voyage-ml-cluster
```

### 3. API Endpoint Testing

```powershell
# Test flight price prediction
$body = @{
    flightType = "economic"
    agency = "Rainbow"
    gender = "male"
    distance = 200
    time = 120
    age = 30
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/v1/predict" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body `
  -UseBasicParsing

# Test gender prediction
$body = @{
    age = 30
    distance = 200
    time = 120
    flightType = "economic"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/v1/predict-gender" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body `
  -UseBasicParsing

# Health check (should return {"status": "healthy"})
Invoke-WebRequest -Uri "http://127.0.0.1:8000/v1/health" `
  -UseBasicParsing
```

### 4. Performance Testing (Load Test)

```powershell
# Install ab (Apache Bench) or use PowerShell
# Simple sequential test
for ($i = 1; $i -le 100; $i++) {
    Invoke-WebRequest -Uri "http://127.0.0.1:8000/v1/health" -UseBasicParsing | Out-Null
    Write-Host "Request $i completed"
}

# Monitor HPA during load
kubectl get hpa -n voyage-ml -w --context kind-voyage-ml-cluster
```

---

## Troubleshooting

### Issue: Docker Compose fails to start

**Error:** "additional properties 'deployment' not allowed"

**Solution:**
```powershell
# Update docker-compose.yaml to use correct syntax
# Remove 'deployment' key, use 'resources' directly
docker-compose config  # Validate YAML
docker-compose up -d
```

### Issue: Port already in use

**Solution:**
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or use different port
kubectl port-forward -n voyage-ml svc/voyage-ml-service 8888:80
```

### Issue: Kubernetes pods stuck in "Pending"

**Solution:**
```powershell
# Check pod events
kubectl describe pod <pod-name> -n voyage-ml --context kind-voyage-ml-cluster

# Check node resources
kubectl top nodes --context kind-voyage-ml-cluster

# Check persistent volumes
kubectl get pvc -n voyage-ml --context kind-voyage-ml-cluster
```

### Issue: MLflow URI not connected

**Solution:**
```powershell
# Ensure MLflow server is running
curl http://127.0.0.1:5000

# Check ConfigMap
kubectl get configmap ml-service-config -n voyage-ml -o yaml --context kind-voyage-ml-cluster

# Verify deployment env vars
kubectl describe deployment voyage-ml-service -n voyage-ml --context kind-voyage-ml-cluster | grep -i "MLFLOW"
```

### Issue: Models not loading

**Solution:**
```powershell
# Check LocalStatus ConfigMap
kubectl get configmap -n voyage-ml --context kind-voyage-ml-cluster

# Edit MODEL_URI if needed
kubectl edit configmap ml-service-config -n voyage-ml --context kind-voyage-ml-cluster

# Trigger rollout
kubectl rollout restart deployment voyage-ml-service -n voyage-ml --context kind-voyage-ml-cluster
```

---

## Quick Reference Commands

### Local Development
```powershell
# Setup
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Train models
python regerssion_model_train.py
python components/gender_classification_model.py

# Run service
cd ml-service && uvicorn app.main:app --reload
```

### Docker Compose
```powershell
# Start all
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

### Kubernetes
```powershell
# Create cluster
kind create cluster --config kind-cluster-config.yaml

# Deploy
kubectl apply -k kubernetes/ --context kind-voyage-ml-cluster

# Port-forward
kubectl port-forward -n voyage-ml svc/voyage-ml-service 8888:80

# Monitor
kubectl get all -n voyage-ml -w --context kind-voyage-ml-cluster

# Cleanup
kind delete cluster --name voyage-ml-cluster
```

### MLflow
```powershell
# Train with tracking
.\scripts\train_with_mlflow.ps1 -StartUi

# View UI
python -m mlflow ui --host 127.0.0.1
```

---

## Architecture Comparison

### Level 1: Local Development
```
Local Machine
├── Python Interpreter
├── ML Models (local files)
├── FastAPI Service
└── SQLite Database (local)
```

### Level 2: Docker Compose
```
Docker Host
├── Container: MLflow Server (port 5000)
├── Container: ML Service (port 8000)
└── Container: nginx (port 80)
```

### Level 3: Kubernetes
```
Kind Cluster (Docker)
├── Namespace: voyage-ml
├── Deployment: voyage-ml-service (2+ replicas)
├── Service: LoadBalancer (port 80)
├── HPA: Auto-scale (2-10 replicas)
├── ConfigMap: Configuration
└── NetworkPolicy: Security
```

---

## Environment Variables

### Local Development
```
MLFLOW_TRACKING_URI=file:./mlruns
MODEL_URI=models:/flight-price-model/Production
GENDER_MODEL_URI=models:/gender-classification-model/Production
LOG_LEVEL=INFO
```

### Docker Compose
```
MLFLOW_TRACKING_URI=http://mlflow-server:5000
MODEL_URI=models:/flight-price-model/Production
GENDER_MODEL_URI=models:/gender-classification-model/Production
```

### Kubernetes
```yaml
# Set in kubernetes/02-configmap.yaml
MLFLOW_TRACKING_URI: "http://mlflow-server:5000"
MODEL_URI: "models:/flight-price-model/Production"
GENDER_MODEL_URI: "models:/gender-classification-model/Production"
LOG_LEVEL: "INFO"
```

---

## Next Steps

1. **Choose Your Level:**
   - Learning? Start with Level 1
   - Development? Use Level 2
   - Production-ready? Deploy Level 3

2. **Configure Models:**
   - Update `kubernetes/02-configmap.yaml` with MLflow model URIs
   - Or keep local models in `models/` directory

3. **Scale:** 
   - Kubernetes HPA auto-scales based on CPU/Memory
   - Manual scaling: `kubectl scale deployment ...`

4. **Monitor:**
   - Check logs: `kubectl logs -f`
   - View metrics: `kubectl top pods`
   - Track models: MLflow UI

5. **Backup:**
   - Export MLflow runs: `mlflow runs list`
   - Backup database: Copy `mlruns/` directory
   - Version models: Push to container registry

---

## Support & Debugging

For more details, see:
- [kubernetes/README.md](kubernetes/README.md) - K8s specifics
- [README.md](README.md) - Project overview
- [ml-service/README.md](ml-service/README.md) - API documentation
