==========================
bpnotify Documentation
==========================

What is bpnotify?
--------------------------

bpnotify is a Django application for sending and storing
notifications. It is meant as a more flexable alternative to
something like django-notifications.

Overview
----------------------

bpnotify allows developers to send notifications to any kind of target model
object.  Usually this will be a user or other kind of model instance but it can
be any kind of model instance.  The API itself doesn't make any assumptions
about the target object's model class however the default provided backends
assume that the target is a Django model instance with a pk.

Features
----------------------

bpnotify supports the following features.

Notification Routing
++++++++++++++++++++++++++++++++++++

Much like django-notifications, bpnotify routes notifications of certain
"notify types" to a specific "media".

Notify types are the type of notification. For example, in a social network, a
signup welcome notification, a notification saying someone followed you, or a
notification saying that someone sent you a private message.

Media are destinations for the notifications. These can include for example,
a user's activity stream or a user's notification area. Or it can simply be
email.

Notify types can be sent to any number of media as defined by the default
routing in the applications ``settings.py`` and by the user's notification
settings.

Notification Settings
+++++++++++++++++++++++++++++++

A settings API is provided to allow user's to set whether they would like
to recieve notifications of a specific type to a specific media. If a setting
for a notify type and media is set to not deliver the notification, the
notification will not be sent even if the :ref:`notify()` method is called.

The :ref:`notify()` method checks the settings for the user when sending
notifications and will not send to user's who have turned their settings
off.

Settings are stored using a storage backend. The storage backend supports a
simple key/value like API which lends itself well to key/value storage and
caching. A default cached_db backend for saving settings in the database is
included.

Notification Backends
++++++++++++++++++++++++++++

Any number of notification backends can be written to allow sending of
notifications. bpnotify includes a few backends to allow for sending
email notifications, and for storing notifications in the database.

Backends support a simple API for sending notifications. Notifications
can also be retrieved through the API by backends supporting retrieval.

目次:

.. toctree::
  :numbered:
  :maxdepth: 1

  install
  settings

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
