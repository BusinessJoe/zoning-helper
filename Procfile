release: python app/manage.py migrate
web: gunicorn --chdir app zoningsite.wsgi --log-file -
