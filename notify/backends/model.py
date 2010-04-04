#:coding=utf-8:

from base import BaseNotify

class ModelNotify(BaseNotify):
    def send(users, notice_type, extra_context={}, target_id=None, origin_id=None, date=None):
            notification = Notification.objects.create(
                user = user,
                notice_type = notice_type,
                extra_data = extra_context,
                target_id = target_id,
                origin_id = origin_id,
                ctime = ctime if ctime else datetime.now(),
            )

