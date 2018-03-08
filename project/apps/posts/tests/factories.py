import random

import factory
from django.contrib.auth import get_user_model
from faker import Factory as FakerFactory

from posts.models import Post
from users.tests.factories import UserFactory

faker = FakerFactory.create()

User = get_user_model()


class PostFactory(factory.django.DjangoModelFactory):
    """User Post factory."""

    title = factory.LazyAttribute(lambda x: faker.sentence())
    body = factory.LazyAttribute(lambda x: faker.text(random.randint(5, 500)))
    allow_comments = True
    status = Post.PUBLISHED
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
