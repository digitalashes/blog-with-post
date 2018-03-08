#!/usr/bin/env bash
#migrate, create super and run server

./manage.py migrate --noinput
./manage.py runserver 0.0.0.0:8000
