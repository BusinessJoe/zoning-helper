release: python zoning-helper/app/manage.py migrate
web: gunicorn --chdir zoning-helper/app zoningsite.wsgi --log-file -
