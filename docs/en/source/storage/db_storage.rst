======================
Database Storage
======================

.. module:: beproud.django.notify.storage.db

.. class:: beproud.django.notify.storage.db.DBStorage

The Database storage stores settings data in the database using the
:class:`NotifySetting <beproud.django.notify.models.NotifySetting>` model.

Since the :class:`DBStorage <beproud.django.notify.storage.db.DBStorage>`
backend can generate a lot of SQL queries it is recommended to used the
:class:`CachedDBStorage
<beproud.django.notify.storage.cached_db.CachedDBStorage>` backend unless the
application does not use the Django cache.

NotifySetting Model Reference
------------------------------------

.. class:: beproud.django.notify.models.NotifySetting

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

    .. attribute:: send

        A boolean attribute specifying whether notifications of the
        notify_type and media are sent to the target.
