from django.utils.translation import ugettext_lazy as _
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)


class UsersSearchFilter(SearchFilter):
    pass


class UsersOrderingFilter(OrderingFilter):
    ordering_fields = ('id', 'username', 'email')
    ordering_description = _(
        f'Which field to use when ordering the results. Available values: {", ".join(ordering_fields)}'
    )
