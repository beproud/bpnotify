#:coding=utf-8:

from datetime import datetime

from base import BaseNotify
from django.db import DatabaseError

class ModelNotify(BaseNotify):
    def _send(user, notice_type, extra_context={}, target_id=None, origin_id=None, date=None):
        try:
            notification = Notification.objects.create(
                user = user,
                notice_type = notice_type,
                extra_data = extra_context,
                target_id = target_id,
                origin_id = origin_id,
                ctime = ctime if ctime else datetime.now(),
            )
            return 1
        except DatabaseError:
            return 0
