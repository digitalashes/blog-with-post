import os

from allauth.utils import build_absolute_uri
from common.validators import ImageSizeValidator
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import SoftDeletableModel
from users.managers import UserManager


def get_user_avatar_upload_path(instance, filename):
    return os.path.join(*('users', 'avatars', str(instance.pk), filename))


class User(PermissionsMixin, AbstractBaseUser, SoftDeletableModel):
    """
    Common user model.

    """

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('Username'),
        max_length=150, unique=True, validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),

    )
    email = models.EmailField(
        _('Email address'), unique=settings.UNIQUE_EMAIL,
        help_text=_('User Email Address.')
    )
    avatar = models.ImageField(
        _('Avatar'), validators=[ImageSizeValidator(width=250, height=250)],
        upload_to=get_user_avatar_upload_path, blank=True, null=True,
        help_text=_('User Avatar.')
    )
    password = models.CharField(
        _('Password'), max_length=128,
        help_text=_('User Password.')
    )
    first_name = models.CharField(
        _('First Name'), max_length=128,
        help_text=_('User First Name.')
    )
    last_name = models.CharField(
        _('Last Name'), max_length=128,
        help_text=_('User Last name.')
    )
    date_joined = models.DateTimeField(
        _('Member since'), auto_now_add=True
    )
    is_active = models.BooleanField(
        _('Active'), default=True
    )
    is_staff = models.BooleanField(
        _('Staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('first_name', 'last_name', 'email')
        indexes = (
            models.Index(fields=['username', 'email',
                                 'last_name', 'first_name']),
        )

    def __str__(self):
        return self.username

    @property
    def primary_email(self):
        return self.emailaddress_set.filter(primary=True).first()

    @property
    def is_email_verified(self):
        email = self.primary_email
        return email.verified if email else False

    @property
    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    @property
    def get_short_name(self):
        return self.first_name

    def set_random_password(self, commit=True, length=8):
        password = User.objects.make_random_password(length=length)
        self.set_password(password)
        if commit:
            self.save()
        return self, password

    @property
    def avatar_url(self):
        url = self.avatar.url if self.avatar else static('/images/default_user_avatar.png')
        return build_absolute_uri(None, url)
