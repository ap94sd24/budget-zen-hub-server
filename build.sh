python3.9 -m venv venv
source venv/bin/activate
pip freeze > requirements.txt
pip uninstall -y -r requirements.txt
pip install -r requirements.txt