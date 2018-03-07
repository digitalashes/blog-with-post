from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load Fake Data'

    def handle(self, *args, **options):
        call_command('loaddata', 'users')
        call_command('loaddata', 'posts')
        call_command('loaddata', 'comments')
