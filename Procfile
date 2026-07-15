web: python manage.py migrate --noinput && python manage.py createsuperuser --noinput --username admin --email admin@admin.com || true && gunicorn gespresence.wsgi --log-file - --bind 0.0.0.0:$PORT
