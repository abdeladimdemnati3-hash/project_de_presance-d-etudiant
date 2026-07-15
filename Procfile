web: python manage.py migrate --noinput && python manage.py create_admin && python manage.py seed_db && gunicorn gespresence.wsgi --log-file - --bind 0.0.0.0:$PORT
