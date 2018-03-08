from rest_framework import serializers

from posts.models import Post
from users.serializers import UserSimpleSerializer


class PostSimpleSerializer(serializers.ModelSerializer):
    updated = serializers.ReadOnlyField(source='modified')

    class Meta:
        model = Post
        fields = ('id', 'title', 'created', 'updated')


class PostDetailsSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer()
    updated = serializers.ReadOnlyField(source='modified')
    comments_total = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body',
                  'image', 'author',
                  'status', 'allow_comments',
                  'created', 'updated',
                  'comments_total')

    @staticmethod
    def get_comments_total(obj):
        return getattr(obj, 'comments_total', 0)


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

    def update(self, instance, validated_data):
        validated_data.update({
            'body_markup_type': 'markdown',
        })
        return super().update(instance, validated_data)
