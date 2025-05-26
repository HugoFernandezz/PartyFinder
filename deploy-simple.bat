@echo off
echo 🚀 Desplegando PartyFinder (Versión Simplificada)...
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
echo 🚀 Iniciando servidor...
start /b node server.js
echo ✅ Servidor iniciado en segundo plano

echo.
echo ⏳ Esperando que el servidor se inicie...
timeout /t 5 /nobreak >nul

echo.
echo 🎯 Iniciando aplicación Expo...
echo 📱 La aplicación se abrirá automáticamente
echo 🌐 Servidor: http://localhost:3001
echo.

npm start

echo.
echo ✅ Despliegue completado!
pause 