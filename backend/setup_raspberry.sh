#!/bin/bash
# ============================================
# PartyFinder - Setup para Raspberry Pi
# ============================================
# Ejecuta este script en tu Raspberry Pi:
# chmod +x setup_raspberry.sh && ./setup_raspberry.sh

echo "=========================================="
echo "  PartyFinder - Instalando en Raspberry"
echo "=========================================="

# Actualizar sistema
echo "[1/6] Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
echo "[2/6] Instalando dependencias..."
sudo apt install -y chromium-browser xvfb python3-pip python3-venv git

# Crear directorio del proyecto
echo "[3/6] Configurando proyecto..."
mkdir -p ~/PartyFinder
cd ~/PartyFinder

# Crear entorno virtual
echo "[4/6] Creando entorno virtual Python..."
python3 -m venv venv
source venv/bin/activate

# Instalar paquetes Python
echo "[5/6] Instalando paquetes Python..."
pip install --upgrade pip
pip install nodriver beautifulsoup4 firebase-admin

# Crear script de ejecución
echo "[6/6] Creando scripts de ejecución..."

cat > run_scraper.sh << 'SCRIPT'
#!/bin/bash
# Script para ejecutar el scraper con display virtual
cd ~/PartyFinder/backend
source ~/PartyFinder/venv/bin/activate

# Usar display virtual para el navegador
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
XVFB_PID=$!
sleep 2

# Ejecutar scraper
python3 scraper.py --firebase

# Limpiar
kill $XVFB_PID 2>/dev/null
SCRIPT

chmod +x run_scraper.sh

echo ""
echo "=========================================="
echo "  Instalación completada!"
echo "=========================================="
echo ""
echo "PASOS SIGUIENTES:"
echo ""
echo "1. Copia los archivos del backend a ~/PartyFinder/backend/"
echo "   Desde tu PC Windows ejecuta:"
echo "   scp -r backend/* hugo@192.168.1.195:~/PartyFinder/backend/"
echo ""
echo "2. Copia serviceAccountKey.json:"
echo "   scp backend/serviceAccountKey.json hugo@192.168.1.195:~/PartyFinder/backend/"
echo ""
echo "3. Configura cron para ejecución automática:"
echo "   crontab -e"
echo "   Añade estas líneas:"
echo "   0 10 * * * ~/PartyFinder/run_scraper.sh >> ~/PartyFinder/scraper.log 2>&1"
echo "   0 16 * * * ~/PartyFinder/run_scraper.sh >> ~/PartyFinder/scraper.log 2>&1"
echo "   0 22 * * * ~/PartyFinder/run_scraper.sh >> ~/PartyFinder/scraper.log 2>&1"
echo ""
echo "4. Prueba manual:"
echo "   ~/PartyFinder/run_scraper.sh"
echo ""

