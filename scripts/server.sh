#!/bin/bash

echo "Running server script for voip..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.." || exit 1

source ./venv/bin/activate

python src/server.py

read -p "Press enter to continue..."

