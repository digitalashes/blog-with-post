from rest_framework import serializers

from posts.models import Post
from users.serializers import UserSimpleSerializer


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title',)


class PostDetailsSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer()
    updated = serializers.ReadOnlyField(source='modified')

    class Meta:
        model = Post
        fields = ('id', 'title', 'body',
                  'image', 'author',
                  'status', 'allow_comments',
                  'created', 'updated')


class PostListSerializer(PostDetailsSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('body', None)
        self.fields.pop('image', None)


class PostSerializer(PostDetailsSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('author', None)

    def create(self, validated_data):
        validated_data.update({
            'author': self.context.get('request').user
        })
        return super().create(validated_data)
