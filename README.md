# Voyage-Analytics-Integrating-MLOps-in-Travel

This repository contains the machine learning models for:
- **Flight Price Prediction** (Regression)
- **Gender Classification** (Classification)

## 🚀 Quick Start Guide

**New to this project?** → Start here based on your use case:

| Level | Purpose | Time | Link |
|-------|---------|------|------|
| **Level 1** | Local Development | 10 min | [Local Setup](DEPLOYMENT_GUIDE.md#level-1-local-development-basic) |
| **Level 2** | Docker Compose | 15 min | [Docker Compose](DEPLOYMENT_GUIDE.md#level-2-docker-compose-intermediate) |
| **Level 3** | Kubernetes (Advanced) | 20 min | [Kubernetes with Kind](DEPLOYMENT_GUIDE.md#level-3-kubernetes-with-kind-advanced) |

**For complete instructions**, see **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

---

## 📋 Project Overview

This repository contains the machine learning models for:

Flight Price Prediction (Regression)
Gender Classification (Classification)

Follow the steps below to set up the project locally.

⚙️ Step 1: Clone the Repository

git clone
cd Voyage-Analytics

🧪 Step 2: Create Virtual Environment
Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

📦 Step 3: Install Dependencies

pip install -r requirements.txt

▶️ Step 4: Run the Models
Run Regression Model:

python regression_model.py

Run Gender Classification Model:

python gender_model.py

📁 Project Structure

project/
│
├── data/ → datasets (flights, hotels, users)
├── models/ → saved ML models & encoders
├── regression_model.py
├── gender_model.py
├── requirements.txt

⚠️ Important Instructions
Always activate the virtual environment before running code
Do not modify model input features without informing the team
Ensure datasets are placed correctly inside the data/ folder
Encoders are saved and must be used during prediction

## Docker Deployment (Flight Price Prediction API)

Build and run the FastAPI model service in a container for portable deployment.

Build:

```powershell
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
docker build -f .\ml-service\Dockerfile -t voyage-ml-service:latest .
```

Run:

```powershell
docker run --name voyage-ml-service -p 8000:8000 voyage-ml-service:latest
```

Health check URL:

http://127.0.0.1:8000/v1/health

## MLflow Tracking and Model Versioning

Use MLflow to track experiments, compare model iterations, and register versioned models.

1) Install MLflow:

```powershell
pip install mlflow
```

2) Start MLflow UI (local file-based tracking):

```powershell
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
python -m mlflow ui --backend-store-uri .\mlruns --port 5000
```

3) One-command tracked training (recommended):

```powershell
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
.\scripts\train_with_mlflow.ps1 -StartUi
```

4) Train and log experiments (manual):

```powershell
$env:MLFLOW_TRACKING_URI="file:./mlruns"
$env:MLFLOW_EXPERIMENT_NAME="flight-price-prediction"
$env:MLFLOW_REGISTERED_MODEL_NAME="flight-price-model"
python .\regerssion_model_train.py
```

5) Open MLflow UI:

http://127.0.0.1:5000

6) Serve API using a versioned model from MLflow registry:

```powershell
docker run --name voyage-ml-service -p 8000:8000 ^
	-e MLFLOW_TRACKING_URI="http://host.docker.internal:5000" ^
	-e MODEL_URI="models:/flight-price-model/Production" ^
	voyage-ml-service:latest
```

### MLflow launcher script options

Two launcher scripts available:
- [scripts/train_with_mlflow.ps1](scripts/train_with_mlflow.ps1) — for flight price prediction model
- [scripts/train_gender_with_mlflow.ps1](scripts/train_gender_with_mlflow.ps1) — for gender classification model

Flight price prediction examples:

```powershell
# Use defaults (file tracking URI, experiment name, model name)
.\scripts\train_with_mlflow.ps1

# Start MLflow UI and run training
.\scripts\train_with_mlflow.ps1 -StartUi

# Custom experiment/model name
.\scripts\train_with_mlflow.ps1 `
  -ExperimentName "flight-price-exp-v2" `
  -RegisteredModelName "flight-price-model-v2"
```

Gender classification examples:

```powershell
# Use defaults
.\scripts\train_gender_with_mlflow.ps1

# Start MLflow UI and run training
.\scripts\train_gender_with_mlflow.ps1 -StartUi

# Custom settings
.\scripts\train_gender_with_mlflow.ps1 `
  -ExperimentName "gender-exp-v2" `
  -RegisteredModelName "gender-model-v2"
```

## Gender Classification Model with MLflow Tracking

Same MLflow workflow for gender classification model—track experiments, version, and deploy.

1) One-command gender model training (recommended):

```powershell
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
.\scripts\train_gender_with_mlflow.ps1 -StartUi
```

2) Train manually with custom settings:

```powershell
$env:MLFLOW_TRACKING_URI="file:./mlruns"
$env:MLFLOW_EXPERIMENT_NAME="gender-classification-v2"
$env:MLFLOW_REGISTERED_MODEL_NAME="gender-classification-model-v2"
python .\gender_classification_model.py
```

3) Serve API with versioned gender model:

```powershell
docker run --name voyage-ml-service -p 8000:8000 ^
	-e MLFLOW_TRACKING_URI="http://host.docker.internal:5000" ^
	-e GENDER_MODEL_URI="models:/gender-classification-model/Production" ^
	voyage-ml-service:latest
```

4) Serve both models from MLflow registry:

```powershell
docker run --name voyage-ml-service -p 8000:8000 ^
	-e MLFLOW_TRACKING_URI="http://host.docker.internal:5000" ^
	-e MODEL_URI="models:/flight-price-model/Production" ^
	-e GENDER_MODEL_URI="models:/gender-classification-model/Production" ^
	voyage-ml-service:latest
```

## Docker Compose for Local Development

Run the entire stack locally with docker-compose (includes MLflow server, ML service, and nginx):

```powershell
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
docker-compose up -d
```

Access:

- ML Service API: http://127.0.0.1:8000/docs
- MLflow UI: http://127.0.0.1/mlflow
- Health check: http://127.0.0.1/health

Stop services:

```powershell
docker-compose down
```

## Kubernetes Deployment for Scalability

Deploy to Kubernetes clusters (EKS, GKE, AKS, minikube, etc.) for automatic scaling and high availability.

### Prerequisites

- Kubernetes cluster 1.20+
- kubectl configured
- Docker image pushed to registry

### Quick Deploy

```bash
# Build and push Docker image
docker build -f ml-service/Dockerfile -t your-registry/voyage-ml-service:latest .
docker push your-registry/voyage-ml-service:latest

# Deploy to cluster
kubectl apply -k kubernetes/
```

### Features

The Kubernetes deployment includes:

- **Deployment** with rolling updates (min 2, auto-scales to 10 replicas)
- **HorizontalPodAutoscaler** (scales on CPU 70%, memory 80%)
- **Service** with LoadBalancer (external access)
- **Ingress** with TLS support
- **ConfigMap** for environment variables and MLflow configuration
- **PodDisruptionBudget** for high availability (minimum 1 pod running)
- **NetworkPolicy** for security
- **ServiceAccount** with RBAC
- **Health checks** (liveness, readiness probes)

### Configuration

Edit `kubernetes/02-configmap.yaml` to set MLflow URI and model versions:

```yaml
data:
  MLFLOW_TRACKING_URI: "http://mlflow-server:5000"
  MODEL_URI: "models:/flight-price-model/Production"
  GENDER_MODEL_URI: "models:/gender-classification-model/Production"
```

Update and restart:

```bash
kubectl apply -f kubernetes/02-configmap.yaml
kubectl rollout restart deployment/voyage-ml-service -n voyage-ml
```

### Monitor Scaling

```bash
kubectl get hpa -n voyage-ml --watch
kubectl top pods -n voyage-ml
```

### Full Documentation

See [kubernetes/README.md](kubernetes/README.md) for comprehensive deployment guide including:

- Troubleshooting
- Security best practices
- Production recommendations
- MLflow integration
- Advanced configuration

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Kubernetes Cluster                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Ingress (TLS, Rate Limiting)                 │  │
│  └───────────────┬─────────────────────────────────────┘  │
│                  │                                         │
│  ┌───────────────▼─────────────────────────────────────┐  │
│  │    Service (LoadBalancer)                            │  │
│  └───────────────┬─────────────────────────────────────┘  │
│                  │                                         │
│  ┌───────────────▼─────────────────────────────────────┐  │
│  │  HorizontalPodAutoscaler (2-10 replicas)            │  │
│  │  - CPU utilization > 70%                             │  │
│  │  - Memory utilization > 80%                          │  │
│  └───────────────┬─────────────────────────────────────┘  │
│                  │                                         │
│  ┌───────────────▼─────────────────────────────────────┐  │
│  │    Deployment (Rolling Updates)                      │  │
│  │  ┌─────────────┬──────────────┬──────────────────┐  │  │
│  │  │  Pod 1      │   Pod 2      │   Pod N          │  │  │
│  │  │ ┌─────────┐ │ ┌─────────┐ │ ┌─────────────┐  │  │  │
│  │  │ │ML Service│ │ │ML Service│ │ │ML Service   │  │  │  │
│  │  │ │ Container│ │ │Container │ │ │Container    │  │  │  │
│  │  │ └─────────┘ │ └─────────┘ │ └─────────────┘  │  │  │
│  │  └─────────────┴──────────────┴──────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ConfigMap (MLflow URI, Model Versions)           │  │
│  │  NetworkPolicy (Security)                         │  │
│  │  PodDisruptionBudget (Min 1 pod available)        │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
         │
         │ (connects to)
         │
    ┌────▼──────────────┐
    │  MLflow Server    │
    │  (Tracking & UI)  │
    └───────────────────┘
```
