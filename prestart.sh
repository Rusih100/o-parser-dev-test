poetry run python3 manage.py migrate
poetry run python3 manage.py collectstatic --noinput

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python run python3 manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

poetry run python3 manage.py runserver 0.0.0.0:8000
