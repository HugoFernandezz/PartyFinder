@echo off
echo ==========================================
echo   PartyFinder - Desplegar a Raspberry Pi
echo ==========================================
echo.

set /p RASPI_USER=Usuario de la Raspberry [hugo]: 
if "%RASPI_USER%"=="" set RASPI_USER=hugo

set /p RASPI_IP=IP de la Raspberry [192.168.1.195]: 
if "%RASPI_IP%"=="" set RASPI_IP=192.168.1.195

echo.
echo Conectando a %RASPI_USER%@%RASPI_IP%...
echo.

echo [1/4] Creando directorios en Raspberry...
ssh %RASPI_USER%@%RASPI_IP% "mkdir -p ~/PartyFinder/backend/data"

echo [2/4] Copiando archivos Python...
scp scraper.py %RASPI_USER%@%RASPI_IP%:~/PartyFinder/backend/
scp firebase_config.py %RASPI_USER%@%RASPI_IP%:~/PartyFinder/backend/
scp requirements.txt %RASPI_USER%@%RASPI_IP%:~/PartyFinder/backend/

echo [3/4] Copiando credenciales de Firebase...
scp serviceAccountKey.json %RASPI_USER%@%RASPI_IP%:~/PartyFinder/backend/

echo [4/4] Copiando script de instalacion...
scp setup_raspberry.sh %RASPI_USER%@%RASPI_IP%:~/PartyFinder/

echo.
echo ==========================================
echo   Archivos copiados!
echo ==========================================
echo.
echo SIGUIENTE PASO:
echo Conectate a la Raspberry y ejecuta:
echo   ssh %RASPI_USER%@%RASPI_IP%
echo   cd ~/PartyFinder
echo   chmod +x setup_raspberry.sh
echo   ./setup_raspberry.sh
echo.
pause

