#:coding=utf8:

from django.core import mail
from django.conf import settings
from test import TestCase

from users.models import User,Customer

from mail import *
from api import *

class BaseTest(object):
    def tearDown(self):
        for attr in ["NOTICE_TYPES", "NOTICE_MEDIA",
                     "NOTICE_MEDIA_MAP", "NOTICE_MEDIA_DEFAULTS"]:
        if hasattr(settings, attr):
            delattr(settings, attr)

class BasicNoticeTest(BaseTest, TestCase):
    fixtures = ['basic_users.json']

    def setUp(self):
        settings.NOTICE_TYPES = (
            ('TEST_NOTICE', u'テスト通知'),
        )
        settings.NOTICE_MEDIA = {
            "TEST_MEDIA": {
                "verbose_name": "My Test Media",
                "backends": ['model'],
            }
        }
        settings.MEDIA_DEFAULTS = {
            'TEST_NOTICE': {
                'TEST_MEDIA': True,
            }
        }
    
    def test_sending(self):
        user = User.objects.get(pk=2)
        items_sent = send_notification(user, 'TEST_NOTICE')
        self.assertEquals(items_sent, 1)

        all_notices = Notification.objects.all()
        self.assertEquals(len(all_notices), 1)
