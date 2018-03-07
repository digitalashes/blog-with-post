import os

from allauth.utils import build_absolute_uri
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import (
    TimeStampedModel,
    StatusModel,
)

User = get_user_model()


def get_blog_image_upload_path(instance, filename):
    return os.path.join(*('posts', 'images', str(instance.pk), filename))


class Post(TimeStampedModel, StatusModel):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS = Choices(
        ('draft', DRAFT, _(DRAFT.capitalize())),
        ('published', PUBLISHED, _(PUBLISHED.capitalize())),
    )

    title = models.CharField(
        _('Title'), max_length=256,
        help_text=_('Post Title.')
    )
    body = MarkupField(
        _('Body'), max_length=2048,
        default_markup_type='markdown',
        help_text=_('Post Body.')
    )
    image = models.ImageField(
        _('Image'), width_field=1024, height_field=1024,
        upload_to=get_blog_image_upload_path, blank=True, null=True,
        help_text=_('Post Head Image.')
    )
    author = models.ForeignKey(
        to=User, on_delete=CASCADE,
        verbose_name=_('Author'), related_name='posts',
        help_text=_('Post Author.')
    )
    allow_comments = models.BooleanField(
        _('Allow comments'), default=True,
        help_text=_('Can other user add comments?')
    )
    status = StatusField(
        _('Status'), default=PUBLISHED,
        help_text=_('Post Status.')
    )

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-created',)
        indexes = (
            models.Index(fields=['title', 'body']),
        )

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return build_absolute_uri(None, self.image.url) if self.image else None

    @property
    def is_draft(self):
        return self.status == self.DRAFT

    @property
    def is_published(self):
        return self.status == self.PUBLISHED
