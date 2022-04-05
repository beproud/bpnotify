SECRET_KEY = "SECRET"
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'beproud.django.notify',
)

# TODO: 次のコードの役割を確認
CELERY_TASK_SERIALIZER = "pickle"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

import os
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
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

