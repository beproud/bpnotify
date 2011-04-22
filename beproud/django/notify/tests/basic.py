#:coding=utf8:

from django.conf import settings
from django.test import TestCase

from beproud.django.notify.tests.base import TestBase
from beproud.django.notify.api import *

class BasicNotifyType(NotifyType):
    verbose_name = u'Basic Notification'

register_type('basic', BasicNotifyType)

class BasicNoticeTest(BaseTestCase, TestCase):
    
    def test_sending(self):
        user = User.objects.get(pk=2)
        items_sent = send_notification(user, 'TEST_NOTICE')
        self.assertEquals(items_sent, 1)

        all_notices = Notification.objects.all()
        self.assertEquals(len(all_notices), 1)
