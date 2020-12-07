release: python manage.py migrate
worker: python manage.py qcluster
web: bin/start-pgbouncer gunicorn copasfn.wsgi --log-file -
