# Enterprise AI Assistant Setup Script for Windows

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Enterprise AI Assistant - Setup Wizard                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Step 2: Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Step 3: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Step 4: Setting up environment file..." -ForegroundColor Yellow
if (Test-Path .env) {
    Write-Host "  .env file already exists, skipping..." -ForegroundColor Green
} else {
    Copy-Item .env.example .env
    Write-Host "  Created .env file from template" -ForegroundColor Green
    Write-Host "  ⚠️  Please edit .env and add your API keys!" -ForegroundColor Red
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit .env file and add your API keys"
Write-Host "  2. Run: python run.py --llm openai"
Write-Host "  3. Test: python demo_scenarios.py"
Write-Host ""
