release: python manage.py makemigrations && python manage.py migrate
web: gunicorn innoevent.wsgi:application