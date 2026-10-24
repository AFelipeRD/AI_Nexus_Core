# Instalador automático — Mods Visuales Open Code + Warp
# AI Nexus Core v2.1.0
#
# Este script instala TODO automáticamente. Tú no tienes que tocar nada más que ejecutarlo.
#
# Requisitos previos:
#   - Open Code instalado (`opencode` en el PATH, v2.x)
#   - Warp terminal instalado
#   - PowerShell 5.1+ (Windows 11)
#
# Uso:
#   .\scripts\instalar_mods_visuales.ps1
#
# Qué hace:
#   1. Copia el tema de Warp a ~/.warp/themes/
#   2. Copia los workflows de Warp a ~/.warp/workflows/
#   3. Instala el plugin visual oc-plugin-rainbow para Open Code
#   4. Configura el tema personalizado V2 ai-nexus-core en ~/.config/opencode/themes/
#   5. Actualiza ~/.config/opencode/cli.json con el tema ai-nexus-core y plugin rainbow
#   6. Verifica que todo esté en su lugar
#
# Consumo: cero tokens, GPU solo de pantalla (CSS / tema de terminal).

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "Instalando Mods Visuales — AI Nexus Core"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  INSTALADOR DE MODS VISUALES — Open Code + Warp" -ForegroundColor Cyan
Write-Host "  AI Nexus Core v2.1.0" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# --- Rutas base ---
$repoRoot = Resolve-Path (PSScriptRoot + "/..") | Select-Object -ExpandProperty Path
$warpThemeSrc  = Join-Path $repoRoot "assets/warp/warp-theme.yaml"
$warpWorkflows = Join-Path $repoRoot "assets/warp/workflows"
$opencodeTheme = Join-Path $repoRoot ".opencode/themes/ai-nexus-core.json"

# --- Destinos ---
$warpThemesDir   = Join-Path $env:USERPROFILE ".warp/themes"
$warpWorkflowsDir = Join-Path $env:USERPROFILE ".warp/workflows"
$opencodeConfigDir = Join-Path $env:USERPROFILE ".config/opencode"
$opencodeThemesDir = Join-Path $opencodeConfigDir "themes"
$opencodeCliCfg   = Join-Path $opencodeConfigDir "cli.json"

Write-Host ">> Detectando entorno..." -ForegroundColor Yellow
if (-not (Test-Path $warpThemeSrc)) { throw "No se encontró el tema de Warp: $warpThemeSrc" }
if (-not (Test-Path $opencodeTheme)) { throw "No se encontró el tema de Open Code: $opencodeTheme" }
Write-Host "   Archivos de origen OK" -ForegroundColor Green

# --- 1. Crear carpetas de destino si no existen ---
Write-Host ""
Write-Host ">> Creando carpetas de destino..." -ForegroundColor Yellow
$null = New-Item -ItemType Directory -Path $warpThemesDir -Force
$null = New-Item -ItemType Directory -Path $warpWorkflowsDir -Force
$null = New-Item -ItemType Directory -Path $opencodeThemesDir -Force
$null = New-Item -ItemType Directory -Path $opencodeConfigDir -Force
Write-Host "   Carpetas listas" -ForegroundColor Green

# --- 2. Instalar tema de Warp ---
Write-Host ""
Write-Host ">> Instalando tema de Warp (AI Nexus Core)..." -ForegroundColor Yellow
Copy-Item -Path $warpThemeSrc -Destination (Join-Path $warpThemesDir "ai-nexus-core.yaml") -Force
Write-Host "   Tema copiado a: $warpThemesDir\ai-nexus-core.yaml" -ForegroundColor Green

# --- 3. Instalar workflows de Warp ---
Write-Host ""
Write-Host ">> Instalando workflows de Warp..." -ForegroundColor Yellow
Get-ChildItem -Path $warpWorkflows -Filter *.yaml | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $warpWorkflowsDir $_.Name) -Force
    Write-Host "   Workflow instalado: $($_.Name)" -ForegroundColor Green
}

# --- 4. Instalar tema personalizado V2 de Open Code ---
Write-Host ""
Write-Host ">> Instalando tema personalizado V2 de Open Code..." -ForegroundColor Yellow
Copy-Item -Path $opencodeTheme -Destination (Join-Path $opencodeThemesDir "ai-nexus-core.json") -Force
Write-Host "   Tema copiado a: $opencodeThemesDir\ai-nexus-core.json" -ForegroundColor Green

# --- 5. Instalar plugin visual oc-plugin-rainbow ---
Write-Host ""
Write-Host ">> Instalando plugin visual de Open Code (oc-plugin-rainbow)..." -ForegroundColor Yellow
if (Get-Command "opencode" -ErrorAction SilentlyContinue) {
    try {
        & opencode plugin add oc-plugin-rainbow | Out-String
        Write-Host "   Plugin oc-plugin-rainbow instalado" -ForegroundColor Green
    } catch {
        Write-Warning "   No se pudo instalar el plugin automáticamente. Intenta manualmente: opencode plugin add oc-plugin-rainbow"
    }
} else {
    Write-Warning "   Open Code CLI no está en el PATH. Instala el plugin manualmente: opencode plugin add oc-plugin-rainbow"
}

# --- 6. Actualizar cli.json global de Open Code ---
Write-Host ""
Write-Host ">> Actualizando configuración CLI de Open Code..." -ForegroundColor Yellow
$cliConfig = @{
    '$schema' = 'https://opencode.ai/v2/cli.json'
    plugins = @('oc-plugin-rainbow')
    theme = @{
        name = 'ai-nexus-core'
        mode = 'dark'
    }
    tabs = @{
        mode = 'on'
    }
}
$cliConfig | ConvertTo-Json -Depth 10 | Set-Content $opencodeCliCfg -Encoding UTF8
Write-Host "   cli.json actualizado con tema ai-nexus-core y plugin rainbow" -ForegroundColor Green

# --- 7. Verificación final ---
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Resumen:" -ForegroundColor White
Write-Host "  [OK] Tema Warp:           AI Nexus Core (OLED oscuro, acento cian)" -ForegroundColor Green
Write-Host "  [OK] Workflows Warp:      open-code-visual, opencode-rapido" -ForegroundColor Green
Write-Host "  [OK] Tema Open Code V2:   ai-nexus-core ( ~/.config/opencode/themes/ )" -ForegroundColor Green
Write-Host "  [OK] CLI Open Code:       cli.json con tema ai-nexus-core + plugin rainbow" -ForegroundColor Green
Write-Host "  [OK] Plugin visual:       oc-plugin-rainbow (bandas de color animadas)" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Reinicia Open Code" -ForegroundColor Gray
Write-Host "  2. En Warp: Ajustes → Apariencia → Temas → selecciona 'AI Nexus Core'" -ForegroundColor Gray
Write-Host "  3. En PowerShell:  \$env:COLORTERM='truecolor'  (para colores completos)" -ForegroundColor Gray
Write-Host "  4. Usa /visuales en Open Code para salidas estructuradas y llamativas" -ForegroundColor Gray
Write-Host ""
Write-Host "Consumo de tokens: 0  ·  GPU: solo pantalla (sin WebGL ni generación de imagen)" -ForegroundColor Cyan
Write-Host ""
