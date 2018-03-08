import datetime

from django.conf import settings
from pytz import UTC
from rest_framework.permissions import BasePermission


class TimeDeltaPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        now = UTC.localize(datetime.datetime.now())
        if request.method.lower() == 'patch':
            time_delta = settings.COMMENT_UPDATE_TIMEDELTA
            return obj.modified > (now + time_delta)
        else:
            time_delta = settings.COMMENT_DELETE_TIMEDELTA
            return obj.modified > (now + time_delta)
