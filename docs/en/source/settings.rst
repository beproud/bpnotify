:mod:`settings` -- bpauth Settings
================================================================

.. module:: settings


.. attribute:: BPNOTIFY_MEDIA

    The media and routing settings for bpnotify. BPNOTIFY_MEDIA is a python
    dictionary whose key is the media name and whose value is another python
    dictionary of settings for that media.

    Here is some example media settings:

    .. code-block:: python 

        BPNOTIFY_MEDIA = {
            "news": {
                "verbose_name": "News",
                "default_types": ("new_user", "follow", "private_msg"),
                "backends": (
                    "beproud.django.notify.backends.model.ModelBackend",
                ),
            },
            "private_messages": {
                "verbose_name": "Private Message",
                "default_types": ("private_msg",),
                "backends": (
                    "beproud.django.notify.backends.model.ModelBackend",
                    "beproud.django.notify.backends.mail.EmailBackend",
                ),
            },
        }

    The :attr:`settings.BPNOTIFY_MEDIA` setting supports three settings for
    each media.

    .. _settings-media-default-types:

    **verbose_name**

    The verbose name of the media. This could be used for settings pages or
    elsewhere in the application. It is optional and defaults to a capitalized
    version of the media name specified in the key.

    **default_types**

    A list of notify types that are sent to this media by default. Sending
    notifications to these types can be disabled via the settings API on a per
    user basis. Additional notify types can also be sent by setting the type to
    be sent via the settings API. The same type can be listed in multiple media
    types.

    This setting is also optional and defaults to an empty list.

    **backends**

    A list of paths to notification backends to be used to send the notification.
    Any number of notification backends can be set here. The notification will
    be sent to each notification backend.

    This setting is optional and defaults to an empty list though without
    setting the any backends any notifications sent to that media will
    be ignored.



.. attribute:: BPNOTIFY_SETTINGS_STORAGE

    The backend for the notification settings. This is set to a path to a
    storage backend class. The default is the
    ``beproud.django.notify.storage.cached_db.CachedDBStorage`` as shown below.

    .. code-block:: python

        BPNOTIFY_SETTINGS_STORAGE="beproud.django.notify.storage.cached_db.CachedDBStorage"


