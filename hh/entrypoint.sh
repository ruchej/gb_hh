#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres $POSTGRES_HOST:$POSTGRES_PORT..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run as "docker-compose exec web python manage.py flush --no-input"
# python manage.py flush --no-input

# Run as "docker-compose exec web python manage.py migrate"
# python manage.py migrate

exec "$@"
