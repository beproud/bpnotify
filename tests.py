import os
import sys
import django
import celery

import test_settings

BASE_PATH = os.path.dirname(__file__)


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    # os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    os.environ["DJANGO_SETTINGS_MODULE"] = "test_settings"

    app = celery.Celery()
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks(lambda: test_settings.INSTALLED_APPS)

    django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(test_settings)

    test_runner = test_runner()
    
    # See: https://docs.djangoproject.com/en/1.6/topics/testing/overview/#running-tests
    failures = test_runner.run_tests(['beproud.django.notify.tests'])

    sys.exit(failures)

if __name__ == '__main__':
    main()
