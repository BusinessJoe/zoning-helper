release: python main.py
web: bin/start-nginx gunicorn -c python:config.gunicorn_conf --chdir app zoningsite.wsgi
