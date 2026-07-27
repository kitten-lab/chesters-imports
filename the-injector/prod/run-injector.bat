@echo off
cd /d "%~dp0box_sys"
start "THE INJECTOR" py -3.12 server.py
timeout /t 1 /nobreak >nul
start "" "http://127.0.0.1:42961/"
