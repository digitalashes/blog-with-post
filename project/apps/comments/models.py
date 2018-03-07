from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from posts.models import Post

User = get_user_model()


class Comment(TimeStampedModel):
    post = models.ForeignKey(
        to=Post, on_delete=CASCADE,
        verbose_name=_('Post'), related_name='comments',
        help_text=_('Post.')
    )
    body = models.TextField(
        _('Comment'), max_length=1024,
        help_text=_('Comment Body.')
    )
    user = models.ForeignKey(
        to=User, on_delete=CASCADE,
        verbose_name=_('User'), related_name='comments',
        help_text=_('Comment Author.')
    )
    ip_address = models.GenericIPAddressField(
        _('Ip Address'), default='0.0.0.0',
        help_text=_('Comment Author IP Address.')
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ('-created', 'user')
        indexes = (
            models.Index(fields=['post', 'body', 'user', 'ip_address']),
        )

    def __str__(self):
        return f'Comment {self.user} for post {self.post}'
