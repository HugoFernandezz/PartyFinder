#!/bin/bash
# =============================================================================
# Setup Cloudflare Bypass para Raspberry Pi 4 ARM64
# =============================================================================
# Este script instala todas las dependencias necesarias para el bypass híbrido
# de Cloudflare en Raspberry Pi 4.
#
# Uso:
#   chmod +x setup_cloudflare_bypass.sh
#   ./setup_cloudflare_bypass.sh
# =============================================================================

set -e  # Salir en caso de error

echo "=============================================="
echo "PartyFinder - Setup Cloudflare Bypass"
echo "Raspberry Pi 4 ARM64"
echo "=============================================="
echo ""

# Verificar que estamos en ARM64
ARCH=$(uname -m)
if [[ "$ARCH" != "aarch64" && "$ARCH" != "arm64" ]]; then
    echo "⚠️  Advertencia: Este script está optimizado para ARM64"
    echo "   Arquitectura detectada: $ARCH"
    read -p "¿Continuar de todos modos? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# =============================================================================
# 1. Instalar dependencias del sistema
# =============================================================================
echo ""
echo "📦 [1/5] Instalando dependencias del sistema..."
echo ""

sudo apt update

# Xvfb para display virtual
sudo apt install -y xvfb

# Chromium browser (si no está instalado)
if ! command -v chromium-browser &> /dev/null; then
    echo "   Instalando Chromium..."
    sudo apt install -y chromium-browser
else
    echo "   ✅ Chromium ya instalado: $(chromium-browser --version)"
fi

# Dependencias para curl_cffi (compilación)
sudo apt install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libcurl4-openssl-dev

echo "   ✅ Dependencias del sistema instaladas"

# =============================================================================
# 2. Crear entorno virtual (opcional pero recomendado)
# =============================================================================
echo ""
echo "🐍 [2/5] Configurando Python..."
echo ""

VENV_DIR="$HOME/PartyFinder/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "   Creando entorno virtual en $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activar entorno virtual
source "$VENV_DIR/bin/activate"

# Actualizar pip
pip install --upgrade pip

echo "   ✅ Python configurado: $(python --version)"

# =============================================================================
# 3. Instalar dependencias de Python
# =============================================================================
echo ""
echo "📚 [3/5] Instalando dependencias de Python..."
echo ""

# Dependencias base
pip install nodriver beautifulsoup4

# Display virtual
pip install pyvirtualdisplay

# curl_cffi para scraping rápido
# NOTA: En ARM64 puede necesitar compilación
echo "   Instalando curl_cffi (puede tardar en ARM64)..."
pip install curl_cffi || {
    echo "   ⚠️  curl_cffi falló, instalando httpx como alternativa..."
    pip install httpx
}

# Firebase
pip install firebase-admin

# Flask para API (opcional)
pip install flask flask-cors

echo "   ✅ Dependencias de Python instaladas"

# =============================================================================
# 4. Verificar instalación
# =============================================================================
echo ""
echo "🔍 [4/5] Verificando instalación..."
echo ""

# Verificar Chromium
CHROMIUM_PATH="/usr/bin/chromium-browser"
if [ -f "$CHROMIUM_PATH" ]; then
    echo "   ✅ Chromium: $($CHROMIUM_PATH --version)"
else
    echo "   ❌ Chromium no encontrado en $CHROMIUM_PATH"
fi

# Verificar Xvfb
if command -v Xvfb &> /dev/null; then
    echo "   ✅ Xvfb instalado"
else
    echo "   ❌ Xvfb no encontrado"
fi

# Verificar Python packages
python -c "import nodriver; print('   ✅ nodriver:', nodriver.__version__)" 2>/dev/null || echo "   ❌ nodriver no instalado"
python -c "import pyvirtualdisplay; print('   ✅ pyvirtualdisplay instalado')" 2>/dev/null || echo "   ❌ pyvirtualdisplay no instalado"
python -c "from curl_cffi import requests; print('   ✅ curl_cffi instalado')" 2>/dev/null || echo "   ⚠️  curl_cffi no instalado (usando httpx)"
python -c "import httpx; print('   ✅ httpx instalado')" 2>/dev/null || true

# =============================================================================
# 5. Crear directorios necesarios
# =============================================================================
echo ""
echo "📁 [5/5] Creando directorios..."
echo ""

mkdir -p "$HOME/PartyFinder/backend/data"
echo "   ✅ Directorio data creado"

# =============================================================================
# Resumen
# =============================================================================
echo ""
echo "=============================================="
echo "✅ Setup completado!"
echo "=============================================="
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Activar entorno virtual:"
echo "   source $VENV_DIR/bin/activate"
echo ""
echo "2. Ir al directorio del backend:"
echo "   cd ~/PartyFinder/backend"
echo ""
echo "3. Obtener sesión de Cloudflare (Fase 1):"
echo "   python3 session_getter.py"
echo ""
echo "4. Ejecutar scraping rápido (Fase 2):"
echo "   python3 fast_scraper.py --full-scrape"
echo ""
echo "=============================================="
