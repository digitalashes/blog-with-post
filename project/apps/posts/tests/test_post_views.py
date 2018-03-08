import pytest
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse_lazy
from rest_framework import status

from posts.models import Post
from posts.serializers import PostSerializer

User = get_user_model()


@pytest.mark.django_db
class PostViewsTestSuite:

    @classmethod
    def setup_class(cls):
        cls.post_list_url = reverse_lazy('api:posts:list')
        cls.my_post_list_url = reverse_lazy('api:posts:my_post_list')
        cls.post_create_url = reverse_lazy('api:posts:create')
        cls.post_detail_url = 'api:posts:detail'
        cls.post_update_url = 'api:posts:update'
        cls.post_delete_url = 'api:posts:delete'

        cls.title_field = 'title'
        cls.body_field = 'body'
        cls.status_field = 'status'
        cls.allow_comments_field = 'allow_comments'
        cls.updated_field = 'updated'

    @classmethod
    def teardown_class(cls):
        pass

    def test_post_list_view(self, client):
        for http_method in ('post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(self.post_list_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        posts_count = Post.objects.filter(status=Post.PUBLISHED).count()
        response = client.get(self.post_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == posts_count
        assert response.data['results']

    def test_my_posts_view(self, client):
        for http_method in ('get', 'post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(self.my_post_list_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user = User.objects.annotate(
            posts_total=Count('posts')
        ).last()
        client.force_authenticate(user)

        for http_method in ('post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(self.my_post_list_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = client.get(self.my_post_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == user.posts_total
        assert response.data['results']
        author_id = set([item.get('author').get('id') for item in response.data['results']])
        assert len(author_id) == 1
        assert author_id.intersection({user.id})

    def test_post_create(self, client, faker):
        for http_method in ('get', 'post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(self.post_create_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user = User.objects.annotate(
            posts_total=Count('posts')
        ).last()
        client.force_authenticate(user)

        for http_method in ('get', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(self.post_create_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        payloads = {}

        response = client.post(self.post_create_url, data=payloads)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['codes']) == 2

        assert self.title_field in response.data
        assert self.body_field in response.data
        assert response.data.get(self.title_field) == ['This field is required.']
        assert response.data.get(self.body_field) == ['This field is required.']

        payloads.update({
            self.title_field: faker.sentence(),
            self.body_field: faker.text(),
            self.allow_comments_field: True,
        })

        user_posts_count = user.posts_total
        response = client.post(self.post_create_url, data=payloads)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == PostSerializer(Post.objects.get(id=response.data.get('id'))).data
        assert response.data.get(self.status_field) == Post.PUBLISHED
        assert response.data.get(self.allow_comments_field)

        user.refresh_from_db()
        user.posts_total = user_posts_count + 1

        payloads.update({
            self.title_field: faker.sentence(),
            self.body_field: faker.text(),
            self.allow_comments_field: True,
            self.status_field: Post.DRAFT,
        })

        user_posts_count = user.posts_total
        response = client.post(self.post_create_url, data=payloads)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == PostSerializer(Post.objects.get(id=response.data.get('id'))).data
        assert response.data.get(self.status_field) == Post.DRAFT
        assert response.data.get(self.allow_comments_field)

        user.refresh_from_db()
        user.posts_total = user_posts_count + 1

    def test_post_detail(self, client, post_factory):
        test_url = reverse_lazy(self.post_detail_url, args=(1,))
        for http_method in ('post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        url = reverse_lazy(self.post_detail_url, args=(100500,))
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        draft_post = post_factory(status=Post.DRAFT)
        url = reverse_lazy(self.post_detail_url, args=(draft_post.id,))
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        non_draft_post = post_factory(status=Post.PUBLISHED)
        url = reverse_lazy(self.post_detail_url, args=(non_draft_post.id,))
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == PostSerializer(non_draft_post).data

        client.force_authenticate(draft_post.author)
        url = reverse_lazy(self.post_detail_url, args=(draft_post.id,))
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == PostSerializer(draft_post).data

    def test_post_update(self, client, user_factory, post_factory, faker):
        test_url = reverse_lazy(self.post_update_url, args=(1,))
        for http_method in ('get', 'post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user = User.objects.prefetch_related('posts').last()
        client.force_authenticate(user)

        for http_method in ('get', 'post', 'put', 'delete'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        new_user = user_factory()
        draft_post = post_factory(author=new_user, status=Post.DRAFT)
        non_draft_post = post_factory(author=new_user, status=Post.PUBLISHED)

        url = reverse_lazy(self.post_update_url, args=(draft_post.id,))
        response = client.patch(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        url = reverse_lazy(self.post_update_url, args=(non_draft_post.id,))
        response = client.patch(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        payloads = {}
        user_post = user.posts.last()

        url = reverse_lazy(self.post_update_url, args=(user_post.id,))
        response = client.patch(url, data=payloads)
        assert response.status_code == status.HTTP_200_OK
        response.data.pop(self.updated_field, None)
        data = PostSerializer(user_post).data
        data.pop(self.updated_field, None)
        assert response.data == data

        payloads = {
            self.title_field: faker.sentence(),
            self.body_field: faker.words(),
            self.status_field: Post.PUBLISHED,
            self.allow_comments_field: False,
        }

        response = client.patch(url, data=payloads)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get(self.title_field) != data.get(self.title_field)
        assert response.data.get(self.body_field) != data.get(self.body_field)
        assert response.data.get(self.status_field) == Post.PUBLISHED
        assert not response.data.get(self.allow_comments_field)

    def test_post_delete(self, client, post):
        test_url = reverse_lazy(self.post_delete_url, args=(1,))
        for http_method in ('get', 'post', 'put', 'patch', 'delete'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user = User.objects.prefetch_related(
            'posts'
        ).annotate(
            posts_total=Count('posts'),
        ).last()
        client.force_authenticate(user)

        for http_method in ('get', 'post', 'put', 'patch'):
            response = getattr(client, http_method)(test_url)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        url = reverse_lazy(self.post_delete_url, args=(post.id,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        user_post = user.posts.last()
        posts_count = user.posts_total
        url = reverse_lazy(self.post_delete_url, args=(user_post.id,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        user.refresh_from_db()
        user.posts_total = posts_count - 1

        response = client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
