#:coding=utf-8:

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

if 'djcelery' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured("You must add celery to INSTALLED_APPS to use the asyncronous task queue")

try:
    from celery.task import Task
    from celery.registry import tasks

    from beproud.django.notify import notify_now 

    class Notify(Task):

        def run(self, users, notice_type, extra_data={}, include_media=None, exclude_media=[], **kwargs):
            return send_notification_now(
                users,
                notice_type,
                extra_data=extra_data,
                include_media=include_media,
                exclude_media=exclude_media,
            )
    tasks.register(Notify)

except ImportError:
    raise ImproperlyConfigured("You must install celery to use the asyncronous task queue")
