#:coding=utf-8:

from beproud.django.notify.backends.base import BaseBackend
from beproud.django.notify.models import Notification
from django.db import DatabaseError

class NotifyBackend(BaseNotify):
    def _send(target, notice_type, media, extra_data={}):
        try:
            notification = Notification(
                notice_type = notice_type,
                media = media,
                extra_data = extra_data,
            )
            notification.target = target
            notification.save()
            return 1
        except DatabaseError:
            return 0
