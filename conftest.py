import pytest
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
