release: python app/manage.py makemigrations dxf && python app/manage.py migrate && python app/manage.py parse_dxf_files
web: gunicorn --chdir app zoningsite.wsgi --log-file -
