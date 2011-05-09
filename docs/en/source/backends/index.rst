========================
Notification Backends
========================

Notification backends do the work of sending/storing notifications
sent by the application. The bpnotify API will route notifications to
the appropriate backends.

bpnotify includes a few backends that can be used to send notifications.
You can also write custom notification backends to support any kind
of implementation that is suited to your application.

.. toctree::
  :numbered:
  :maxdepth: 2

  model_backend
  mail_backend
..    writing_backends
