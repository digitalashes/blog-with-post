import pytest
from django.core.management import call_command
from faker import Factory as FakerFactory
from pytest_factoryboy import register
from rest_auth.utils import jwt_encode
from rest_framework.test import APIClient, APIRequestFactory

from comments.tests.factories import CommentFactory
from posts.tests.factories import PostFactory
from users.tests.factories import UserFactory

register(UserFactory)
register(PostFactory)
register(CommentFactory)


def pytest_addoption(parser):
    parser.addoption('--repeat', action='store', help='Number of times to repeat each test')


def pytest_generate_tests(metafunc):
    if metafunc.config.option.repeat is not None:
        count = int(metafunc.config.option.repeat)

        # We're going to duplicate these tests by parametrizing them,
        # which requires that each test has a fixture to accept the parameter.
        # We can add a new fixture like so:
        metafunc.fixturenames.append('tmp_ct')

        # Now we parametrize. This is what happens when we do e.g.,
        # @pytest.mark.parametrize('tmp_ct', range(count))
        # def test_foo(): pass
        metafunc.parametrize('tmp_ct', range(count))


@pytest.fixture
def token(user):
    return jwt_encode(user)


@pytest.fixture(scope='session')
def faker():
    """Return faker instance"""

    return FakerFactory.create()


@pytest.fixture
def client():
    """Return API client"""

    return APIClient()


@pytest.fixture
def arf():
    """Return API request factory"""

    return APIRequestFactory()


@pytest.fixture
def fake_request(client, arf):
    """Return a request object with a session"""

    request = arf.get('/')
    setattr(request, 'session', client.session)
    return request


@pytest.fixture
def fake_request_with_user(fake_request, user):
    """Return a request object with a session and user"""

    setattr(fake_request, 'user', user)
    return fake_request


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Prepare common DB data.

    """

    with django_db_blocker.unblock():
        call_command('load_fake_data', call_from_test=True)
