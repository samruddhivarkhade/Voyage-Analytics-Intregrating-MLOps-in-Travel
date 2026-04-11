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
