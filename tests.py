import os
import sys
import django


BASE_PATH = os.path.dirname(__file__)


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.SECRET_KEY = "SECRET"
    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'beproud.django.notify',
    )

    global_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    #global_settings.ROOT_URLCONF = 'notify.tests.urls'
    global_settings.TEMPLATE_DIRS = (
        os.path.join(BASE_PATH, 'beproud', 'django', 'notify', 'tests', 'templates'),
    )

    global_settings.CELERY_ALWAYS_EAGER = True

    global_settings.BPNOTIFY_MEDIA = {
        "news": {
            "verbose_name": "News",
            "default_types": ("new_user", "follow", "private_msg"),
            "backends": (
                "beproud.django.notify.backends.model.ModelBackend",
            ),
        },
        "private_messages": {
            "verbose_name": "Private Message",
            "default_types": ("private_msg", "notify_type_with_length_over_thirty"),
            "backends": (
                "beproud.django.notify.backends.model.ModelBackend",
                "beproud.django.notify.backends.mail.EmailBackend",
            ),
        },
    }
    global_settings.BPNOTIFY_SETTINGS_STORAGE = 'beproud.django.notify.storage.db.DBStorage'

    import celery
    if celery.VERSION >= (3, 1):
        app = celery.Celery()
        app.config_from_object('django.conf:settings')
        app.autodiscover_tasks(lambda: global_settings.INSTALLED_APPS)
    else:
        global_settings.INSTALLED_APPS += ('djcelery',)

    if django.VERSION > (1, 7):
        django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1, 2):
        test_runner = test_runner()
        if django.VERSION > (1, 6):
            # See: https://docs.djangoproject.com/en/1.6/topics/testing/overview/#running-tests
            failures = test_runner.run_tests(['beproud.django.notify'])
        else:
            failures = test_runner.run_tests(['notify'])

    else:
        failures = test_runner(['notify'], verbosity=1)

    sys.exit(failures)

if __name__ == '__main__':
    main()
