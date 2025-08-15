@echo OFF

echo "Running server script for voip..."

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%\.."

call .\venv\Scripts\activate

python src/server.py

pause

