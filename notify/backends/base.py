#:coding=utf8:

class BaseNotify(object):

    def send(users, notice_type, extra_context={}, target_id=None, origin_id=None, date=None):
        raise NotImplemented
