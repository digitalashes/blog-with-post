from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from comments.models import Comment
from comments.permissions import TimeDeltaPermission
from comments.serializers import (
    CommentSerializer,
    CommentUpdateSerializer,
)
from common.permissions import IsObjectOwner


class CommentCreateApiView(generics.CreateAPIView):
    """
    post: Create a new comment

    """

    http_method_names = ('post', 'head', 'options')
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)


class CommentUpdateApiView(generics.UpdateAPIView):
    """
    patch: Update comment body

    """

    queryset = Comment.objects
    http_method_names = ('patch', 'head', 'options')
    serializer_class = CommentUpdateSerializer
    permission_classes = (IsAuthenticated, IsObjectOwner, TimeDeltaPermission)


class CommentDeleteApiView(generics.DestroyAPIView):
    """
    delete: Delete comment

    """

    queryset = Comment.objects
    http_method_names = ('delete', 'head', 'options')
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsObjectOwner, TimeDeltaPermission)


comment_create = CommentCreateApiView.as_view()
comment_update = CommentUpdateApiView.as_view()
comment_delete = CommentDeleteApiView.as_view()
