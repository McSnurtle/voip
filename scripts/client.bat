@echo OFF

echo "Running voip client..."

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%\.."

call .\venv\Scripts\activate

python src/client.py

pause

