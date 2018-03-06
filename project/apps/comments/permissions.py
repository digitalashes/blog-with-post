import datetime

from django.conf import settings
from rest_framework.permissions import BasePermission


class TimeDeltaPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method.lower() == 'patch':
            time_delta = settings.COMMENT_UPDATE_TIMEDELTA
            now = datetime.datetime.now()
            return obj.modified > (now + time_delta)
        else:
            time_delta = settings.COMMENT_DELETE_TIMEDELTA
            now = datetime.datetime.now()
            return obj.modified > (now + time_delta)
