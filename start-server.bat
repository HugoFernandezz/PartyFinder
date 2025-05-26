@echo off
echo 🚀 Iniciando PartyFinder Server...

REM Verificar si Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js no está instalado. Por favor instala Node.js primero.
    pause
    exit /b 1
)

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado. Por favor instala Python primero.
    pause
    exit /b 1
)

REM Verificar si BeautifulSoup está instalado
python -c "import bs4" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando BeautifulSoup4...
    pip install beautifulsoup4
)

REM Instalar dependencias de Node.js si no existen
if not exist "node_modules" (
    echo 📦 Instalando dependencias de Node.js...
    npm install express cors nodemon
)

REM Ejecutar una prueba del script de Python
echo 🐍 Probando script de Python...
python fourvenues_scraper.py >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Script de Python funcionando correctamente
) else (
    echo ⚠️  Advertencia: El script de Python puede tener problemas
)

REM Iniciar el servidor
echo.
echo 🌐 Iniciando servidor en puerto 3001...
echo 📱 Tu app React Native debe apuntar a: http://localhost:3001
echo 🔄 El servidor actualizará datos cada 6 horas automáticamente
echo.
echo Endpoints disponibles:
echo   - GET  /api/data/complete     (Todos los datos)
echo   - GET  /api/parties/today     (Fiestas de hoy)
echo   - GET  /api/venues/active     (Locales activos)
echo   - GET  /api/status            (Estado del servidor)
echo   - POST /api/update            (Forzar actualización)
echo.
echo Presiona Ctrl+C para detener el servidor
echo ----------------------------------------

node server.js

pause 