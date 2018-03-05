from django.contrib.auth import logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration.views import RegisterView as BaseRegisterView
from rest_auth.registration.views import VerifyEmailView as BaseVerifyEmailView
from rest_auth.views import LoginView as BaseLoginView
from rest_auth.views import (
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetView as BasePasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import (
    jwt_payload_handler,
    jwt_encode_handler,
)

from users.serializers import (
    VerifyEmailResendSerializer,
)


class RegisterApiView(BaseRegisterView):
    """
    post: Create new user instance.

    """

    http_method_names = ('post', 'head', 'options')


class VerifyEmailResendApiView(generics.GenericAPIView):
    """
    post: Resend email verification letter.

    """

    serializer_class = VerifyEmailResendSerializer
    http_method_names = ('post', 'head', 'options')
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(self.request)
        return Response(
            {'detail': _('Verification e-mail sent.')},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailConfirmApiView(BaseVerifyEmailView):
    """
    post: Verify email if valid secret key given.

    """

    http_method_names = ('post', 'head', 'options')
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        confirmation = self.get_object()
        user = confirmation.email_address.user

        # purge other unverified emails
        user.emailaddress_set.exclude(email=confirmation.email_address.email).delete()

        # create token and respond auth key
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token, 'user': payload}, status=status.HTTP_200_OK)


class LoginApiView(BaseLoginView):
    """
    post: Return auth token and user data.

    """

    http_method_names = ('post', 'head', 'options')


class LogoutApiView(APIView):
    """
    post: Calls Django logout method and delete the Token object assigned to the current User object.

    """

    http_method_names = ('post', 'head', 'options')
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        auth_logout(request)
        return Response({'detail': _('Successfully logged out.')}, status=status.HTTP_200_OK)


class PasswordChangeApiView(BasePasswordChangeView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.

    """

    http_method_names = ('post', 'head', 'options')


class PasswordResetView(BasePasswordResetView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.

    """

    http_method_names = ('post', 'head', 'options')


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.

    """

    http_method_names = ('post', 'head', 'options')


registration = RegisterApiView.as_view()

verify_email_resend = VerifyEmailResendApiView.as_view()
verify_email_confirm = VerifyEmailConfirmApiView.as_view()

login = LoginApiView.as_view()
logout = LogoutApiView.as_view()

password_change = PasswordChangeApiView.as_view()
password_reset = PasswordResetView.as_view()
password_reset_confirm = PasswordResetConfirmView.as_view()
