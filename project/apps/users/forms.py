from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetForm(BasePasswordResetForm):
    def save(self, domain_override=None,
             subject_template_name='account/email/password_reset_subject.txt',
             email_template_name='account/email/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the user.

        """

        email = self.cleaned_data.get('email')
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            url = settings.WEB_URLS['reset_password'].format(
                root_url=settings.CLIENT_DOMAIN,
                uid=urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                token=token_generator.make_token(user))
            context = {
                'url': url,
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'user': user,
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )
