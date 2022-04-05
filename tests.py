import os
import sys
import django
import celery


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

    # TODO: 次のコードの役割を確認
    global_settings.CELERY_TASK_SERIALIZER = "pickle"

    global_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    #global_settings.ROOT_URLCONF = 'notify.tests.urls'
    global_settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_PATH, 'beproud', 'django', 'notify', 'tests', 'templates')
            ],
        },
    ]

    global_settings.CELERY_TASK_ALWAYS_EAGER = True

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

    app = celery.Celery()
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks(lambda: global_settings.INSTALLED_APPS)

    django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    test_runner = test_runner()
    
    # See: https://docs.djangoproject.com/en/1.6/topics/testing/overview/#running-tests
    failures = test_runner.run_tests(['beproud.django.notify.tests'])

    sys.exit(failures)

if __name__ == '__main__':
    main()
