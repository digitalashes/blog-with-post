from rest_framework import serializers

from posts.models import Post
from users.serializers import UserSimpleSerializer


class PostListSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer()
    updated = serializers.ReadOnlyField(source='modified')

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'created', 'updated')
        read_only_fields = fields
