# Hotel Recommendation Model Training Script
# Trains the hotel recommendation model using RandomForest

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$mlServicePath = Join-Path $projectRoot "ml-service"

# Activate virtual environment (if it exists)
$venvPath = Join-Path $projectRoot ".venv"
if (Test-Path (Join-Path $venvPath "Scripts" "Activate.ps1")) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & (Join-Path $venvPath "Scripts" "Activate.ps1")
}

Write-Host "`n=================================" -ForegroundColor Cyan
Write-Host "Hotel Recommendation Model Training" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Run training script
Write-Host "`nStarting training pipeline..." -ForegroundColor Green
python $scriptDir\train_hotel_recommendation.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Training completed successfully!" -ForegroundColor Green
    Write-Host "Model saved to: $projectRoot\models\hotel_recommendation\hotel_recommender.pkl" -ForegroundColor Green
} else {
    Write-Host "`n✗ Training failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

Write-Host "`nDone!" -ForegroundColor Cyan
