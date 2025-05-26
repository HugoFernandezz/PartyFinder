# Script de despliegue de PartyFinder en PowerShell
Write-Host "🚀 Desplegando PartyFinder..." -ForegroundColor Green
Write-Host ""

# Función para verificar si un comando existe
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Paso 1: Limpiar caché
Write-Host "🧹 Limpiando caché..." -ForegroundColor Yellow
if (Test-Path "clear-cache.bat") {
    & .\clear-cache.bat
} else {
    Write-Host "❌ clear-cache.bat no encontrado, limpiando manualmente..." -ForegroundColor Red
    
    # Limpiar caché manualmente
    Write-Host "🗑️ Limpiando caché de npm..."
    if (Test-Command "npm") {
        npm cache clean --force
    }
    
    # Eliminar directorios de caché
    if (Test-Path ".expo") {
        Remove-Item -Recurse -Force ".expo" -ErrorAction SilentlyContinue
        Write-Host "✅ Directorio .expo eliminado"
    }
    
    if (Test-Path "node_modules\.cache") {
        Remove-Item -Recurse -Force "node_modules\.cache" -ErrorAction SilentlyContinue
        Write-Host "✅ Cache de node_modules eliminada"
    }
}

Write-Host ""

# Paso 2: Verificar scraper
Write-Host "🔧 Verificando scraper..." -ForegroundColor Yellow
try {
    $scraperResult = & python simple_scraper.py --json-only 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Scraper funcionando correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error en el scraper, pero continuando" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error ejecutando scraper: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Paso 3: Verificar Node.js
Write-Host "🔍 Verificando Node.js..." -ForegroundColor Yellow
if (Test-Command "node") {
    $nodeVersion = & node --version
    Write-Host "✅ Node.js encontrado: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js no encontrado" -ForegroundColor Red
    Write-Host "📥 Por favor instala Node.js desde: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar de todos modos"
}

Write-Host ""

# Paso 4: Detener procesos anteriores
Write-Host "🔄 Deteniendo procesos anteriores..." -ForegroundColor Yellow
Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "✅ Procesos anteriores detenidos" -ForegroundColor Green

Write-Host ""

# Paso 5: Iniciar servidor
Write-Host "🚀 Iniciando servidor..." -ForegroundColor Yellow
try {
    $serverProcess = Start-Process -FilePath "node" -ArgumentList "server.js" -WindowStyle Hidden -PassThru
    Write-Host "✅ Servidor iniciado (PID: $($serverProcess.Id))" -ForegroundColor Green
} catch {
    Write-Host "❌ Error iniciando servidor: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Intentando iniciar manualmente..." -ForegroundColor Yellow
    Start-Process -FilePath "cmd" -ArgumentList "/c", "node server.js" -WindowStyle Minimized
}

Write-Host ""

# Paso 6: Esperar y verificar servidor
Write-Host "⏳ Esperando que el servidor se inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "🔍 Verificando que el servidor responda..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001/api/health" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Servidor respondiendo correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Servidor responde con código: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Servidor no responde, pero continuando..." -ForegroundColor Red
    Write-Host "💡 Puedes verificar manualmente en: http://localhost:3001/api/health" -ForegroundColor Yellow
}

Write-Host ""

# Paso 7: Iniciar aplicación Expo
Write-Host "🎯 Iniciando aplicación Expo..." -ForegroundColor Yellow
Write-Host "📱 La aplicación se abrirá automáticamente" -ForegroundColor Cyan
Write-Host "🌐 Servidor: http://localhost:3001" -ForegroundColor Cyan
Write-Host "📲 Escanea el QR code con Expo Go en tu móvil" -ForegroundColor Cyan
Write-Host ""

if (Test-Command "npm") {
    Write-Host "🚀 Iniciando con npm..." -ForegroundColor Green
    & npm start
} elseif (Test-Command "npx") {
    Write-Host "🚀 Iniciando con npx..." -ForegroundColor Green
    & npx expo start
} else {
    Write-Host "❌ No se encontró npm ni npx" -ForegroundColor Red
    Write-Host "📥 Por favor reinstala Node.js desde: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "✅ Despliegue completado!" -ForegroundColor Green
Read-Host "Presiona Enter para salir" 