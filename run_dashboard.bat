@echo off
title Clothing Scraper - Full Pipeline & Dashboard
cd /d "%~dp0"

echo ===================================================
echo   Step 1: Running Scraper, Cleaner, and Analysis...
echo ===================================================
py -3.13 main.py

echo.
echo ===================================================
echo   Step 2: Launching Web Dashboard...
echo ===================================================

:: Open the default browser to the web app
start http://127.0.0.1:5000

:: Start the Flask web server
py -3.13 app.py

pause