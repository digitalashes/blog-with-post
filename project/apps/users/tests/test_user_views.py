import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from freezegun import freeze_time
from rest_auth.utils import jwt_encode
from rest_framework import status

from users.serializers import UserDetailsSerializer
from users.tests.factories import USER_DEFAULT_PASSWORD

User = get_user_model()


# @pytest.mark.django_db
class UserViewsTestSuite:

    @classmethod
    def setup_class(cls):
        cls.registration_url = reverse_lazy('api:auth:registration')

        cls.login_url = reverse_lazy('api:auth:login')
        cls.logout_url = reverse_lazy('api:auth:logout')

        cls.token_refresh_url = reverse_lazy('api:auth:token_refresh')
        cls.token_verify_url = reverse_lazy('api:auth:token_verify')

        cls.password_change_url = reverse_lazy('api:auth:password_change')
        cls.password_reset_url = reverse_lazy('api:auth:password_reset')
        cls.password_reset_confirm_url = reverse_lazy('api:auth:password_reset_confirm')

        cls.verify_email_url = reverse_lazy('api:auth:verify_email')
        cls.verify_email_reset_url = reverse_lazy('api:auth:verify_email_reset')

        cls.email_field = 'email'
        cls.password_field = 'password'
        cls.first_name_field = 'first_name'
        cls.last_name_field = 'last_name'
        cls.detail_field = 'detail'
        cls.non_field_errors_field = 'non_field_errors'
        cls.token_field = 'token'
        cls.user_field = 'user'
        cls.key_field = 'key'
        cls.old_password_field = 'old_password'
        cls.new_password1_field = 'new_password1'
        cls.new_password2_field = 'new_password2'
        cls.uid_field = 'uid'

    @classmethod
    def teardown_class(cls):
        pass

    def test_hello(self):
        assert 1

    # @freeze_time()
    # def test_registration_view(self, client, user, faker, mailoutbox):
    #     for http_method in ('get', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.registration_url)
    #         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #
    #     assert User.objects.count() == 1
    #     assert User.objects.first() == user
    #     payloads = {}
    #
    #     response = client.post(self.registration_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #
    #     assert len(response.data['codes']) == 5
    #     assert self.email_field in response.data
    #     assert self.password_field in response.data
    #     assert self.first_name_field in response.data
    #     assert self.last_name_field in response.data
    #     assert self.phone_number_filed in response.data
    #
    #     assert response.data.get(self.email_field) == ['This field is required.']
    #     assert response.data.get(self.password_field) == ['This field is required.']
    #     assert response.data.get(self.first_name_field) == ['This field is required.']
    #     assert response.data.get(self.last_name_field) == ['This field is required.']
    #     assert response.data.get(self.phone_number_filed) == ['This field is required.']
    #
    #     assert User.objects.count() == 1
    #     assert User.objects.first() == user
    #
    #     payloads.update({
    #         self.email_field: faker.word(),
    #         self.password_field: USER_DEFAULT_PASSWORD,
    #         self.first_name_field: faker.first_name() * 30,
    #         self.last_name_field: faker.last_name() * 30,
    #         self.phone_number_filed: faker.phone_number(),
    #     })
    #     response = client.post(self.registration_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert len(response.data['codes']) == 4
    #     assert self.email_field in response.data
    #     assert self.first_name_field in response.data
    #     assert self.last_name_field in response.data
    #     assert self.phone_number_filed in response.data
    #     assert response.data.get(self.email_field) == ['Enter a valid email address.']
    #     assert response.data.get(self.first_name_field) == ['Ensure this field has no more than 30 characters.']
    #     assert response.data.get(self.last_name_field) == ['Ensure this field has no more than 30 characters.']
    #     assert response.data.get(self.phone_number_filed) == ['Enter a valid phone number.']
    #     assert User.objects.count() == 1
    #
    #     payloads.update({
    #         self.email_field: user.email,
    #         self.password_field: USER_DEFAULT_PASSWORD,
    #         self.first_name_field: faker.first_name(),
    #         self.last_name_field: faker.last_name(),
    #         self.phone_number_filed: self.valid_phone_number,
    #     })
    #     response = client.post(self.registration_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert len(response.data['codes']) == 1
    #     assert self.email_field in response.data
    #     assert response.data.get(self.email_field) == ['User with this Email address already exists.']
    #     assert User.objects.count() == 1
    #     assert len(mailoutbox) == 0
    #
    #     email = faker.email()
    #     payloads.update({
    #         self.email_field: email,
    #         self.password_field: USER_DEFAULT_PASSWORD,
    #         self.first_name_field: faker.first_name(),
    #         self.last_name_field: faker.last_name(),
    #         self.phone_number_filed: self.valid_phone_number,
    #     })
    #     response = client.post(self.registration_url, data=payloads)
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert len(mailoutbox) == 1
    #     assert User.objects.count() == 2
    #     assert User.objects.filter(email=email).exists()
    #     new_user = User.objects.get(email=email)
    #     assert len(response.data) == 2
    #     assert self.token_field in response.data
    #     assert self.user_field in response.data
    #     assert response.data.get(self.token_field) == jwt_encode(new_user)
    #     assert response.data.get(self.user_field) == UserDetailsSerializer(new_user).data
    #     assert new_user.is_active
    #     assert new_user.is_owner
    #     assert not new_user.is_admin
    #     assert not new_user.is_user
    #
    # def test_login_view(self, client, user, faker):
    #     for http_method in ('get', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.registration_url)
    #         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #
    #     payloads = {}
    #     response = client.post(self.login_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.email_field in response.data
    #     assert self.password_field in response.data
    #
    #     assert response.data.get(self.email_field) == ['This field is required.']
    #     assert response.data.get(self.password_field) == ['This field is required.']
    #
    #     payloads = {
    #         self.email_field: faker.word(),
    #         self.password_field: faker.word(),
    #     }
    #     response = client.post(self.login_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.non_field_errors_field in response.data
    #     assert response.data.get(self.non_field_errors_field) == ['Unable to log in with provided credentials.']
    #
    #     payloads = {
    #         self.email_field: user.email,
    #         self.password_field: USER_DEFAULT_PASSWORD,
    #     }
    #     response = client.post(self.login_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 2
    #     assert self.token_field in response.data
    #     assert response.data.get(self.token_field) == jwt_encode(user)
    #     assert response.data.get(self.user_field) == UserDetailsSerializer(user).data
    #
    # def test_logout_view(self, client):
    #     for http_method in ('get', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.registration_url)
    #         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #
    #     response = client.post(self.logout_url)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 1
    #     assert self.detail_field in response.data
    #     assert response.data.get(self.detail_field) == 'Successfully logged out.'
    #
    # def test_refresh_token(self, client, user, faker):
    #     freezer = freeze_time('2018-01-01 00:00:00')
    #     payloads = {}
    #     response = client.post(self.token_refresh_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.token_field in response.data
    #     assert response.data.get(self.token_field) == ['This field is required.']
    #
    #     payloads = {
    #         self.token_field: faker.uuid4()
    #     }
    #     response = client.post(self.token_refresh_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert len(response.data) == 1
    #     assert self.non_field_errors_field in response.data
    #     assert response.data.get(self.non_field_errors_field) == ['Error decoding signature.']
    #
    #     freezer.start()
    #     valid_token = jwt_encode(user)
    #     payloads = {
    #         self.token_field: valid_token
    #     }
    #     response = client.post(self.token_refresh_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 2
    #     assert self.token_field in response.data
    #     assert self.user_field in response.data
    #
    #     assert response.data.get(self.token_field) == valid_token
    #     assert response.data.get(self.user_field) == UserDetailsSerializer(user).data
    #     freezer.stop()
    #
    #     response = client.post(self.token_refresh_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.non_field_errors_field in response.data
    #     assert response.data.get(self.non_field_errors_field) == ['Signature has expired.']
    #
    # def test_token_verify(self, client, user, faker):
    #     freezer = freeze_time('2018-01-01 00:00:00')
    #     payloads = {}
    #     response = client.post(self.token_verify_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.token_field in response.data
    #     assert response.data.get(self.token_field) == ['This field is required.']
    #
    #     payloads = {
    #         self.token_field: faker.uuid4()
    #     }
    #     response = client.post(self.token_verify_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.non_field_errors_field in response.data
    #     assert response.data.get(self.non_field_errors_field) == ['Error decoding signature.']
    #
    #     freezer.start()
    #     valid_token = jwt_encode(user)
    #     payloads = {
    #         self.token_field: valid_token
    #     }
    #     response = client.post(self.token_verify_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 2
    #     assert response.data.get(self.token_field) == valid_token
    #     assert response.data.get(self.user_field) == UserDetailsSerializer(user).data
    #     freezer.stop()
    #
    #     response = client.post(self.token_verify_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.non_field_errors_field in response.data
    #     assert response.data.get(self.non_field_errors_field) == ['Signature has expired.']
    #
    # def test_verify_email_reset(self, client, user, mailoutbox, faker):
    #     for http_method in ('get', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.verify_email_reset_url)
    #         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #
    #     payloads = {}
    #     response = client.post(self.verify_email_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.email_field in response.data
    #     assert response.data.get(self.email_field) == ['This field is required.']
    #
    #     payloads.update({
    #         self.email_field: faker.word()
    #     })
    #     response = client.post(self.verify_email_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.email_field in response.data
    #     assert response.data.get(self.email_field) == ['Enter a valid email address.']
    #
    #     payloads.update({
    #         self.email_field: faker.email()
    #     })
    #     response = client.post(self.verify_email_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.email_field in response.data
    #     assert response.data.get(self.email_field) == ['A user with this e-mail address is not registered.']
    #
    #     assert len(mailoutbox) == 0
    #     payloads.update({
    #         self.email_field: user.email
    #     })
    #     response = client.post(self.verify_email_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert self.detail_field in response.data
    #     assert response.data.get(self.detail_field) == 'Verification e-mail sent.'
    #     assert len(mailoutbox) == 1
    #
    #     response = client.post(self.verify_email_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert len(mailoutbox) == 2
    #
    # def test_verify_email(self, client, user, mailoutbox, faker):
    #     for http_method in ('get', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.verify_email_url)
    #         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #
    #     email = user.get_primary_email()
    #     email.verified = False
    #     email.save()
    #
    #     assert not user.get_primary_email().verified
    #
    #     payloads = {
    #         self.email_field: user.email,
    #     }
    #     response = client.post(self.verify_email_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert len(mailoutbox) == 1
    #     # key = find_values_in_mail_body(mailoutbox[0].body, 'email_confirm').get('key')
    #     payloads.clear()
    #
    #     payloads.update({
    #         self.key_field: faker.uuid4(),
    #     })
    #     response = client.post(self.verify_email_url, data=payloads)
    #     assert response.status_code == status.HTTP_404_NOT_FOUND
    #     assert len(response.data) == 1
    #     assert self.detail_field in response.data
    #     assert response.data.get(self.detail_field) == 'Not found.'
    #
    #     payloads.update({
    #         # self.key_field: key,
    #     })
    #     response = client.post(self.verify_email_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 2
    #     assert self.token_field in response.data
    #     assert self.user_field in response.data
    #
    #     assert response.data.get(self.token_field) == jwt_encode(user)
    #     assert response.data.get(self.user_field) == UserDetailsSerializer(user).data
    #
    #     assert user.get_primary_email().verified
    #
    # def test_password_change(self, client, user, token, faker):
    #     for http_method in ('get', 'post', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.password_change_url)
    #         assert response.status_code == status.HTTP_401_UNAUTHORIZED
    #
    #     client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
    #
    #     for http_method in ('get', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.password_change_url)
    #         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #
    #     payloads = {}
    #
    #     response = client.post(self.password_change_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.old_password_field in response.data
    #     assert self.new_password1_field in response.data
    #     assert self.new_password2_field in response.data
    #     assert response.data.get(self.old_password_field) == ['This field is required.']
    #     assert response.data.get(self.new_password1_field) == ['This field is required.']
    #     assert response.data.get(self.new_password2_field) == ['This field is required.']
    #
    #     payloads.update({
    #         self.old_password_field: faker.password(),
    #         self.new_password1_field: faker.password(),
    #         self.new_password2_field: faker.password(),
    #     })
    #     response = client.post(self.password_change_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.old_password_field in response.data
    #     assert response.data.get(self.old_password_field) == ['Invalid password']
    #
    #     payloads.update({
    #         self.old_password_field: USER_DEFAULT_PASSWORD,
    #     })
    #     response = client.post(self.password_change_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.new_password2_field in response.data
    #     assert response.data.get(self.new_password2_field) == ["The two password fields didn't match."]
    #
    #     new_password = faker.password()
    #     payloads.update({
    #         self.new_password1_field: new_password,
    #         self.new_password2_field: new_password,
    #     })
    #     response = client.post(self.password_change_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 1
    #     assert self.detail_field in response.data
    #     assert response.data.get(self.detail_field) == 'New password has been saved.'
    #
    #     payloads.clear()
    #     payloads.update({
    #         self.email_field: user.email,
    #         self.password_field: USER_DEFAULT_PASSWORD,
    #     })
    #     response = client.post(self.login_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.non_field_errors_field in response.data
    #     assert response.data.get(self.non_field_errors_field) == ['Unable to log in with provided credentials.']
    #
    #     payloads.update({
    #         self.password_field: new_password,
    #     })
    #     response = client.post(self.login_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert self.token_field in response.data
    #     assert self.user_field in response.data
    #
    # def test_password_reset(self, client, user, faker, mailoutbox):
    #     for http_method in ('get', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.password_reset_url)
    #         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #
    #     payloads = {
    #         self.email_field: faker.email(),
    #     }
    #     response = client.post(self.password_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.email_field in response.data
    #     assert response.data.get(self.email_field) == ['A user with this e-mail address is not registered.']
    #
    #     assert len(mailoutbox) == 0
    #     payloads.update({
    #         self.email_field: user.email,
    #     })
    #     response = client.post(self.password_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 1
    #     assert self.detail_field in response.data
    #     assert response.data.get(self.detail_field) == 'Password reset e-mail has been sent.'
    #     assert len(mailoutbox) == 1
    #
    # def test_password_reset_confirm(self, client, user, faker, mailoutbox):
    #     for http_method in ('get', 'put', 'patch', 'delete'):
    #         response = getattr(client, http_method)(self.password_reset_confirm_url)
    #         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    #
    #     payloads = {}
    #     response = client.post(self.password_reset_confirm_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert len(response.data['codes']) == 4
    #     assert self.new_password1_field in response.data
    #     assert self.new_password2_field in response.data
    #     assert self.uid_field in response.data
    #     assert self.token_field in response.data
    #
    #     assert response.data.get(self.new_password1_field) == ['This field is required.']
    #     assert response.data.get(self.new_password2_field) == ['This field is required.']
    #     assert response.data.get(self.uid_field) == ['This field is required.']
    #     assert response.data.get(self.token_field) == ['This field is required.']
    #
    #     payloads.update({
    #         self.email_field: user.email,
    #     })
    #     response = client.post(self.password_reset_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     # email_data = find_values_in_mail_body(mailoutbox[0].body, 'reset_password')
    #     payloads.clear()
    #
    #     payloads.update({
    #         self.new_password1_field: faker.password(),
    #         self.new_password2_field: faker.password(),
    #         self.uid_field: faker.uuid4(),
    #         self.token_field: faker.uuid4(),
    #     })
    #     response = client.post(self.password_reset_confirm_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert len(response.data['codes']) == 1
    #     assert self.uid_field in response.data
    #     assert response.data.get(self.uid_field) == ['Invalid value']
    #
    #     payloads.update({
    #         # self.uid_field: email_data.get(self.uid_field),
    #     })
    #     response = client.post(self.password_reset_confirm_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert len(response.data['codes']) == 1
    #     assert self.new_password2_field in response.data
    #     assert response.data.get(self.new_password2_field) == ["The two password fields didn't match."]
    #
    #     new_password = faker.password()
    #     payloads.update({
    #         self.new_password1_field: new_password,
    #         self.new_password2_field: new_password,
    #     })
    #     response = client.post(self.password_reset_confirm_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert self.token_field in response.data
    #     assert response.data.get(self.token_field) == ['Invalid value']
    #
    #     payloads.update({
    #         # self.token_field: email_data.get('token')
    #     })
    #     response = client.post(self.password_reset_confirm_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 1
    #     assert self.detail_field in response.data
    #     assert response.data.get(self.detail_field) == 'Password has been reset with the new password.'
    #
    #     payloads.clear()
    #     payloads.update({
    #         self.email_field: user.email,
    #         self.password_field: USER_DEFAULT_PASSWORD,
    #     })
    #     response = client.post(self.login_url, data=payloads)
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     payloads.update({
    #         self.password_field: new_password,
    #     })
    #     response = client.post(self.login_url, data=payloads)
    #     assert response.status_code == status.HTTP_200_OK
