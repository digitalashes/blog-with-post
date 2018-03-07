from django.contrib.auth import logout as auth_logout, get_user_model
from django.db.models import Count
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

from comments.filters import (
    CommentsSearchFilter,
    CommentsOrderingFilter,
)
from comments.models import Comment
from comments.serializers import CommentSimpleSerializer
from posts.filters import (
    PostsSearchFilter,
    PostsOrderingFilter,
)
from posts.models import Post
from posts.serializers import PostSimpleSerializer
from users.filters import (
    UsersSearchFilter,
    UsersOrderingFilter,
)
from users.serializers import (
    VerifyEmailResendSerializer,
    UserDetailsSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


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


class UserListApiView(generics.ListAPIView):
    """
    get: List of users

    """

    queryset = User.objects.only(
        'id', 'email', 'username',
        'first_name', 'last_name',
        'avatar', 'last_login',
    ).annotate(
        posts_total=Count('posts', distinct=True),
        comments_total=Count('comments', distinct=True),
    )
    http_method_names = ('get', 'head', 'options')
    filter_backends = (UsersSearchFilter, UsersOrderingFilter)
    search_fields = ('email', 'first_name', 'last_name')
    serializer_class = UserDetailsSerializer
    permission_classes = (AllowAny,)


class UserInfoApiView(generics.RetrieveAPIView):
    """
    get: Return user info

    """

    queryset = User.objects.only(
        'id', 'email', 'username',
        'first_name', 'last_name',
        'avatar', 'last_login',
    ).annotate(
        posts_total=Count('posts', distinct=True),
        comments_total=Count('comments', distinct=True),
    )
    http_method_names = ('get', 'head', 'options')
    serializer_class = UserDetailsSerializer
    permission_classes = (AllowAny,)
    lookup_url_kwarg = 'pk'


class UserUpdateApiView(generics.UpdateAPIView):
    """
    patch: Update user info

    """

    http_method_names = ('patch', 'head', 'options')
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user


class UserPostsListView(generics.ListAPIView):
    queryset = Post.objects.only('id', 'title', 'created', 'modified')
    http_method_names = ('get', 'head', 'options')
    permission_classes = (AllowAny,)
    filter_backends = (PostsOrderingFilter, PostsSearchFilter)
    search_fields = ('title', 'body')
    serializer_class = PostSimpleSerializer

    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            'author_id': self.kwargs[lookup_url_kwarg],
            'status': Post.PUBLISHED,
        }
        queryset = super().get_queryset().filter(**filter_kwargs)
        return queryset


class UserCommentsListView(generics.ListAPIView):
    queryset = Comment.objects.only('id', 'post_id', 'body', 'created', 'modified')
    http_method_names = ('get', 'head', 'options')
    permission_classes = (AllowAny,)
    filter_backends = (CommentsSearchFilter, CommentsOrderingFilter)
    search_fields = ('body',)
    serializer_class = CommentSimpleSerializer

    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            'user_id': self.kwargs[lookup_url_kwarg],
        }
        queryset = super().get_queryset().filter(**filter_kwargs)
        return queryset


registration = RegisterApiView.as_view()

verify_email_resend = VerifyEmailResendApiView.as_view()
verify_email_confirm = VerifyEmailConfirmApiView.as_view()

login = LoginApiView.as_view()
logout = LogoutApiView.as_view()

password_change = PasswordChangeApiView.as_view()
password_reset = PasswordResetView.as_view()
password_reset_confirm = PasswordResetConfirmView.as_view()

user_list = UserListApiView.as_view()
user_info = UserInfoApiView.as_view()
user_update = UserUpdateApiView.as_view()

user_posts = UserPostsListView.as_view()
user_comments = UserCommentsListView.as_view()
