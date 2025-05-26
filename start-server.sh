#!/bin/bash

echo "🚀 Iniciando PartyFinder Server..."

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado. Por favor instala Node.js primero."
    exit 1
fi

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python no está instalado. Por favor instala Python primero."
    exit 1
fi

# Verificar si BeautifulSoup está instalado
python -c "import bs4" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Instalando BeautifulSoup4..."
    pip install beautifulsoup4
fi

# Instalar dependencias de Node.js si no existen
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias de Node.js..."
    npm install express cors nodemon
fi

# Ejecutar una prueba del script de Python
echo "🐍 Probando script de Python..."
python fourvenues_scraper.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Script de Python funcionando correctamente"
else
    echo "⚠️  Advertencia: El script de Python puede tener problemas"
fi

# Iniciar el servidor
echo "🌐 Iniciando servidor en puerto 3001..."
echo "📱 Tu app React Native debe apuntar a: http://localhost:3001"
echo "🔄 El servidor actualizará datos cada 6 horas automáticamente"
echo ""
echo "Endpoints disponibles:"
echo "  - GET  /api/data/complete     (Todos los datos)"
echo "  - GET  /api/parties/today     (Fiestas de hoy)"
echo "  - GET  /api/venues/active     (Locales activos)"
echo "  - GET  /api/status            (Estado del servidor)"
echo "  - POST /api/update            (Forzar actualización)"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "----------------------------------------"

node server.js 