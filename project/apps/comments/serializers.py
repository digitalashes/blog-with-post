from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from comments.models import Comment
from common.utils import get_client_ip
from posts.models import Post
from users.serializers import UserSimpleSerializer


class CommentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'body', 'created', 'modified')


class CommentDetailsSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'body', 'created', 'modified')


class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(required=True,
                                       help_text=_('Specific Post ID.'))

    class Meta:
        model = Comment
        fields = ('post_id', 'body',)

    def validate_post_id(self, post_id):
        get_object_or_404(Post, id=post_id,
                          status=Post.PUBLISHED,
                          allow_comments=True)
        return post_id

    def validate(self, attrs):
        request = self.context.get('request')
        user_ip = get_client_ip(request)
        attrs.update({
            'user_id': request.user.id,
            'ip_address': user_ip,
        })
        return attrs

    def to_representation(self, instance):
        return CommentSimpleSerializer(instance).data


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body',)
