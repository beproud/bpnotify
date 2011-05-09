==========================
Sending Notifications
==========================

.. module:: beproud.django.notify.api


Sending notifications is fairly straitforward. Notifications are sent via the
:func:`notify() <beproud.django.notify.api.notify>` function. Though there are
some variations on how to call this function, the functionality does not change
a great deal.

.. function:: notify(targets, notify_type, extra_data={}, include_media=None, exclude_media=[])

The notify method is called to send a notification of the given type to a
iterable of targets. If the targets option is not iterable then it is treated
as a single target. The notification will be send asynchronously using the
Celery task queue API if ``djcelery`` is installed. Otherwise the notification
is sent synchronously using the :func:`notify_now()
<beproud.django.notify.api.notify_now>` function.

.. function:: notify_now(targets, notify_type, extra_data={}, include_media=None, exclude_media=[])

If you wish to bypass sending notifications asynchronously then you can call
the :func:`notify_now() <beproud.django.notify.api.notify_now>` function
directly.

Sending a Simple Notification
-----------------------------------

Here is an example of sending a notification to the current Django user
in a view.

.. code-block:: python

    from django.http import HttpResponse
    from django.contrib.auth.decorators import login_required
    from beproud.django.notify import notify

    @login_required
    def hello_world(request):
        notify(request.user, "hello_world")
        return HttpResponse("<html><body>Hello World!</body></html>")

In this case, the notification will be sent to all media types for which the
given notify type "hello_world" is listed in the :ref:`default_types
<settings-media-default-types>` in your :attr:`settings.BPNOTIFY_MEDIA` setting
as well as any media for which the target user's settings specify that it
should be sent. i.e. Even if "hello_world" is not listed in :ref:`default_types
<settings-media-default-types>` for a particular media type, the notification
will still be sent if the user's setting for the "hello_world" notify type and
the media type specify that the notification should be sent.

Excluding Media
---------------------------------

By default bpnotify will attempt to send notifications to all media types.
However, there may be some cases where you know which media you would like to
send the notification to, or where you would like to exclude one or two media
types.  In those cases, you can specify which media the notification should be
delivered to by passing the ``include_media`` or ``exclude_media`` parameters
to the :func:`notify() <beproud.django.notify.api.notify>` function.

.. code-block:: python

    # Send only to the "mail" media type.
    notify(request.user, "welcome", include_media=["mail"])

    # Send to all media types except the "profile" and "notices" media types.
    notify(request.user, "welcome", exclude_media=["profile", "notices"])

Retrieving Notifications
-----------------------------------

The notifications API supports retrieving notifications from backends that
support retrieval. For this the :func:`get_notifications()
<beproud.django.notify.api.get_notifications>` function is provided.  The
:func:`get_notifications() <beproud.django.notify.api.get_notifications>`
function retrieves notifications from the first backend that supports retrieval
for the given media type.

.. function:: get_notifications(target, media, start=None, end=None)

The :func:`get_notifications() <beproud.django.notify.api.get_notifications>`
method retrieves notifications sent to a specific target and media type and
returns them as a python dictionary in the following format and in the reverse
order they were sent (newest first):

.. code-block:: python

    >>> get_notifications(user, "private_messages")
    [{
        'target': User: monty,
        'notify_type': "private_message",
        'media': "private_messages",
        'extra_data': {
            'spam': 'eggs',
        }
        'ctime': datetime.datetime(2011, 5, 8, 14, 06, 52, 882674)
    },
    ...
    ]

The :func:`get_notifications() <beproud.django.notify.api.get_notifications>`
function also supports specifying the start and end index of the notifications
to be retrieved as the ``start`` and ``end`` arguments.

Getting and Updating Notification Settings
-------------------------------------------------

The setting of whether to send or not send a particular notification can be
retrieved using the :func:`get_notify_setting()
<beproud.django.notify.api.get_notify_setting>` function. Each setting is
unique for the target, notify type, and media type. If no setting has been set
yet then the given default value is returned. If not default value is specified
then the function returns None.

.. function:: get_notify_setting(target, notify_type, media_name, default=None)

:func:`get_notify_setting() <beproud.django.notify.api.get_notify_setting>` 
returns a boolean indicating if notifications to the given target with
the given notify type routed to the given media will be sent.

Settings can be updated by using the :func:`set_notify_setting()
<beproud.django.notify.api.set_notify_setting>` function. The send argument is
a boolean. If True then notifications sent to the target with the given
notify type that are routed to the given media will be sent. If False
notifications are not sent.

.. function:: set_notify_setting(target, notify_type, media_name, send)

Setting are stored and retrieved using the settings storage backend specified
in the application's ``settings.py`` in the
:attr:`settings.BPNOTIFY_SETTINGS_BACKEND` setting.
