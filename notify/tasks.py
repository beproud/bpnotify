# vim:fileencoding=utf8

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
