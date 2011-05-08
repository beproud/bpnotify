======================
Model Backend
======================

.. module:: beproud.django.notify.backends.model

The model backend sends notifications by saving themy in the database
using the :class:`Notification <beproud.django.notify.models.Notification>` model.

Notification Model Reference
------------------------------------

.. class:: beproud.django.notify.models.Notification

    .. attribute:: target
    
        A GenericForeignKey for the target model object.
        The target is retrieved using a automatically using
        the ``target_content_type`` and ``target_object_id`` fields.

    .. attribute:: target_content_type
    
        A ForeignKey to the content type of the target object.

    .. attribute:: target_object_id

        The target object's id.

    .. attribute:: notify_type

        The notify type of the notification.

    .. attribute:: media
        
        The media type of the notification.

    .. attribute:: extra_data

        A JSONField of extra data sent along with the notification. The
        extra_data is a dictionary stored in the database as JSON.

    .. attribute:: ctime

        A datetime specifying the time that the notification was sent.
