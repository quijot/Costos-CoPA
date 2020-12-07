release: python manage.py migrate
worker: python manage.py qcluster
web: gunicorn --workers 3 copasfn.wsgi --log-file -
