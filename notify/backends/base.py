#:coding=utf8:

class BaseNotify(object):

    def send(recipient_list, notice_type, extra_context={}, target_id=None, origin_id=None, date=None):
        """
        Sends a message to the given users.

        recipient_list: A list of users to send the notification. 
        notice_type: The notification type
        extra_context: A dictionary containing extra data that is sent along with
                       the notification
        target_id: A target id for possible later reference. This should be set
                   to the id of a related object.
        origin_id: A origin id for possible later reference. This should be set
                   to the id of the object sending the notification.
        date: The date the notification is sent. Defaults to the current date.
              Can be set to past dates for backends that support dates.

        Returns the number of notifications sent.
        """
        for user in recipient_list:
            self._send(
                user,
                notice_type,
                extra_content,
                target_id,
                origin_id,
                date or datetime.now(),
            )

    def _send(user, notice_type, extra_context={}, target_id=None, origin_id=None, date=None):
        raise NotImplemented
