. venv/bin/activate

pip install -r requirements.txt

cp /home/vadim/projects/webchat-frontend/webchat/core/config/config_example.py /home/vadim/projects/webchat-frontend/webchat/core/config/config.py
rm /home/vadim/projects/webchat-frontend/webchat/core/config/config_example.py 

alembic init alembic