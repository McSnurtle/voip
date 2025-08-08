@echo OFF

echo "Running installation of https://github.com/McSnurtle/voip.git"

python -m venv venv

.\venv\Scripts\activate

pip install --upgrade -r requirements.txt

python src/client.py
