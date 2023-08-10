poetry run python3 manage.py migrate
poetry run python3 manage.py collectstatic --noinput

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    poetry run python3 manage.py createsuperuser --noinput
fi

poetry run python3 manage.py runserver 0.0.0.0:8000
