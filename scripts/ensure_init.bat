@echo off
REM Скрипт для автоматического создания __init__.py файлов
REM Запускается из папки scripts, но работает с корнем проекта

cd /d "%~dp0\.."
python scripts\ensure_init_files.py
pause
