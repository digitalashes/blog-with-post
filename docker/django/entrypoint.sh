#!/usr/bin/env bash
#migrate, create super and run server

./manage.py migrate --noinput
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | ./manage.py shell
./manage.py runserver 0.0.0.0:8000
