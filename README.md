# Store

Just store.

### Start project
* `git clone https://repo.url` - clone repo
* `virtualenv venv --python=/path/to/python` - configure virtual environment
* `pip install -r requirements.txt` - install requirements
* `pip install -r requirements/local.txt` - install requirements for tests
* `createdb store` - create database
* `cp env.example .env` - crate you .env file and configure settings to .env
* `python manage.py migrate` - migrate database
* `python manage.py runserver` - run development server

