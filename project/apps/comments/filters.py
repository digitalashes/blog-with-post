from django.utils.translation import ugettext_lazy as _
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)


class CommentsSearchFilter(SearchFilter):
    pass


class CommentsOrderingFilter(OrderingFilter):
    ordering_fields = ('id', 'created', 'modified')
    ordering_description = _(
        f'Which field to use when ordering the results. Available values: {", ".join(ordering_fields)}'
    )
