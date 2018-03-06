from rest_framework.permissions import BasePermission


class PostDetailPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_anonymous and obj.is_draft:
            return False
        if user.is_authenticated and (obj.is_draft and obj.author_id != user.id):
            return False
        return True


class IsPostOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.author_id
