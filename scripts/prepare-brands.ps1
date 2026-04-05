# PowerShell script to prepare brand assets for Home Assistant Brands submission
# Usage: .\scripts\prepare-brands.ps1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$BrandsDir = Join-Path $ProjectDir "brands"
$OutputDir = Join-Path $ProjectDir "dist\brands-submission"

Write-Host "Preparing brand assets for Home Assistant Brands submission..." -ForegroundColor Green

# Create output directory
$TargetDir = Join-Path $OutputDir "custom_integrations\domotique-sherbrooke"
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

# Copy all brand files
Get-ChildItem -Path $BrandsDir -Filter "*.svg" | ForEach-Object {
    Copy-Item $_.FullName -Destination $TargetDir -Force
    Write-Host "  Copied: $($_.Name)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ Brand assets prepared in: $OutputDir" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Fork https://github.com/home-assistant/brands"
Write-Host "2. Copy the contents of $OutputDir\custom_integrations\ to your fork"
Write-Host "3. Submit a Pull Request to home-assistant/brands"
Write-Host ""
Write-Host "Directory structure to submit:" -ForegroundColor Cyan
Get-ChildItem -Path $TargetDir -Recurse | Select-Object -ExpandProperty FullName | ForEach-Object {
    $relative = $_.Substring($OutputDir.Length + 1)
    Write-Host "  $relative"
}
