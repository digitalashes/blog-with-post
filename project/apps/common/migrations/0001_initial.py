# Generated by Django 2.0.3 on 2018-03-06 22:03

from django.conf import settings
from django.core.management import call_command
from django.db import migrations


def load_fake_data(*args, **kwargs):
    call_command('load_fake_data')


def delete_fake_data(*args, **kwargs):
    call_command('delete_fake_data')


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('users', '0002_auto_20180306_1907'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(load_fake_data, delete_fake_data)
    ]
