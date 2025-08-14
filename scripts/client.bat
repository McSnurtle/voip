@echo OFF

echo "Running voip client..."

call .\venv\Scripts/activate

python src/client.py
