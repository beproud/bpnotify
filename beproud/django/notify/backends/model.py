#:coding=utf-8:

from beproud.django.notify.backends.base import BaseBackend
from beproud.django.notify.models import Notification
from django.db import DatabaseError

class NotifyBackend(BaseNotify):
    """
    A basic backend that saves to the default
    Notification model. Extra data must be JSON serializable.
    """
    def _send(target, notice_type, media, extra_data={}):
        notification = Notification(
            notice_type = notice_type,
            media = media,
            extra_data = extra_data,
        )
        notification.target = target

        try:
            notification.save()
            return 1
        except (TypeError, DatabaseError):
            # extra_data could not be serialized to JSON or
            # there was some kind of Database error
            # TODO: logging
            return 0
