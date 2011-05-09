========================
Cached DB Storage
========================

.. module:: beproud.django.notify.storage.cached_db

.. class:: beproud.django.notify.storage.cached_db.CachedDBStorage

The cached db storage storage is identical in functionality to the
:class:`DBStorage <beproud.django.notify.storage.db.DBStorage>` backend,
storing setting data in the database using the :class:`NotifySetting
<beproud.django.notify.models.NotifySetting>` model. However, the cached db
storage caches settings data using Django's cache framework.

The cached db storage is the default settings storage backend and is
recommended over the :class:`DBStorage
<beproud.django.notify.storage.db.DBStorage>` backend unless the site does not
use the Django's cache framework.
