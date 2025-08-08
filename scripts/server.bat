@echo OFF

echo "Running server script for voip..."

call ./venv/Scripts/activate

python src/server.py
