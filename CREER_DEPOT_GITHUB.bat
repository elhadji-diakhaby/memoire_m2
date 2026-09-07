@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\github\create_repo_and_push.ps1" -ProjectPath "%~dp0"
pause
