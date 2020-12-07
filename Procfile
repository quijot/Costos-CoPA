release: python manage.py migrate
worker: python manage.py qcluster
web: gunicorn --workers 8 copasfn.wsgi --log-file -
