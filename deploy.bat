@echo off
echo.
echo =========================================
echo  🚀 SCRIPT DE DESPLIEGUE DE PARTYFINDER 🚀
echo =========================================
echo.
echo Este script te guiará para compilar tu aplicación para Android usando EAS.
echo.
echo Requisitos:
echo 1. Tener una cuenta de Expo (https://expo.dev)
echo 2. Haber instalado EAS CLI: npm install -g eas-cli
echo 3. Haber iniciado sesion: eas login
echo.
pause

:menu
cls
echo.
echo Selecciona una opcion de despliegue:
echo.
echo   1. Compilar para Android (genera un .apk para instalar)
echo   2. Publicar una actualizacion (OTA Update)
echo   3. Salir
echo.
set /p choice="Introduce tu opcion (1-3): "

if "%choice%"=="1" goto build_android
if "%choice%"=="2" goto publish_update
if "%choice%"=="3" exit /b

echo Opcion no valida.
pause
goto menu

:build_android
cls
echo.
echo =================================
echo  COMPILANDO APP PARA ANDROID 📱
echo =================================
echo.
echo Se iniciara el proceso de compilacion de EAS Build.
echo Se te pedira que confirmes la cuenta de Expo y el proyecto.
echo.
echo La compilacion puede tardar entre 15-30 minutos en los servidores de Expo.
echo Recibiras un enlace para seguir el progreso y descargar el .apk cuando este listo.
echo.
pause

eas build --platform android --profile preview

echo.
echo ✅ Proceso de compilacion iniciado.
echo.
pause
goto menu

:publish_update
cls
echo.
echo ===================================
echo  PUBLICANDO ACTUALIZACION (OTA) 🔄
echo ===================================
echo.
echo Esto publicara los cambios de tu codigo (JavaScript/TypeScript)
echo sin necesidad de crear un nuevo .apk. Los usuarios recibiran
echo la actualizacion la proxima vez que abran la app.
echo.
pause

eas update

echo.
echo ✅ Actualizacion publicada exitosamente.
echo.
pause
goto menu 