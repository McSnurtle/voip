#!bin/bash

echo "Running installation for https://github.com/McSnurtle/voip.git"

# installation is pwd-sensitive, so just to be sure:
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.." || exit 1

python -m venv venv

source ./venv/bin/activate

pip install --upgrade -r requirements.txt

read -p "Press enter to continue..."

