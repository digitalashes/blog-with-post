import re

from django.conf import settings
from django.contrib.sites.models import Site


def find_values_in_mail_body(mail_body, web_url_key):
    """
    Search in given text a web link entity and parse named placeholders.

    Pattern example:
    {
        web_url_key: '{root_url}/profile/email-confirm/?key={key}'
    }

    Response example:
    {
        'root_url': 'example.com',
        'uid': 'Mjk',
        'token': '4q9-95768eb80cf66490b6b2'
    }

    """

    pattern = settings.WEB_URLS[web_url_key]
    location = f'{settings.CLIENT_DOMAIN}'

    try:
        url = re.findall(r'{}\S+'.format(location), mail_body)[0].strip('"')
    except IndexError:  # pragma: no cover
        return {}

    # Convert to named regex pattern:
    #   '(?P<root_url>.*?)/profile/password-reset/?uid=(?P<uid>.*?)'
    re_pattern = re.sub(
        r'{(\w+)}', r'(?P<\1>.+)',
        pattern.replace('?', r'\?'))

    try:
        match = re.match(re_pattern, url)
        return match.groupdict()
    except AttributeError:  # pragma: no cover
        return {}
