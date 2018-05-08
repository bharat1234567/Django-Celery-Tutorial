#!/bin/bash
echo "$CURR_DIR"
python3 -m venv superenv
echo "virtual environment creating completed ...."
source superenv/bin/activate
if [[ "$VIRTUAL_ENV" != "" ]]
then
  echo "virutal environment is activated"
  pip install --upgrade pip
  pip install django #installs the latest version
  pip install celery #installs celery
  pip freeze > requirements.txt
  #echo "Installing requirements..."
  #pip install -r requirements.txt
  #echo "running migrations"
  #python manage.py migrate
  #echo "running server"
  #nohup python manage.py runserver 0.0.0.0:8000&
else
  echo "problem occurred in activating virtual environment"
fi
