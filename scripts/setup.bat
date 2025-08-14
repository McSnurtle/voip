@echo OFF

echo "Running installation of https://github.com/McSnurtle/voip.git"

:: installation is pwd-sensitive, so just to be sure:
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%\.."

python -m venv venv

call .\venv\Scripts\activate

pip install --upgrade -r requirements.txt
