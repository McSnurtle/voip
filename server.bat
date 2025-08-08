echo "DOING THE STUFF THE THING THE STUFF THINGS"

python -m venv venv

.\venv\Scripts\activate

pip install --upgrade -r requirements.txt

python src/server.py
