from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Delete Fake Data'

    def handle(self, *args, **options):
        from users.models import User
        users_ids = tuple(User.objects.only('id').exclude(
            is_superuser=True
        ).values_list('id', flat=True))
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM comments_comment WHERE comments_comment.user_id IN %s """,
                           [users_ids])
            cursor.execute("""DELETE FROM posts_post WHERE posts_post.author_id IN %s """,
                           [users_ids])
            cursor.execute("""DELETE FROM account_emailaddress WHERE account_emailaddress.user_id IN %s """,
                           [users_ids])
            cursor.execute("""DELETE FROM users_user WHERE users_user.id IN %s """,
                           [users_ids])
