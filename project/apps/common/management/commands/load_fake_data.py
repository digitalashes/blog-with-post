from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load Fake Data'

    def handle(self, *args, **options):
        Site.objects.filter(id=1).update(domain='localhost:8000')
        call_command('loaddata', 'users')
        call_command('loaddata', 'posts')
        call_command('loaddata', 'comments')
