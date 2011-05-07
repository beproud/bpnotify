#:coding=utf-8:

from django.contrib.contenttypes.models import ContentType
from django.db import DatabaseError

from beproud.django.notify.storage.base import BaseStorage
from beproud.django.notify.models import NotifySetting

__all__ = ('DBStorage',)

class DBStorage(object):
    """
    A notification settings backend for storing user
    settings in the database.
    """

    def get(self, target, notify_type, media_name, default=None):
        try:
            content_type = ContentType.objects.get_for_model(target)
            return NotifySetting.objects.get(
                target_content_type = content_type,
                target_object_id = target.pk,
                notify_type = notify_type,
                media = media_name,
            ).send
        except NotifySetting.DoesNotExist, e:
            return default

    def set(self, target, notify_type, media_name, send):
        try:
            content_type = ContentType.objects.get_for_model(target)
            try:
                setting = NotifySetting.objects.get(
                    target_content_type = content_type,
                    target_object_id = target.pk,
                    notify_type = notify_type,
                    media = media_name,
                )
                setting.send = send
                setting.save()
                return True
            except NotifySetting.DoesNotExist, e:
                setting = NotifySetting.objects.create(
                    target_content_type = content_type,
                    target_object_id = target.pk,
                    notify_type = notify_type,
                    media = media_name,
                    send = send,
                )
                return True
        except DatabaseError, e:
            return False
