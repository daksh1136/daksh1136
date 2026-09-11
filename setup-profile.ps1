$ErrorActionPreference = "Stop"

Write-Host "=== daksh1136 GitHub Profile Setup ===" -ForegroundColor Cyan

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or not on PATH."
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI is not installed or not on PATH."
}

gh auth status
if ($LASTEXITCODE -ne 0) {
    throw "Run: gh auth login"
}

if (-not (Test-Path ".git")) {
    git init
    git branch -M main
}

$remote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote add origin "https://github.com/daksh1136/daksh1136.git"
}

git add .
git commit -m "feat: animated terminal GitHub profile" 2>$null
git push -u origin main

Write-Host "Done: https://github.com/daksh1136/daksh1136" -ForegroundColor Green
Write-Host "Then: Actions -> Update profile art -> Run workflow" -ForegroundColor Cyan
