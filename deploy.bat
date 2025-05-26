@echo off
echo 🚀 Desplegando PartyFinder...
echo.

echo 🧹 Paso 1: Limpiando cache...
call clear-cache.bat

echo.
echo 🔧 Paso 1.5: Verificando scraper...
echo Probando el nuevo scraper simplificado...
python simple_scraper.py --json-only > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Scraper funcionando correctamente
) else (
    echo ❌ Error en el scraper, pero continuando con datos de ejemplo
)

echo.
echo 🔧 Paso 2: Verificando configuración...

echo 📡 Verificando servidor...
node -e "
const http = require('http');
const options = {
  hostname: 'localhost',
  port: 3001,
  path: '/api/health',
  method: 'GET',
  timeout: 5000
};

const req = http.request(options, (res) => {
  console.log('✅ Servidor respondiendo en puerto 3001');
  process.exit(0);
});

req.on('error', (err) => {
  console.log('❌ Servidor no disponible en puerto 3001');
  console.log('🔄 Iniciando servidor...');
  process.exit(1);
});

req.on('timeout', () => {
  console.log('⏰ Timeout conectando al servidor');
  req.destroy();
  process.exit(1);
});

req.end();
"

if %errorlevel% neq 0 (
    echo 🔄 Iniciando servidor en segundo plano...
    start /b node server.js
    timeout /t 5 /nobreak >nul
)

echo.
echo 🎯 Paso 3: Iniciando aplicación...
echo 📱 La aplicación se abrirá en tu navegador y/o dispositivo
echo 🌐 URL del servidor: http://localhost:3001
echo 📲 Escanea el QR code para abrir en tu dispositivo móvil
echo.

echo 🚀 Iniciando Expo...
npm start

echo.
echo ✅ Despliegue completado!
pause 