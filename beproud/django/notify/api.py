#:coding=utf8:

from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_unicode
from django.utils.functional import memoize

__all__ = (
    'notify',
    'notify_now',
    'get_notify_setting',
    'set_notify_setting',
)

def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    # force the import name to automatically convert to strings
    if isinstance(import_name, unicode):
        import_name = str(import_name)
    try:
        if ':' in import_name:
            module, obj = import_name.split(':', 1)
        elif '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)
        # __import__ is not able to handle unicode strings in the fromlist
        # if the module is a package
        if isinstance(obj, unicode):
            obj = obj.encode('utf-8')
        return getattr(__import__(module, None, None, [obj]), obj)
    except (ImportError, AttributeError):
        if not silent:
            raise

def _capfirst(value):
    if value:
        value = force_unicode(value)
        return "%s%s" % (value[0].upper(), value[1:])
    else:
        return value

_media_map_cache = {}
def _get_media_map():
    from django.conf import settings

    media_settings = getattr(settings, 'BPNOTIFY_MEDIA', {})
    media_map = {}
    for name in media_settings:
        media_map[name] = {
            'verbose_name': media_settings[name].get('verbose_name', _capfirst(name)),
            'default_types': media_settings[name].get('default_types', ()),
            'backends': [load_backend(path) for path in media_settings[name].get('backends', ())],
        }
    return media_map
_get_media_map = memoize(_get_media_map, _media_map_cache, 0)

_notify_backend_cache = {}
def load_backend(backend_path):
    """
    Load the auth backend with the given name
    """
    try:
        return import_string(backend_path)
    except (ImportError, AttributeError), e:
        raise ImproperlyConfigured('Error importing notify backend %s: "%s"' % (backend_path, e))
    except ValueError, e:
        raise ImproperlyConfigured('Error importing notify backends. Is BPNOTIFY_MEDIA a correctly defined dict?')
load_backend = memoize(load_backend, _notify_backend_cache, 1)

def notify(targets, notify_type, extra_data={}, include_media=None, exclude_media=[]):
    if 'djcelery' in settings.INSTALLED_APPS:
        from django.contrib.contenttypes.models import ContentType
        from beproud.django.notify import tasks

        return tasks.Notify.delay(
            targets=[(ContentType.get_for_model(target).pk, target.pk) for target in targets],
            notify_type=notify_type,
            extra_data=extra_data,
            include_media=include_media,
            exclude_media=exclude_media,
        )
    else:
        return notify_now(targets, notify_type, extra_data, include_media, exclude_media)

def notify_now(targets, notify_type, extra_data={}, include_media=None, exclude_media=[]):
    u"""
    Send a notification to the appropriate media based on the notify type.

    include_media: A list of media names to include.

    """
    if not hasattr(targets, '__iter__'):
        targets = [targets]

    media_map = _get_media_map()
    if include_media:
        include_media = [media for media in include_media if media in media_map]
    else:
        include_media = [media for media in media_map if media not in exclude_media]

    for media_name in include_media:
        media_settings = media_map[media_name]

        targets_to_send = filter(lambda t: get_notify_setting(t, notify_type, media_name), targets)
        if targets_to_send:
            for backends in media_settings['backends']:
                backend.send(targets_to_send, notify_type, media, extra_content)

def get_notify_setting(target, notify_type, media_name):
    # TODO
    media_map = _get_media_map()
    return notify_type in media_map['default_types']

def set_notify_setting(target, notify_type, media_name, send):
    pass