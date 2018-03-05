from collections import OrderedDict

from rest_framework.pagination import (
    PageNumberPagination as BasePageNumberPagination,
)
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    """

    Custom PageNumberPagination with additional data
    like page_number_first and page_number_last

    """

    page_size_query_param = 'page_size'
    page_size_query_description = 'Results per page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('max_page_size', self.max_page_size),
            ('page_number_first', 1),
            ('page_number_last', self.page.paginator.num_pages),
            ('page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
