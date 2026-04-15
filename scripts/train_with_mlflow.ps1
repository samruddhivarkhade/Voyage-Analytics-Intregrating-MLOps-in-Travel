param(
    [string]$TrackingUri = "file:./mlruns",
    [string]$ExperimentName = "flight-price-prediction",
    [string]$RegisteredModelName = "flight-price-model",
    [switch]$StartUi,
    [int]$UiPort = 5000,
    [string]$UiBackendStoreUri = "./mlruns"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
Set-Location $repoRoot

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$pythonExe = "python"
if (Test-Path $venvPython) {
    $pythonExe = $venvPython
}

$env:MLFLOW_TRACKING_URI = $TrackingUri
$env:MLFLOW_EXPERIMENT_NAME = $ExperimentName
$env:MLFLOW_REGISTERED_MODEL_NAME = $RegisteredModelName

Write-Host "MLflow configuration:" -ForegroundColor Cyan
Write-Host "  MLFLOW_TRACKING_URI=$($env:MLFLOW_TRACKING_URI)"
Write-Host "  MLFLOW_EXPERIMENT_NAME=$($env:MLFLOW_EXPERIMENT_NAME)"
Write-Host "  MLFLOW_REGISTERED_MODEL_NAME=$($env:MLFLOW_REGISTERED_MODEL_NAME)"

if ($StartUi) {
    Write-Host "Starting MLflow UI at http://127.0.0.1:$UiPort" -ForegroundColor Yellow
    Start-Process -FilePath $pythonExe -ArgumentList "-m", "mlflow", "ui", "--backend-store-uri", $UiBackendStoreUri, "--port", $UiPort
}

Write-Host "Running training script with MLflow tracking..." -ForegroundColor Green
& $pythonExe .\regerssion_model_train.py
