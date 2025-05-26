@echo off
echo 🚀 Desplegando PartyFinder (Configuración de Red)...
echo.

echo 🔄 Deteniendo procesos anteriores...
taskkill /f /im node.exe 2>nul
taskkill /f /im expo.exe 2>nul
echo ✅ Procesos detenidos

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
echo 🌐 Configurando red...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set "LOCAL_IP=%%a"
    goto :found_ip
)
:found_ip
set LOCAL_IP=%LOCAL_IP: =%
echo ✅ IP local detectada: %LOCAL_IP%
echo 📱 La app móvil se conectará a: http://%LOCAL_IP%:3001

echo.
echo 🚀 Iniciando servidor...
start /b node server.js
echo ✅ Servidor iniciado en segundo plano

echo.
echo ⏳ Esperando que el servidor se inicie...
timeout /t 8 /nobreak >nul

echo.
echo 🔍 Verificando conexión...
powershell -Command "try { Invoke-WebRequest -Uri 'http://%LOCAL_IP%:3001/api/health' -UseBasicParsing -TimeoutSec 5 | Out-Null; Write-Host '✅ Servidor accesible desde la red' } catch { Write-Host '❌ Error de conexión, verificando localhost...' }"

powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:3001/api/health' -UseBasicParsing -TimeoutSec 5 | Out-Null; Write-Host '✅ Servidor funcionando en localhost' } catch { Write-Host '❌ Servidor no responde' }"

echo.
echo 🎯 Iniciando aplicación Expo...
echo.
echo 📋 INSTRUCCIONES:
echo 📱 Para MÓVIL: Escanea el QR code con Expo Go
echo 🌐 Para WEB: Presiona 'w' y abre http://localhost:8081
echo 🔧 Para ANDROID: Presiona 'a' (requiere emulador)
echo.
echo 🌐 APIs disponibles:
echo    - Servidor: http://%LOCAL_IP%:3001
echo    - Estado: http://%LOCAL_IP%:3001/api/health
echo    - Datos: http://%LOCAL_IP%:3001/api/data/complete
echo.

npm start

echo.
echo ✅ Despliegue completado!
pause 