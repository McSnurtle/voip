@echo OFF

echo "Running installation of https://github.com/McSnurtle/voip.git"

python -m venv venv

call .\venv\Scripts\activate

pip install --upgrade -r requirements.txt
