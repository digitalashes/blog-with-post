import coreapi
import coreschema
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from rest_framework.filters import (
    BaseFilterBackend,
    SearchFilter,
    OrderingFilter,
)

from posts.models import Post


class PostsOrderingFilter(SearchFilter):
    pass


class PostsSearchFilter(OrderingFilter):
    ordering_fields = ('id', 'title', 'author')
    ordering_description = _(
        f'Which field to use when ordering the results. Available values: {", ".join(ordering_fields)}'
    )


class MyPostsStatusFilter(BaseFilterBackend):
    filter_name = 'status'
    filter_available_values = Post.STATUS._db_values

    def filter_queryset(self, request, queryset, view):
        allowed_filters = view.filter_fields
        query_filters = request.query_params.copy()

        # Cleaning from not allowed filters
        for filter_name, value in request.query_params.items():
            if filter_name not in allowed_filters:
                query_filters.pop(filter_name, None)

        for filter_name, value in query_filters.items():
            if filter_name == self.filter_name:
                value = {value} & self.filter_available_values
                if value:
                    queryset = queryset.filter(status__in=value)
        return queryset

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name='status',
                description=force_text('A parameter that allows you to filter by status'),
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text('Post status'),
                    description=force_text(f'Available values: {", ".join(self.filter_available_values)}')
                ),
                type='string',
            )
        ]
