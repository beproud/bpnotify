#:coding=utf8:

from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase

from beproud.django.notify.tests.base import TestBase
from beproud.django.notify.models import Notification
from beproud.django.notify.api import *

class BasicNotifyTest(TestBase, TestCase):
    fixtures = ['test_users.json']
    
    def test_sending(self):
        user = User.objects.get(pk=2)
        items_sent = notify(user, 'private_msg', extra_data={"spam": "eggs"})
        self.assertEquals(items_sent, 2)

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
