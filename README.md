# 🛫 Voyage Analytics - MLOps in Travel

A complete production-ready machine learning system for travel analytics with **flight price prediction**, **gender classification**, and **hotel recommendations** using modern MLOps practices, containerization, and Kubernetes orchestration.

**Project Status:** ✅ Complete | **Last Updated:** April 19, 2026

---

## 📋 Quick Navigation

- **New here?** → Read [Quick Start](#-quick-start-choose-one) below
- **Frontend details** → See [frontend/README.md](frontend/README.md)
- **Backend API** → See [ml-service/README.md](ml-service/README.md)
- **Full project structure** → Scroll to [Project Structure](#-project-structure)

---

## ✨ Features at a Glance

✅ **3 ML Models** - Flight prices, gender classification, hotel recommendations  
✅ **FastAPI Backend** - 6+ RESTful endpoints with JWT authentication  
✅ **React Frontend** - Modern UI with TypeScript, Tailwind CSS, error boundaries  
✅ **Docker Ready** - Multi-stage builds, docker-compose orchestration  
✅ **Kubernetes Ready** - Auto-scaling (2-10 pods), HPA, PDB, network policies  
✅ **MLFlow Tracking** - Full experiment versioning and model registry  
✅ **Database** - SQLAlchemy ORM with SQLite, prediction tracking  
✅ **Error Handling** - Comprehensive boundaries, fallback pages, toast notifications  

---

## 🚀 Quick Start (Choose One)

### **1️⃣ Local Development** (Fastest - 2 minutes)

```powershell
# Terminal 1: Backend
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
.\.venv\Scripts\Activate.ps1
uvicorn ml-service.app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

**Access:** Frontend http://localhost:5173 | API http://localhost:8000 | Docs http://localhost:8000/docs

---

### **2️⃣ Docker Compose** (Production-like - 5 minutes)

```powershell
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
docker-compose build
docker-compose up -d
```

**Access:** Frontend http://localhost | API http://localhost/api/v1 | MLFlow http://localhost:5000

---

### **3️⃣ Kubernetes** (Advanced - 30 minutes)

```bash
# Create local cluster
kind create cluster --config kind-cluster-config.yaml

# Deploy
kubectl apply -k kubernetes/

# Access
kubectl port-forward -n voyage-ml svc/voyage-ml 8000:8000
```

**Access:** Frontend build + API on http://localhost:8000

---

## 📁 Project Structure

```
Voyage-Analytics-Intregrating-MLOps-in-Travel/
├── 📖 README.md                              ← You are here
├── frontend/                                  
│   ├── README.md                             ← Frontend docs
│   ├── src/
│   │   ├── pages/                            (Dashboard, Auth, Predictions, etc.)
│   │   ├── components/                       (ErrorBoundary, Header, Toast, etc.)
│   │   ├── services/apiClient.ts             (API communication)
│   │   ├── store/authStore.ts                (Auth state)
│   │   └── utils/errorHandler.ts             (Error utilities)
│   └── package.json, vite.config.ts, etc.
│
├── ml-service/                                
│   ├── README.md                             ← Backend docs
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py                           (FastAPI app)
│   │   ├── api/routes.py                     (All endpoints)
│   │   ├── services/hotel_recommendation.py  (ML service)
│   │   ├── schemas/input_schema.py           (Pydantic models)
│   │   └── core/                             (Config, Security, ORM)
│   └── requirements.txt
│
├── components/                                (ML training scripts)
│   ├── regerssion_model_train.py
│   ├── gender_classification_model.py
│   └── recommendation_model.ipynb
│
├── scripts/                                   (Training & deployment)
│   ├── train_with_mlflow.ps1
│   ├── train_gender_with_mlflow.ps1
│   ├── train_hotel_recommendation.ps1
│   ├── deploy-k8s.sh
│   └── delete-k8s.sh
│
├── kubernetes/                                (K8s manifests)
│   ├── 01-namespace.yaml
│   ├── 02-configmap.yaml
│   ├── 03-deployment.yaml
│   ├── 04-service.yaml
│   ├── 05-hpa.yaml                           ← Auto-scaling
│   ├── 06-serviceaccount.yaml
│   ├── 07-pdb.yaml
│   ├── 08-ingress.yaml
│   ├── 09-network-policy.yaml
│   └── kustomization.yaml
│
├── data/                                      (Datasets)
│   ├── flights.csv (50K+ records)
│   ├── hotels.csv
│   └── users.csv
│
├── models/                                    (Trained artifacts)
│   ├── final_model.pkl
│   ├── gender_model.pkl
│   └── hotel_recommendation/
│
├── mlruns/                                    (MLFlow experiments)
│   ├── 410661797205375458/                   (Flight experiments)
│   └── 243563443763366529/                   (Gender experiments)
│
├── docker-compose.yaml                       ← Multi-container setup
├── nginx.conf                                ← Reverse proxy
├── kind-cluster-config.yaml                  ← K8s config
└── requirements.txt
```

---

## 🤖 ML Models Summary

| Model | Type | Algorithm | Accuracy | Speed |
|-------|:----:|-----------|:--------:|:-----:|
| **Flight Prices** | Regression | GradientBoosting | R² > 0.85 | ~10ms |
| **Gender** | Classification | LogisticRegression | > 85% | ~5ms |
| **Hotel Recommendations** | Ranking | RandomForest (300 trees) | Top-5 ranked | ~50ms |

---

## 🔌 API Endpoints

**Base URL:** `http://localhost:8000/v1` (local) or `http://localhost/api/v1` (Docker)

### Authentication
```
POST   /login              Login user (returns JWT token)
POST   /register           Register new user
```

### Predictions
```
POST   /predict            Flight price prediction (requires JWT)
POST   /predict-gender     Gender classification (requires JWT)
POST   /recommend-hotels   Hotel recommendations (requires JWT)
GET    /stats              User prediction statistics (requires JWT)
```

### Health
```
GET    /health             Service health check
GET    /info               API information
```

**Interactive Docs:** http://localhost:8000/docs (Swagger) | http://localhost:8000/redoc (ReDoc)

---

## 🐳 Deployment Methods

| Method | Cost | Setup | Performance | Persistence | Best For |
|--------|:----:|:-----:|:-----------:|:----------:|----------|
| **Local** | Free | 2 min | ⚡⚡ | None | Development |
| **Docker Compose** | Free | 5 min | ⚡⚡ | Volume | Testing |
| **Kind K8s** | Free | 30 min | ⚡⚡⚡ | Limited | Production test |
| **Fly.io** | Free* | 10 min | ⚡⚡ | ✅ | Production |
| **Railway** | Free* | 10 min | ⚡⚡ | ✅ | Production |

*Free tier: 1,000 hours/month

---

## 🐛 Troubleshooting

### "Connection refused" on port 8000
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend not connecting to API
Check `frontend/src/services/apiClient.ts` - verify API URL matches backend

### Models not loading
```bash
cd ml-service/app/services
python -c "from hotel_recommendation import load_recommendation_model; load_recommendation_model()"
```

### Docker won't start
```powershell
docker system prune -a
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

---

## 📚 Full Documentation

| Document | Purpose |
|----------|---------|
| [frontend/README.md](frontend/README.md) | Frontend development, components, customization |
| [ml-service/README.md](ml-service/README.md) | Backend API, models, training, deployment |
| **This file** | Project overview, quick start, structure |

---

## ✅ Project Completion Status

✅ Regression Model - Flight price prediction  
✅ REST API - FastAPI with JWT auth  
✅ Containerization - Docker & docker-compose  
✅ Kubernetes - Auto-scaling, HPA, PDB  
✅ MLFlow - Model versioning & tracking  
✅ Gender Classification - Full pipeline  
✅ Hotel Recommendations - ML + UI  
✅ Error Handling - Boundaries, fallback pages, toasts  

**Total Features:** 7/7 ✅ Complete

---

## 🤝 Support & Contributing

**Issues?** Check troubleshooting above or review [ml-service/README.md](ml-service/README.md)  
**Questions?** See [frontend/README.md](frontend/README.md) for frontend issues  
**Contributing?** Follow the structure, add tests, document changes  

---

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│         End User (Browser)              │
└──────────────────┬──────────────────────┘
                   │ HTTPS
┌──────────────────▼──────────────────────┐
│      Nginx Reverse Proxy               │
│  (Docker/K8s Load Balancer)            │
└──┬──────────────────────────────────┬──┘
   │ /                                │ /api/v1
   │                                  │
┌──▼──────────────────┐   ┌──────────▼─────────┐
│ React Frontend      │   │  FastAPI Backend   │
│ (SPA, TypeScript)   │   │  (6 endpoints)     │
│ ├─ Dashboard        │   │  ├─ /predict      │
│ ├─ Auth flows       │   │  ├─ /predict-*   │
│ ├─ Predictions      │   │  ├─ /stats        │
│ └─ Error boundaries │   │  └─ /health       │
└────────────────────┘   │                    │
                         ├─ SQLAlchemy ORM   │
                         ├─ scikit-learn ML  │
                         ├─ Pydantic         │
                         └─ JWT Security     │
                                │
                    ┌───────────▼──────────┐
                    │   SQLite Database    │
                    │  ├─ Users            │
                    │  └─ Predictions      │
                    └────────────────────┘
```

---

**Version:** 1.0.0 | **Status:** Production Ready ✅ | **Last Updated:** April 19, 2026
