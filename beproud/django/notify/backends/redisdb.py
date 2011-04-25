#:coding=utf-8:

from django.core.exceptions import ImproperlyConfigured
from django.utils import simplejson as json

from beproud.django.notify.backends.base import BaseBackend

try:
    from redis import Redis
except ImportError:
    raise ImproperlyConfigured('You must install the redis python client in order to use the redis backend')

class RedisBackend(BaseBackend):
    """
    A backend that stores notifications in a redis list for each
    target, media combination. A maximum number of items in the list
    can be specified and the backend will cull the items in the list.

    Extra data must be JSON serializable.
    """

    def __init__(self, key_func=None, max_items=None, **kwargs):
        if key_func is None:
            key_func = lambda target, media: 'bpnotify|%s:%s' % (target.pk, media)
        self.key_func = key_func
        self.max_items = max_items
        self.redis = Redis(**kwargs)
    
    def _send(self, target, notify_type, media, extra_data={}):
        try:
            key = self.key_func(target, media)
            self.redis.rpush(key, json.dumps({
                'notify_type': notify_type,
                'media': media,
                'extra_data': extra_data,
            }))
            if self.max_items and self.redis.llen(key) > self.max_items:
                self.redis.ltrim(0, self.max_items-1)

            return 1
        except (RedisError, TypeError), e:
            # TODO: logging
            return 0
