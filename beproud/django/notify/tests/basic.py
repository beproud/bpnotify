#:coding=utf8:

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase

from beproud.django.notify.tests.base import TestBase
from beproud.django.notify.models import Notification
from beproud.django.notify.api import *

__all__ = ('BasicNotifyTest',)

class BasicNotifyTest(TestBase, TestCase):
    fixtures = ['test_users.json']
    
    def test_sending_model(self):
        user = User.objects.get(pk=2)
        items_sent = notify(user, 'follow', extra_data={"followed": "eggs"})
        # 1 news model
        self.assertEquals(items_sent, 1)

        news = Notification.objects.filter(media='news')
        self.assertEquals(len(news), 1)
        self.assertEquals(news[0].media, 'news')
        self.assertEquals(news[0].notify_type, 'follow')
        self.assertEquals(news[0].target, user)
        self.assertEquals(news[0].extra_data.get('followed'), 'eggs')
        
        private_messages = Notification.objects.exclude(media='news')
        self.assertEquals(len(private_messages), 0)

    def test_sending_model_types(self):
        user = User.objects.get(pk=2)
        items_sent = notify(user, 'private_msg', extra_data={"spam": "eggs"})
        # 1 private_messages model
        # 1 private_messages mail
        # 1 news model
        self.assertEquals(items_sent, 3)

        private_messages = Notification.objects.filter(media='private_messages')
        self.assertEquals(len(private_messages), 1)
        self.assertEquals(private_messages[0].media, 'private_messages')
        self.assertEquals(private_messages[0].notify_type, 'private_msg')
        self.assertEquals(private_messages[0].target, user)
        self.assertEquals(private_messages[0].extra_data.get('spam'), 'eggs')

        news = Notification.objects.filter(media='news')
        self.assertEquals(len(news), 1)
        self.assertEquals(news[0].media, 'news')
        self.assertEquals(news[0].notify_type, 'private_msg')
        self.assertEquals(news[0].target, user)
        self.assertEquals(news[0].extra_data.get('spam'), 'eggs')

    def test_sending_model_multi(self):
        user = [User.objects.get(pk=1), User.objects.get(pk=2)]
        items_sent = notify(user, 'private_msg', extra_data={"spam": "eggs"})

        # 2 private_messages model
        # 2 private_messages mail
        # 2 news model
        self.assertEquals(items_sent, 6)

        # User2
        private_messages = Notification.objects.filter(
            media='private_messages',
            target_content_type=ContentType.objects.get_for_model(user[0]),
            target_object_id=user[0].id,
        )
        self.assertEquals(len(private_messages), 1)
        self.assertEquals(private_messages[0].media, 'private_messages')
        self.assertEquals(private_messages[0].notify_type, 'private_msg')
        self.assertEquals(private_messages[0].target, user[0])
        self.assertEquals(private_messages[0].extra_data.get('spam'), 'eggs')

        news = Notification.objects.filter(
            media='news',
            target_content_type=ContentType.objects.get_for_model(user[0]),
            target_object_id=user[0].id,
        )
        self.assertEquals(len(news), 1)
        self.assertEquals(news[0].media, 'news')
        self.assertEquals(news[0].notify_type, 'private_msg')
        self.assertEquals(news[0].target, user[0])
        self.assertEquals(news[0].extra_data.get('spam'), 'eggs')

        # User2
        private_messages = Notification.objects.filter(
            media='private_messages',
            target_content_type=ContentType.objects.get_for_model(user[1]),
            target_object_id=user[1].id,
        )
        self.assertEquals(len(private_messages), 1)
        self.assertEquals(private_messages[0].media, 'private_messages')
        self.assertEquals(private_messages[0].notify_type, 'private_msg')
        self.assertEquals(private_messages[0].target, user[1])
        self.assertEquals(private_messages[0].extra_data.get('spam'), 'eggs')

        news = Notification.objects.filter(
            media='news',
            target_content_type=ContentType.objects.get_for_model(user[1]),
            target_object_id=user[1].id,
        )
        self.assertEquals(len(news), 1)
        self.assertEquals(news[0].media, 'news')
        self.assertEquals(news[0].notify_type, 'private_msg')
        self.assertEquals(news[0].target, user[1])
        self.assertEquals(news[0].extra_data.get('spam'), 'eggs')


    def test_sending_with_settings(self):
        user = [User.objects.get(pk=1), User.objects.get(pk=2)]

        items_sent = notify(user, 'followed', extra_data={"spam": "eggs"})
        self.assertEquals(items_sent, 0)

        self.assertTrue(set_notify_setting(user[0], 'followed', 'news', True))
        items_sent = notify(user, 'followed', extra_data={"spam": "eggs"})

        # 1 news model
        self.assertEquals(items_sent, 1)

