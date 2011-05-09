========================
Settings Storage
========================

Notification settings are stored by the storage backend class specified by the
:attr:`settings.BPNOTIFY_SETTINGS_STORAGE` setting in ``settings.py``. Stored
notification settings hold information about whether notifications of a
specific notify type and media type are sent to a target.

.. toctree::
  :numbered:
  :maxdepth: 2

  db_storage 
  cached_db_storage 
..    writing_storage
