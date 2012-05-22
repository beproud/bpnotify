#:coding=utf-8:

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

if 'djcelery' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured("You must add djcelery to INSTALLED_APPS to use the asyncronous task queue")

try:
    from celery.task import Task
    from celery.registry import tasks

    from beproud.django.notify import notify_now 

    class Notify(Task):

        def run(self, targets, notify_type, extra_data={}, include_media=None, exclude_media=[],
                      max_retries=3, retry_countdown=10, **kwargs):
            try:
                return notify_now(
                    targets,
                    notify_type,
                    extra_data=extra_data,
                    include_media=include_media,
                    exclude_media=exclude_media,
                )
            except Exception, e:
                return self.retry(
                    exc=e,
                    countdown=retry_countdown,
                    max_retries=max_retries,
                )
    tasks.register(Notify)

except ImportError:
    raise ImproperlyConfigured("You must install celery to use the asyncronous task queue")
