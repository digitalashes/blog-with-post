from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from posts.filters import (
    PostsSearchFilter,
    PostsOrderingFilter,
    MyPostsStatusFilter,
)
from posts.models import Post
from posts.permissions import (
    PostDetailPermission,
    IsPostOwner,
)
from posts.serializers import (
    PostListSerializer,
    PostSerializer,
)


class PostListApiView(generics.ListAPIView):
    queryset = Post.objects.only(
        'id', 'title', 'body', 'image',
        'author', 'created', 'modified'
    ).select_related('author').filter(
        status=Post.PUBLISHED
    ).order_by('-created', 'author__username')
    http_method_names = ('get', 'head', 'options')
    serializer_class = PostListSerializer
    filter_backends = (
        PostsSearchFilter,
        PostsOrderingFilter,
    )
    search_fields = ('title', 'body', 'author__username')
    permission_classes = (AllowAny,)


class MyPostListApiView(PostListApiView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    filter_backends = (
        MyPostsStatusFilter,
        PostsSearchFilter,
        PostsOrderingFilter,
    )
    filter_fields = ('status',)

    def get_queryset(self):
        user = self.request.user
        return Post.objects.only(
            'id', 'title', 'body', 'image',
            'created', 'modified',
        ).filter(author_id=user.id).order_by('-created')


class PostCreateApiView(generics.CreateAPIView):
    http_method_names = ('post', 'head', 'options')
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer


class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.only(
        'id', 'title', 'body', 'image',
        'author', 'created', 'modified'
    ).select_related('author')
    http_method_names = ('get', 'head', 'options')
    permission_classes = (AllowAny, PostDetailPermission)
    serializer_class = PostSerializer
    lookup_url_kwarg = 'pk'


class PostUpdateApiView(generics.UpdateAPIView):
    queryset = Post.objects.only(
        'id', 'title', 'body', 'image',
        'author', 'created', 'modified'
    ).select_related('author')
    http_method_names = ('patch', 'head', 'options')
    permission_classes = (IsAuthenticated, IsPostOwner)
    serializer_class = PostSerializer


class PostDeleteApiView(generics.DestroyAPIView):
    queryset = Post.objects.only(
        'id', 'title', 'body', 'image',
        'author', 'created', 'modified'
    ).select_related('author')
    http_method_names = ('delete', 'head', 'options')
    permission_classes = (IsAuthenticated, IsPostOwner)


post_list = PostListApiView.as_view()
my_post_list = MyPostListApiView.as_view()
post_create = PostCreateApiView.as_view()
post_detail = PostDetailApiView.as_view()
post_update = PostUpdateApiView.as_view()
post_delete = PostDeleteApiView.as_view()
