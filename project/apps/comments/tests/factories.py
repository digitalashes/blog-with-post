import random

import factory
from django.contrib.auth import get_user_model
from faker import Factory as FakerFactory

from comments.models import Comment
from posts.tests.factories import PostFactory
from users.tests.factories import UserFactory

faker = FakerFactory.create()

User = get_user_model()


class CommentFactory(factory.django.DjangoModelFactory):
    post = factory.SubFactory(PostFactory)
    body = factory.LazyAttribute(lambda x: faker.text(random.randint(5, 50)))
    user = factory.SubFactory(UserFactory)
    ip_address = factory.LazyAttribute(lambda x: faker.ipv4())

    class Meta:
        model = Comment
