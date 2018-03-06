from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from rest_framework.response import Response

User = get_user_model()


class AccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        url = settings.WEB_URLS['email_confirm'].format(
            root_url=settings.CLIENT_DOMAIN,
            key=emailconfirmation.key)
        return url

    def format_email_subject(self, subject):
        prefix = settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            site = get_current_site(self.request)
            prefix = f'[{site.name}] '
        return f'[{prefix}] {force_text(subject)}'

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        super().send_confirmation_mail(request, emailconfirmation, False)

    def confirm_email(self, request, email_address):
        """
        Marks the email address as confirmed and primary on the db

        """

        email_address.verified = True
        email_address.set_as_primary(conditional=False)
        email_address.save()

    def respond_email_verification_sent(self, request, user):
        return Response({'detail': _('Email was successfully confirmed.')})
