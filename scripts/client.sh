#!/bin/bash

echo "Running voip client..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.." || exit 1

source ./venv/bin/activate

python src/client.py
