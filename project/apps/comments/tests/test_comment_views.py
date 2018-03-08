import datetime

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from freezegun import freeze_time
from rest_framework import status

from comments.models import Comment
from comments.serializers import CommentSimpleSerializer
from posts.models import Post

User = get_user_model()


@pytest.mark.django_db
class CommentViewsTestSuite:

    @classmethod
    def setup_class(cls):
        cls.comment_create_url = reverse_lazy('api:comments:create')
        cls.comment_update_url = 'api:comments:update'
        cls.comment_delete_url = 'api:comments:delete'

        cls.post_id_field = 'post_id'
        cls.body_field = 'body'

    @classmethod
    def teardown_class(cls):
        pass

    def test_comment_create_view(self, client, user, post_factory, faker):
        for http_method in ('get', 'post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(self.comment_create_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        client.force_authenticate(user)

        for http_method in ('get', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(self.comment_create_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        payloads = {}

        response = client.post(self.comment_create_url, data=payloads)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['codes']) == 2
        assert self.post_id_field in response.data
        assert self.body_field in response.data
        assert response.data.get(self.post_id_field) == ['This field is required.']
        assert response.data.get(self.body_field) == ['This field is required.']

        draft_post = post_factory(status=Post.DRAFT)
        payloads.update({
            self.post_id_field: draft_post.id,
            self.body_field: faker.word()
        })
        response = client.post(self.comment_create_url, data=payloads)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        post_without_comments = post_factory(allow_comments=False)

        payloads.update({
            self.post_id_field: post_without_comments.id,
        })
        response = client.post(self.comment_create_url, data=payloads)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        normal_post = post_factory()

        comments_count = user.comments.count()
        payloads.update({
            self.post_id_field: normal_post.id,
        })
        response = client.post(self.comment_create_url, data=payloads)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == CommentSimpleSerializer(Comment.objects.get(id=response.data.get('id'))).data
        user.refresh_from_db()
        assert user.comments.count() == comments_count + 1

    def test_comment_update_view(self, client, comment, comment_factory, faker, settings):
        test_url = reverse_lazy(self.comment_update_url, args=(1,))
        for http_method in ('get', 'post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        client.force_authenticate(comment.user)

        for http_method in ('get', 'post', 'put', 'delete'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        another_comment = comment_factory()
        new_body = faker.word()
        payloads = {
            self.body_field: new_body
        }

        url = reverse_lazy(self.comment_update_url, args=(another_comment.id,))
        response = client.patch(url, data=payloads)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        old_body = comment.body
        url = reverse_lazy(self.comment_update_url, args=(comment.id,))

        with freeze_time(datetime.datetime.now() - datetime.timedelta(minutes=15)):
            response = client.patch(url, data=payloads)
        assert response.status_code == status.HTTP_200_OK
        assert self.body_field in response.data
        assert response.data.get(self.body_field) == new_body
        comment.refresh_from_db()
        assert comment.body != old_body
        assert comment.body == new_body

        with freeze_time(datetime.datetime.now() + settings.COMMENT_UPDATE_TIMEDELTA):
            response = client.patch(url, data=payloads)
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_comment_delete_view(self, client, user, comment_factory, settings):
        test_url = reverse_lazy(self.comment_delete_url, args=(1,))
        for http_method in ('get', 'post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        client.force_authenticate(user)

        for http_method in ('get', 'post', 'put', 'patch'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        url = reverse_lazy(self.comment_delete_url, args=(100500,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        another_comment = comment_factory()
        url = reverse_lazy(self.comment_delete_url, args=(another_comment.id,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        comment = comment_factory(user=user)
        url = reverse_lazy(self.comment_delete_url, args=(comment.id,))

        comments_count = user.comments.count()
        with freeze_time(datetime.datetime.now() - datetime.timedelta(minutes=15)):
            response = client.delete(url)
            assert response.status_code == status.HTTP_204_NO_CONTENT

            response = client.delete(url)
            assert response.status_code == status.HTTP_404_NOT_FOUND

        user.refresh_from_db()
        assert user.comments.count() == comments_count - 1

        comment = comment_factory(user=user)
        url = reverse_lazy(self.comment_delete_url, args=(comment.id,))
        comments_count = user.comments.count()
        with freeze_time(datetime.datetime.now() + settings.COMMENT_DELETE_TIMEDELTA):
            response = client.delete(url)
            assert response.status_code == status.HTTP_403_FORBIDDEN
        user.refresh_from_db()
        assert user.comments.count() == comments_count
