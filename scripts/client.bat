@echo OFF

echo "Running voip client..."

call ./venv/bin/activate

python src/client.py
