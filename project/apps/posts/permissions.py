from django.http import Http404
from rest_framework.permissions import BasePermission


class PostDetailPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_anonymous and obj.is_draft:
            raise Http404
        if user.is_authenticated and (obj.is_draft and obj.author_id != user.id):
            raise Http404
        return True
