@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\github\push_to_existing_repo.ps1" -ProjectPath "%~dp0"
pause
