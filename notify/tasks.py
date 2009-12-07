# vim:fileencoding=utf8
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

if 'celery' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured("You must add celery to INSTALLED_APPS to use the asyncronous task queue")

try:
    from celery.task import Task
    from celery.registry import tasks

    from notify import send_notification_now

    class SendNotification(Task):

        def run(self, users, notice_type, extra_context={}, target_id=None, origin_id=None, ctime=None, exclude_media=[], **kwargs):
            return send_notification_now(
            users,
            notice_type,
            extra_context=extra_context,
            target_id=target_id,
            origin_id=None,
            ctime=ctime,
            exclude_media=exclude_media,
        )

    tasks.register(SendNotification)
except ImportError:
    raise ImproperlyConfigured("You must install celery to use the asyncronous task queue")
