web: python manage.py migrate --noinput && python manage.py create_admin && gunicorn gespresence.wsgi --log-file - --bind 0.0.0.0:$PORT
