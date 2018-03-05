from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_auth.serializers import (
    LoginSerializer as LoginSerializerBase,
    PasswordResetSerializer as PasswordResetSerializerBase,
)
from rest_framework import serializers

from users.forms import PasswordResetForm

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'avatar')

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.')
                )
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password', ''),
        }

    def custom_signup(self, request, user):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class VerifyEmailResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
                                   help_text=_('Email, which was specified during registration'))

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and not email_address_exists(email):
            raise serializers.ValidationError(_('A user with this e-mail address is not registered.'))
        return email

    def save(self, request):
        email_address = EmailAddress.objects.get(email__iexact=self.validated_data.get('email'))
        email_address.send_confirmation(request)


class LoginSerializer(LoginSerializerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('email')
        self.fields['username'].required = True
        self.fields['username'].help_text = _('Username.')
        self.fields['password'].help_text = _('Password.')


class PasswordResetSerializer(PasswordResetSerializerBase):
    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        tpl = 'account/email/%s'
        return {
            'subject_template_name': tpl % 'password_reset_subject.txt',
            'email_template_name': tpl % 'password_reset_message.txt',
            'html_email_template_name': tpl % 'password_reset_message.html',
            'extra_email_context': {
                'request': self.context.get('request'),
            }
        }


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar_url')
        read_only_fields = ('id', 'email', 'avatar_url')
