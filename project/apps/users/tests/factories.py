import factory
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from faker import Factory as FakerFactory

faker = FakerFactory.create()
User = get_user_model()
USER_DEFAULT_PASSWORD = 'password'


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda x: faker.user_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    password = make_password(USER_DEFAULT_PASSWORD)

    class Meta:
        model = User

    @factory.post_generation
    def generate_token(self, create, value, **kwargs):
        if create:
            AccountEmailFactory(user=self, email=self.email)


class AccountEmailFactory(factory.django.DjangoModelFactory):
    verified = True
    primary = True

    class Meta:
        model = EmailAddress
