@echo off
title DevOps ETL & Outreach Pipeline - Autopilot
color 0A

echo ===================================================
echo   INICIANDO AUTOMATIZACION DIARIA DEL PIPELINE ETL
echo ===================================================
echo.
echo Ejecutando scripts de ingestion, validacion y sincronizacion...
echo.

:: Cambiar al directorio donde esta el batch file (raiz del proyecto)
cd /d "%~dp0"

:: Ejecutar el script maestro de Python
python 03-SCRIPTS\run_daily.py

if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo ===================================================
    echo   ERROR EN LA EJECUCION DEL PIPELINE
    echo ===================================================
    echo Por favor, revisa los registros en 05-LOGS.
    pause
)
