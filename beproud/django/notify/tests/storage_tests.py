#:coding=utf8:

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings
from django.test import TestCase

from beproud.django.notify.tests.base import TestBase

from beproud.django.notify.storage import get_storage
from beproud.django.notify.storage.model import *
from beproud.django.notify.models import NotifySetting
from beproud.django.notify.api import *

__all__ = (
    'ModelStorageTest',
)

class ModelStorageTest(TestBase, TestCase):
    fixtures = ['test_users.json']

    BPNOTIFY_SETTINGS_STORAGE='beproud.django.notify.storage.model.ModelStorage'
    
    def test_model_storage_get(self):

        user = User.objects.get(pk=2)
        NotifySetting.objects.create(
            target_content_type = ContentType.objects.get_for_model(user),
            target_object_id = user.pk,
            notify_type = 'new_user',
            media = 'news',
            send = True,
        )

        storage = get_storage(self.BPNOTIFY_SETTINGS_STORAGE)
        self.assertTrue(storage.get(user, 'new_user', 'news'))

    def test_model_storage_get_default(self):

        user = User.objects.get(pk=2)
        NotifySetting.objects.create(
            target_content_type = ContentType.objects.get_for_model(user),
            target_object_id = user.pk,
            notify_type = 'new_user',
            media = 'news',
            send = True,
        )

        storage = get_storage(self.BPNOTIFY_SETTINGS_STORAGE)
        self.assertFalse(storage.get(user, 'private_message', 'news', False))
        self.assertTrue(storage.get(user, 'private_message', 'news', True))
        self.assertTrue(storage.get(user, 'new_user', 'news', False))

    def test_model_storage_set(self):
        user = User.objects.get(pk=2)
        storage = get_storage(self.BPNOTIFY_SETTINGS_STORAGE)

        self.assertFalse(storage.get(user, 'new_user', 'news', False))

        storage.set(user, 'new_user', 'news', True)

        try:
            setting = NotifySetting.objects.get(
                target_content_type = ContentType.objects.get_for_model(user),
                target_object_id = user.pk,
                notify_type = 'new_user',
                media = 'news',
            )
            self.assertTrue(setting.send, u'NotifySetting set to an false when it should be true!')

        except NotifySetting.DoesNotExist:
            self.fail(u'NotifySetting record was not created!')


        storage.set(user, 'new_user', 'news', False)

        try:
            setting = NotifySetting.objects.get(
                target_content_type = ContentType.objects.get_for_model(user),
                target_object_id = user.pk,
                notify_type = 'new_user',
                media = 'news',
            )
            self.assertFalse(setting.send, u'NotifySetting record was not updated!')

        except NotifySetting.DoesNotExist:
            self.fail(u'NotifySetting record was not created!')

    def test_settings_api(self):
        user = User.objects.get(pk=2)

        # Test get default settings
        self.assertTrue(get_notify_setting(user, 'new_user', 'news'))
        self.assertFalse(get_notify_setting(user, 'followed', 'news'))
        self.assertFalse(get_notify_setting(user, 'new_user', 'news', False))
        self.assertTrue(get_notify_setting(user, 'new_user', 'news', True))

        # Unknown types
        self.assertFalse(get_notify_setting(user, 'unknown', 'private_messages'))
        self.assertFalse(get_notify_setting(user, 'some_type', 'private_messages'))
        self.assertTrue(get_notify_setting(user, 'some_type', 'private_messages', True))

        # Unknown Media
        self.assertFalse(get_notify_setting(user, 'new_user', 'unknown'))
        self.assertFalse(get_notify_setting(user, 'new_user', 'some_media'))
        self.assertTrue(get_notify_setting(user, 'new_user', 'some_media', True))


        # Test Set 
        self.assertTrue(set_notify_setting(user, 'private_message', 'news', True))
        self.assertTrue(get_notify_setting(user, 'private_message', 'news'))

        self.assertTrue(set_notify_setting(user, 'private_message', 'news', False))
        self.assertFalse(get_notify_setting(user, 'private_message', 'news', True))
