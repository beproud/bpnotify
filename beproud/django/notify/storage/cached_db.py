#:coding=utf-8:

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_str
from django.core.cache import get_cache, cache
from django.conf import settings

from beproud.django.notify.storage.db import DBStorage

__all__ = ('CachedDBStorage',)

class CachedDBStorage(DBStorage):
    """
    A notification settings backend for storing user
    settings in the database. The settings are also
    cached using Django's cache framework.
    """

    def make_key(self, target, notify_type, media_name):
        content_type = ContentType.objects.get_for_model(target)
        key_list = map(lambda a: smart_str(a), [target.pk, content_type.pk, notify_type, media_name])
        return u'bpnotify|setting|%s' % (':'.join(key_list))

    def get(self, target, notify_type, media_name, default=None):
        cache_key = self.make_key(target, notify_type, media_name)
        data = cache.get(cache_key, None)
        if data is None:
            data = super(CachedDBStorage, self).get(
                target,
                notify_type,
                media_name,
                None
            )
            if data is not None:
                cache.set(cache_key, data)
            else:
                data = default
        return data

    def set(self, target, notify_type, media_name, send):
        super(CachedDBStorage, self).set(
            target,
            notify_type,
            media_name,
            send,
        )
        cache.set(self.make_key(target, notify_type, media_name), send)
