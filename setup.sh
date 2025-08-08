#!bin/bash

echo "Running installation for https://github.com/McSnurtle/voip.git"

python -m venv venv

source ./venv/bin/activate

pip install --upgrade -r requirements.txt
