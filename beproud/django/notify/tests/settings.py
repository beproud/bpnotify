# Django3では、標準のdjango.conf.global_settingsの定数をオーバーライドすると例外が発生する場合がある。
# https://github.com/django/django/blob/70035fb0444ae7c01613374212ca5e3c27c9782c/django/conf/__init__.py#L188
# そのため、testではdjango.conf.global_settingsを直接利用せず、このtest用settings定数を使用する。

import os
import celery

SECRET_KEY = "SECRET"
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'beproud.django.notify',
)

# kombu.exceptions.EncodeError: Object of type User is not JSON serializable エラーを抑止する
# (参考)
#   https://github.com/celery/celery/issues/5922
#   https://stackoverflow.com/questions/49373825/kombu-exceptions-encodeerror-user-is-not-json-serializable
CELERY_TASK_SERIALIZER = "pickle"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

BASE_PATH = os.path.dirname(__file__)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_PATH, 'beproud', 'django', 'notify', 'tests', 'templates')
        ],
    },
]

CELERY_TASK_ALWAYS_EAGER = True

BPNOTIFY_MEDIA = {
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
BPNOTIFY_SETTINGS_STORAGE = 'beproud.django.notify.storage.db.DBStorage'

# The name of the class to use to run the test suite
# TEST_RUNNER = 'django.test.runner.DiscoverRunner'

app = celery.Celery()
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: INSTALLED_APPS)
