from rest_framework import generics
from rest_framework.permissions import AllowAny

from posts.filters import PostsSearchFilter, PostsOrderingFilter
from posts.models import Post
from posts.serializers import PostListSerializer


class PostListApiView(generics.ListAPIView):
    queryset = Post.objects.only(
        'id', 'title', 'body', 'image',
        'author', 'created', 'modified'
    ).select_related('author').order_by('-created', 'author__username')
    http_method_names = ('get', 'head', 'options')
    serializer_class = PostListSerializer
    filter_backends = (PostsSearchFilter, PostsOrderingFilter)
    search_fields = ('title', 'body', 'author__username')
    permission_classes = (AllowAny,)


post_list = PostListApiView.as_view()
