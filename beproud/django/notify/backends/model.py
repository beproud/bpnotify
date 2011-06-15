#:coding=utf-8:

from django.contrib.contenttypes.models import ContentType
from django.db import DatabaseError

from beproud.django.notify.backends.base import BaseBackend

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
    
    def get(self, target, media, start=None, end=None):
        from beproud.django.notify.models import Notification

        notifications = Notification.objects.filter(
            target_content_type = ContentType.objects.get_for_model(target),
            target_object_id = target.pk,
            media = media, 
        ).order_by('-ctime')
        
        if start is not None or end is not None:
            if start is None:
                notifications = notifications[:end]
            elif end is None:
                notifications = notifications[start:]
            else:
                notifications = notifications[start:end]

        def _func(n):
            return {
                'id': 'Notification:%s' % n.id,
                'target': n.target,
                'notify_type': n.notify_type,
                'media': n.media,
                'extra_data': n.extra_data,
                'ctime': n.ctime,
            }

        return map(_func, notifications)
