release: python manage.py migrate
worker: bin/start-pgbouncer python manage.py qcluster
web: bin/start-pgbouncer gunicorn copasfn.wsgi --log-file -
