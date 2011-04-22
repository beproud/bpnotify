#:coding=utf8:

class BaseBackend(object):

    def send(self, targets, notify_type, media, extra_data={}):
        """
        Sends a message to the given users.

        targets: The notification target model instance. Normally a user.
        notify_type: The notify type
        media: The media name
        extra_context: A dictionary containing extra data that is sent along with
                       the notification
        Returns the number of notifications sent.
        """
        num_sent = 0
        for target in targets:
            num_sent += self._send(
                target=target,
                notify_type=notify_type,
                media=media,
                extra_data=extra_data,
            )
        return num_sent

    def _send(self, target, notify_type, media, extra_data={}):
        raise NotImplemented('You must implement the _send() method in from the BaseBackend class.')
