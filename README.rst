==============================
django_project_heroku_template
==============================

*A minimal Django project template ready for heroku*, using

- Python >=3.6 (because we love ``f-strings``)
- Django >=3.0,<4

Usage
-----

Just clone this repo and follow the instructions below...

Step by step
************

0. Clone this repo:

::

    git clone https://github.com/quijot/django_project_heroku_template.git

1. Enter the project directory, create and activate a virtualenv with your favorite method and install requirements:

::

    cd django_project_heroku_template
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

2. Install `Heroku CLI <https://devcenter.heroku.com/articles/heroku-cli>`_

3. Choose a proper ``<<herokuapp_name>>`` (without ``<<`` and ``>>``, of course)

4. Get a valid ``SECRET_KEY`` value here: `Django Secret Key Generator <https://www.miniwebtool.com/django-secret-key-generator/>`_

5. And then...

::

    heroku create <<herokuapp_name>>
    heroku config:set DJANGO_HEROKUAPP_NAME='<<herokuapp_name>>'
    heroku config:set DJANGO_SECRET_KEY='<<your-secret-key>>'
    heroku config:set DJANGO_DEBUG='False'
    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser

... and that's it, your Django project is up! Now start adding it apps and stuff.

To test it go to https://<<herokuapp_name>>.herokuapp.com/admin. Without */admin* it will fail because we set ``DEBUG=False``.


Future commits & Database Migrations
------------------------------------

Make modifications through ``commit`` and ``push`` to your git repository.

Once you add an app with its database migrations, you will need to run ``makemigrations`` remotely. So, migrations need to be checked into the git repository or generated in the `release phase <https://devcenter.heroku.com/articles/release-phase#specifying-release-phase-tasks>`_.

The easiest way:

- check your migrations dir into the git repo
- add ``release: python manage.py migrate`` as the first line in your Procfile

Please, take a look at this article: https://help.heroku.com/GDQ74SU2/django-migrations where all of this is more clearly explained.
