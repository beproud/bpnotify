#:coding=utf-8:

import uuid
from datetime import datetime

from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.utils import simplejson as json

from beproud.django.notify.backends.base import BaseBackend
from beproud.django.notify.utils import local_to_utc, utc_to_local, parse_utc_isostring

try:
    from redis import Redis, RedisError
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
            key_func = lambda target, media: 'bpnotify|%s:%s:%s' % (
                ContentType.objects.get_for_model(target).pk,
                target.pk,
                media,
            )
        self.key_func = key_func
        self.max_items = max_items
        self.redis = Redis(**kwargs)
    
    def _send(self, target, notify_type, media, extra_data={}):
        try:
            key = self.key_func(target, media)
            # We know the target and media from the key
            # so we don't need to save it in Redis
            self.redis.rpush(key, json.dumps({
                'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, Site.objects.get_current().domain)),
                'notify_type': notify_type,
                'extra_data': extra_data,
                'ctime': local_to_utc(datetime.now()).isoformat(),
            }))
            if self.max_items and self.redis.llen(key) > self.max_items:
                self.redis.ltrim(0, self.max_items-1)

            return 1
        except (RedisError, TypeError, ValueError), e:
            # TODO: logging
            return 0

    def get(self, target, media, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = -1

        key = self.key_func(target, media)
        notifications = self.redis.lrange(key, start, end)

        def _func(n):
            try:
                n = json.loads(n)
                return {
                    'id': n.get('id'),
                    'target': target,
                    'notify_type': n.get('notify_type'),
                    'media': media,
                    'extra_data': n.get('extra_data'),
                    'ctime': utc_to_local(parse_utc_isostring(n.get('ctime'))),
                }
            except (TypeError, ValueError), e:
                # TODO: logging
                return None
        
        # Map the notifications to the right format.
        return map(_func, notifications)

    def count(self, target, media):
        key = self.key_func(target, media)
        return self.redis.llen(key)
