# Launch the MathViz API server (reload mode).
# Usage:  .\scripts\run.ps1    (then open http://127.0.0.1:8000)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..
if (-not (Test-Path ".venv")) {
    Write-Host "No .venv found. Create one with:  python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -e ."
}
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000