# 🔧 Voyage Analytics - Backend API

FastAPI-based REST API server for machine learning models. Includes flight price prediction, gender classification, and hotel recommendations with full authentication, error handling, and MLFlow integration.

**Version:** 1.0.0 | **Status:** Production Ready ✅ | **Python:** 3.10+

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Running the Server](#-running-the-server)
- [API Endpoints](#-api-endpoints)
- [Authentication](#-authentication)
- [Machine Learning Models](#-machine-learning-models)
- [Database](#-database)
- [Testing](#-testing)
- [Docker Deployment](#-docker-deployment)
- [MLFlow Integration](#-mlflow-integration)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or conda
- Git

### Setup & Run (5 minutes)

```powershell
# Clone/Navigate to project
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel

# Create virtual environment
python -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install -r ml-service/requirements.txt

# Start server
uvicorn ml-service.app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/v1/health

---

## 📁 Project Structure

```
ml-service/
├── app/
│   ├── __init__.py
│   ├── main.py                    FastAPI app setup, CORS, middleware
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              All endpoints (predict, login, stats, etc.)
│   │   └── auth.py                JWT token creation/validation
│   │
│   ├── services/
│   │   └── hotel_recommendation.py ML service for hotel recommendations
│   │
│   ├── schemas/
│   │   └── input_schema.py        Pydantic request/response models
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              Configuration & settings
│   │   ├── models.py              SQLAlchemy ORM models
│   │   ├── security.py            JWT & password utilities
│   │   └── database.py            Database connection
│   │
│   └── utils/
│       └── [utilities]
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               Pytest fixtures
│   ├── unit/                     Unit tests
│   └── integration/              Integration tests
│
├── Dockerfile                    Multi-stage Docker build
├── requirements.txt              Python dependencies
├── pytest.ini                    Pytest configuration
├── AUTH_API.md                   API documentation
└── README.md                     (This file)
```

---

## 🛠️ Installation & Setup

### Step 1: Create Virtual Environment

```powershell
# From project root
python -m venv .venv
```

### Step 2: Activate Virtual Environment

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

```powershell
# Install main dependencies
pip install -r requirements.txt

# Install ML service dependencies
pip install -r ml-service/requirements.txt

# For testing
pip install pytest pytest-asyncio
```

### Step 4: Create Database

```powershell
# Database auto-creates on first run, or manually:
python -c "
from ml_service.app.core.database import Base, engine
Base.metadata.create_all(bind=engine)
print('Database created successfully!')
"
```

---

## ▶️ Running the Server

### Development Mode (with auto-reload)

```powershell
uvicorn ml-service.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```powershell
uvicorn ml-service.app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Gunicorn (Production)

```powershell
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker ml-service.app.main:app
```

### Options

- `--reload` - Auto-restart on code changes
- `--host 0.0.0.0` - Listen on all interfaces
- `--port 8000` - Port (default: 8000)
- `--workers 4` - Number of worker processes
- `--log-level debug` - Debug logging

---

## 🔌 API Endpoints

**Base URL:** `http://localhost:8000/v1`

### Authentication

```
POST /login              Login with email & password → JWT token
POST /register           Create new user account
POST /logout             Invalidate session (optional)
```

**Example - Login:**
```bash
curl -X POST http://localhost:8000/v1/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {...}
}
```

### Predictions (Protected Endpoints)

```
POST /predict            Flight price prediction (requires JWT)
POST /predict-gender     Gender classification (requires JWT)
POST /recommend-hotels   Hotel recommendations (requires JWT)
GET  /stats              User prediction statistics (requires JWT)
```

**Example - Flight Prediction:**
```bash
curl -X POST http://localhost:8000/v1/predict \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "Air India",
    "route": "NYC-LAX",
    "distance": 2475,
    "days_until_departure": 7,
    "num_stops": 0,
    "departure_time": "morning"
  }'
```

### Health & Info

```
GET /health              Service health check
GET /info                API information
```

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🔐 Authentication

### JWT Token Flow

1. **Register** - Create new user account
```bash
POST /v1/register
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "secure_password"
}
```

2. **Login** - Get JWT token
```bash
POST /v1/login
{
  "email": "user@example.com",
  "password": "secure_password"
}
# Response: { "access_token": "...", "token_type": "bearer" }
```

3. **Use Token** - Include in Authorization header
```bash
Authorization: Bearer <access_token>
```

### Token Details

- **Algorithm:** HS256
- **Expiration:** 24 hours (configurable in `core/config.py`)
- **Storage:** Bearer token in Authorization header
- **Scope:** All protected endpoints

### Configuration

Edit `ml-service/app/core/config.py`:
```python
JWT_SECRET_KEY = "your-secret-key"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 24 hours
```

---

## 🤖 Machine Learning Models

### 1. Flight Price Prediction

**File:** `components/regerssion_model_train.py`

- **Type:** Regression
- **Algorithm:** GradientBoosting
- **Features:** 6+ input features
- **Performance:** R² > 0.85, MAE < $50
- **Inference Time:** ~10ms

**Input Features:**
- airline (categorical)
- route (categorical)
- distance (numeric)
- days_until_departure (numeric)
- num_stops (numeric)
- departure_time (categorical: morning/afternoon/evening)

**Output:**
- predicted_price (float)

**Training:**
```powershell
cd components
python regerssion_model_train.py
```

### 2. Gender Classification

**File:** `components/gender_classification_model.py`

- **Type:** Classification (Binary)
- **Algorithm:** LogisticRegression
- **Features:** 5+ travel behavior features
- **Performance:** Accuracy > 85%
- **Inference Time:** ~5ms

**Input Features:**
- age (numeric)
- avg_flight_price (numeric)
- num_flights_per_month (numeric)
- preferred_destination (categorical)
- travel_class (categorical: economy/business/first)

**Output:**
- predicted_gender (male/female/unknown)
- confidence (0-1)

**Training:**
```powershell
cd components
python gender_classification_model.py
```

### 3. Hotel Recommendations

**File:** `ml-service/app/services/hotel_recommendation.py`

- **Type:** Ranking/Collaborative Filtering
- **Algorithm:** RandomForest (300 trees)
- **Features:** 7+ input features
- **Output:** Top-N hotels with match scores
- **Inference Time:** ~50ms

**Input Features:**
- days (travel duration: 1-30)
- month (travel month: 1-12)
- age (user age: 18-100)
- gender (male/female/unknown)
- budget (budget/mid/luxury)
- company (4You/Acme Factory/Monsters/Umbrella/Wonka)

**Output:**
- hotel_name (string)
- hotel_id (int)
- match_score (0-100%)
- rating (float)

**Training:**
```powershell
.\scripts\train_hotel_recommendation.ps1
```

**Model Location:** `models/hotel_recommendation/hotel_recommender.pkl`

---

## 💾 Database

### SQLite Setup

Database file: `voyage_analytics.db` (auto-created)

### ORM Models (SQLAlchemy)

Located in `app/core/models.py`:

```python
# User table
class User(Base):
    id: int
    email: str (unique)
    name: str
    hashed_password: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

# Prediction table
class Prediction(Base):
    id: int
    user_id: int (FK → User)
    model_type: str (flight/gender/hotel)
    input_data: JSON
    output_data: JSON
    created_at: datetime
```

### Database Operations

```python
from ml_service.app.core.database import SessionLocal
from ml_service.app.core.models import User, Prediction

# Create session
db = SessionLocal()

# Query user
user = db.query(User).filter(User.email == "user@example.com").first()

# Create prediction
prediction = Prediction(
    user_id=user.id,
    model_type="flight",
    input_data={"airline": "Air India", ...},
    output_data={"predicted_price": 150.50}
)
db.add(prediction)
db.commit()
```

### Reset Database

```powershell
# Delete database file
Remove-Item voyage_analytics.db

# Restart server (auto-creates)
uvicorn ml-service.app.main:app --reload
```

---

## 🧪 Testing

### Run All Tests

```powershell
cd ml-service
python -m pytest -v
```

### Run Specific Test Suite

```powershell
# Unit tests only
python -m pytest tests/unit -v

# Integration tests only
python -m pytest tests/integration -v

# Single test file
python -m pytest tests/unit/test_auth.py -v

# Tests matching keyword
python -m pytest -k "health" -v
```

### Test Coverage

```powershell
pip install pytest-cov
python -m pytest --cov=app tests/
```

### Common Test Commands

```powershell
# Verbose output
python -m pytest -v

# Show print statements
python -m pytest -s

# Stop on first failure
python -m pytest -x

# Parallel execution
pip install pytest-xdist
python -m pytest -n 4
```

---

## 🐳 Docker Deployment

### Build Docker Image

```powershell
# From project root
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel

# Build
docker build -f .\ml-service\Dockerfile -t voyage-ml-service:latest .

# Check image
docker images | findstr voyage
```

### Run Docker Container

```powershell
# Interactive
docker run -p 8000:8000 voyage-ml-service:latest

# Detached
docker run -d --name voyage-api -p 8000:8000 voyage-ml-service:latest

# With environment variables
docker run -d --name voyage-api \
  -p 8000:8000 \
  -e JWT_SECRET_KEY="your-secret" \
  -e DATABASE_URL="sqlite:///./voyage.db" \
  voyage-ml-service:latest
```

### Container Management

```powershell
# List containers
docker ps -a

# View logs
docker logs voyage-api
docker logs -f voyage-api  # Follow logs

# Stop container
docker stop voyage-api

# Remove container
docker rm voyage-api

# Restart container
docker restart voyage-api
```

### Docker Compose

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f ml-service

# Stop services
docker-compose down
```

---

## 🔄 MLFlow Integration

### Start MLFlow Server

```powershell
# File-based tracking
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000

# Or use included script
.\scripts\train_with_mlflow.ps1 -StartUi
```

### Access MLFlow UI

Visit: http://localhost:5000

### Track Experiments Manually

```python
import mlflow

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("flight-price-prediction")

with mlflow.start_run():
    mlflow.log_metric("r2_score", 0.85)
    mlflow.log_metric("mae", 45.5)
    mlflow.log_params({"model": "GradientBoosting", "trees": 100})
    mlflow.sklearn.log_model(model, "model")
```

### Training Scripts

```powershell
# Flight price model
.\scripts\train_with_mlflow.ps1 -StartUi

# Gender classification model
.\scripts\train_gender_with_mlflow.ps1 -StartUi

# Hotel recommendations
.\scripts\train_hotel_recommendation.ps1
```

---

## 🐛 Troubleshooting

### "Address already in use" on port 8000

```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or use different port
uvicorn ml-service.app.main:app --port 8001
```

### "ModuleNotFoundError" when importing

```powershell
# Ensure virtual environment is active
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
pip install -r ml-service/requirements.txt
```

### Database locked error

```powershell
# Delete database and restart
Remove-Item voyage_analytics.db
uvicorn ml-service.app.main:app --reload
```

### JWT token expired

- Tokens expire after 24 hours (configurable)
- User must login again to get new token
- Change `ACCESS_TOKEN_EXPIRE_MINUTES` in config

### Models not loading

```powershell
# Check model files exist
Get-Item models/final_model.pkl
Get-Item models/gender_model.pkl
Get-Item models/hotel_recommendation/hotel_recommender.pkl

# If missing, train models
.\scripts\train_with_mlflow.ps1
.\scripts\train_gender_with_mlflow.ps1
.\scripts\train_hotel_recommendation.ps1
```

### CORS errors from frontend

Check `ml-service/app/main.py` has CORS enabled for frontend URL:
```python
allow_origins=["http://localhost:5173", "http://localhost"]
```

### Connection refused to database

```powershell
# Ensure database URL is correct
# Default: sqlite:///./voyage_analytics.db

# Check database exists
Get-Item voyage_analytics.db

# If not, restart server to auto-create
```

---

## 📚 Configuration

### Environment Variables

Create `.env` file in project root:
```
DATABASE_URL=sqlite:///./voyage_analytics.db
JWT_SECRET_KEY=your-secret-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
MLFLOW_TRACKING_URI=http://localhost:5000
LOG_LEVEL=INFO
```

### Configuration File

Edit `ml-service/app/core/config.py`:
```python
class Settings:
    DATABASE_URL: str = "sqlite:///./voyage_analytics.db"
    JWT_SECRET_KEY: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60
```

---

## 🚀 Performance

### Typical Response Times
- Flight Prediction: ~10ms
- Gender Classification: ~5ms
- Hotel Recommendations: ~50ms
- Login: ~50ms

### Optimization Tips
1. Use connection pooling in production
2. Add caching for predictions
3. Use async/await for I/O operations
4. Monitor with MLFlow and logging

---

## 📞 Support

**Issues?** Check [../README.md](../README.md) for general project info  
**Frontend?** See [../frontend/README.md](../frontend/README.md)  
**Documentation?** Check [AUTH_API.md](AUTH_API.md)

---

**Last Updated:** April 19, 2026 | **Version:** 1.0.0

Set environment variables before starting API locally:

```powershell
$env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"
$env:MODEL_URI="models:/flight-price-model/Production"
python -m uvicorn app.main:app --reload
```

Run Docker with MLflow model URI:

```powershell
docker run --name voyage-ml-service -p 8000:8000 ^
	-e MLFLOW_TRACKING_URI="http://host.docker.internal:5000" ^
	-e MODEL_URI="models:/flight-price-model/Production" ^
	voyage-ml-service:latest
```

If `MODEL_URI` is not provided, the service falls back to `models/final_model.pkl` in the container.
## 9) Deploy gender classification model via MLflow

Both flight price and gender classification models support MLflow versioning.

Set gender model URI:

```powershell
$env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"
$env:GENDER_MODEL_URI="models:/gender-classification-model/Production"
python -m uvicorn app.main:app --reload
```

Run Docker with gender model MLflow URI:

```powershell
docker run --name voyage-ml-service -p 8000:8000 ^
  -e MLFLOW_TRACKING_URI="http://host.docker.internal:5000" ^
  -e GENDER_MODEL_URI="models:/gender-classification-model/Production" ^
  voyage-ml-service:latest
```

Deploy both models from MLflow:

```powershell
docker run --name voyage-ml-service -p 8000:8000 ^
  -e MLFLOW_TRACKING_URI="http://host.docker.internal:5000" ^
  -e MODEL_URI="models:/flight-price-model/Production" ^
  -e GENDER_MODEL_URI="models:/gender-classification-model/Production" ^
  voyage-ml-service:latest
```