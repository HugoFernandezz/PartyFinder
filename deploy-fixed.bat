@echo off
echo 🚀 Desplegando PartyFinder (Versión Corregida)...
echo.

echo 🧹 Limpiando cache...
call clear-cache.bat

echo.
echo 🔧 Verificando scraper...
python simple_scraper.py --json-only > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Scraper funcionando correctamente
) else (
    echo ❌ Error en el scraper, pero continuando
)

echo.
echo 🔍 Verificando Node.js...
where node > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Node.js encontrado
    node --version
) else (
    echo ❌ Node.js no encontrado en PATH
    echo 💡 Intentando con rutas comunes...
    
    REM Intentar rutas comunes de Node.js
    if exist "C:\Program Files\nodejs\node.exe" (
        set "NODE_PATH=C:\Program Files\nodejs\node.exe"
        echo ✅ Node.js encontrado en: C:\Program Files\nodejs\
    ) else if exist "C:\Program Files (x86)\nodejs\node.exe" (
        set "NODE_PATH=C:\Program Files (x86)\nodejs\node.exe"
        echo ✅ Node.js encontrado en: C:\Program Files (x86)\nodejs\
    ) else (
        echo ❌ No se pudo encontrar Node.js
        echo 📥 Por favor instala Node.js desde: https://nodejs.org/
        pause
        exit /b 1
    )
)

echo.
echo 🚀 Iniciando servidor...
REM Usar PowerShell para iniciar el servidor en segundo plano
powershell -Command "Start-Process node -ArgumentList 'server.js' -WindowStyle Hidden"
echo ✅ Servidor iniciado en segundo plano

echo.
echo ⏳ Esperando que el servidor se inicie...
timeout /t 8 /nobreak >nul

echo.
echo 🔍 Verificando que el servidor responda...
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:3001/api/health' -UseBasicParsing -TimeoutSec 5 | Out-Null; Write-Host '✅ Servidor respondiendo correctamente' } catch { Write-Host '❌ Servidor no responde, pero continuando...' }"

echo.
echo 🎯 Iniciando aplicación Expo...
echo 📱 La aplicación se abrirá automáticamente
echo 🌐 Servidor: http://localhost:3001
echo 📲 Escanea el QR code con Expo Go en tu móvil
echo.

REM Verificar npm
where npm > nul 2>&1
if %errorlevel% equ 0 (
    npm start
) else (
    echo ❌ npm no encontrado
    echo 💡 Intentando con npx...
    where npx > nul 2>&1
    if %errorlevel% equ 0 (
        npx expo start
    ) else (
        echo ❌ No se pudo encontrar npm ni npx
        echo 📥 Por favor reinstala Node.js desde: https://nodejs.org/
        pause
        exit /b 1
    )
)

echo.
echo ✅ Despliegue completado!
pause 