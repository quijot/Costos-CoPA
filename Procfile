release: python manage.py migrate
worker: python manage.py qcluster
web: gunicorn copasfn.wsgi --log-file -
