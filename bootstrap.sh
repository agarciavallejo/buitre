#!/bin/bash
export FLASK_ENV=development
source $(pipenv --venv)/bin/activate
gunicorn -b localhost:8000 -w 4 buitre:app
