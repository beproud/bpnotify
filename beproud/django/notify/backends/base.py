#:coding=utf8:

class BaseBackend(object):

    def send(targets, notify_type, media, extra_context={}):
        """
        Sends a message to the given users.

        targets: The notification target model instance. Normally a user.
        notify_type: The notify type
        media: The media name
        extra_context: A dictionary containing extra data that is sent along with
                       the notification
        Returns the number of notifications sent.
        """
        for target in targets:
            self._send(
                target,
                notice_type,
                extra_content,
                target_id,
                origin_id,
                date or datetime.now(),
            )

    def _send(user, notice_type, media, extra_context={})
        raise NotImplemented('You must implement the _send() method in from the BaseBackend class.')
