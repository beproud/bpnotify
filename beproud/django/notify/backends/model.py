#:coding=utf-8:

from beproud.django.notify.backends.base import BaseBackend
from django.db import DatabaseError

class ModelBackend(BaseBackend):
    """
    A basic backend that saves to the default
    Notification model. Extra data must be JSON serializable.
    """
    def _send(self, target, notify_type, media, extra_data={}):
        from beproud.django.notify.models import Notification

        notification = Notification(
            notify_type = notify_type,
            media = media,
            extra_data = extra_data,
        )
        notification.target = target

        try:
            notification.save()
            return 1
        except (TypeError, DatabaseError), e:
            # extra_data could not be serialized to JSON or
            # there was some kind of Database error
            # TODO: logging
            return 0
