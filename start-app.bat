@echo off
title Iniciar PartyFinder App

echo =======================================================
echo  Iniciando la aplicacion PartyFinder para Expo Go
echo =======================================================
echo.
echo Este script instalara las dependencias (si es necesario)
echo y luego iniciara el servidor de desarrollo de Expo.
echo.
echo Cuando veas un codigo QR, escanealo con la aplicacion
echo Expo Go en tu iPhone para abrir la app.
echo.

echo Instalando dependencias...
call npm install

echo.
echo Iniciando Expo...
call npx expo start

pause 