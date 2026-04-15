# ML Service Run Guide

This guide explains how to run the FastAPI ML service and its test cases.

## 1) Prerequisites

- Python 3.10+
- pip
- Windows PowerShell or Command Prompt

## 2) Create and activate a virtual environment

Run these commands from the project root:

```powershell
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
python -m venv .venv
```

Activate the environment:

### PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Command Prompt (cmd)

```bat
.venv\Scripts\activate.bat
```

## 3) Install ML service dependencies

From the project root:

```powershell
pip install -r .\ml-service\requirements.txt
pip install pytest
```

## 4) Run the ML service

Move into the service folder:

```powershell
cd .\ml-service
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

Useful URLs:

- Health: http://127.0.0.1:8000/v1/health
- Docs: http://127.0.0.1:8000/docs

Note:
- The API router uses the `/v1` prefix, so `/health` returns 404 and `/v1/health` returns 200.

## 5) Run test cases

From `ml-service` folder:

```powershell
python -m pytest -q
```

Run only unit tests:

```powershell
python -m pytest tests/unit -q
```

Run only integration tests:

```powershell
python -m pytest tests/integration -q
```

Run a single test file:

```powershell
python -m pytest tests/integration/test_routes.py -q
```

Run matching tests by keyword:

```powershell
python -m pytest -k health -q
```

## 6) Common command mistake

Do not run:

```powershell
python pytest -q
```

This fails because Python treats `pytest` as a file path.

Use:

```powershell
python -m pytest -q
```

## 7) Containerization and deployment with Docker

Build the image from the repository root so both the API code and model artifacts are included:

```powershell
cd E:\Voyage-Analytics-Intregrating-MLOps-in-Travel
docker build -f .\ml-service\Dockerfile -t voyage-ml-service:latest .
```

Run the container:

```powershell
docker run --name voyage-ml-service -p 8000:8000 voyage-ml-service:latest
```

Run in detached mode:

```powershell
docker run -d --name voyage-ml-service -p 8000:8000 voyage-ml-service:latest
```

Verify deployment:

```powershell
curl http://127.0.0.1:8000/v1/health
```

Stop and remove container:

```powershell
docker stop voyage-ml-service
docker rm voyage-ml-service
```

## 8) Deploy specific model versions via MLflow

The API can load a local model file or a versioned MLflow model URI.

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