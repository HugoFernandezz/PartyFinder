@echo off
echo 🧹 Limpiando cache completa de PartyFinder...
echo.

echo 🔄 Deteniendo procesos de Expo y Node...
taskkill /f /im node.exe 2>nul
taskkill /f /im expo.exe 2>nul
timeout /t 2 /nobreak >nul

echo 🗑️ Limpiando cache de npm...
npm cache clean --force

echo 🗑️ Limpiando cache de Expo...
if exist "%USERPROFILE%\.expo" (
    rmdir /s /q "%USERPROFILE%\.expo\cache" 2>nul
    echo Cache de Expo eliminada
)

echo 🗑️ Limpiando cache de Metro...
if exist "%APPDATA%\Metro" (
    rmdir /s /q "%APPDATA%\Metro" 2>nul
    echo Cache de Metro eliminada
)

echo 🗑️ Limpiando directorios temporales del proyecto...
if exist ".expo" (
    rmdir /s /q ".expo" 2>nul
    echo Directorio .expo eliminado
)

if exist "node_modules\.cache" (
    rmdir /s /q "node_modules\.cache" 2>nul
    echo Cache de node_modules eliminada
)

echo 🗑️ Limpiando archivos de cache del servidor...
if exist "cached_data.json" (
    del "cached_data.json" 2>nul
    echo cached_data.json eliminado
)

if exist "fresh_data.json" (
    del "fresh_data.json" 2>nul
    echo fresh_data.json eliminado
)

if exist "backup_data.json" (
    del "backup_data.json" 2>nul
    echo backup_data.json eliminado
)

echo 🔄 Reinstalando dependencias...
rmdir /s /q node_modules 2>nul
del package-lock.json 2>nul
npm install

echo.
echo ✅ Cache limpiada completamente!
echo 🚀 Ahora puedes ejecutar: npm start
echo.
pause 