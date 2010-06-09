#:coding=utf8:

class BaseNotify(object):

    def send(user, notice_type, extra_context={}, target_id=None, origin_id=None, date=None):
        """
        Sends a message to the given user.

        notice_type: The notification type
        extra_context: A dictionary containing extra data that is sent along with
                       the notification
        target_id: A target id for possible later reference. This should be set
                   to the id of a related object.
        origin_id: A origin id for possible later reference. This should be set
                   to the id of the object sending the notification.
        date:

        Returns the number of notifications sent.
        """
        raise NotImplemented
