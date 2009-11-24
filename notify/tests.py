#:coding=utf8:

from django.core import mail
from test import TestCase

from users.models import User,Customer

import conf
from mail import *
from engine import *

class BasicNotificationTest(TestCase):
    fixtures = ['basic_users.json']

    def setUp(self):
        conf.NOTICE_TYPES = list(conf.NOTICE_TYPES)
        conf.NOTICE_TYPES.append(
            ('TEST_NOTICE', u'テスト通知'),
        )
        conf.NOTICE_TYPES_DICT['TEST_NOTICE'] = u'テスト通知'
        conf.MEDIA_DEFAULTS['TEST_NOTICE'] = {
            'EMAIL': True,
            'RECENT_EVENTS': True,
        }
        
        self.customer = Customer.objects.get(pk=2)
        self.users = list(User.objects.be().filter(customer=self.customer))
    
    def test_sending(self):
        send_notification(self.users, 'TEST_NOTICE')

        self.assertEquals(len(mail.outbox), len(self.users))
        for obj in mail.outbox:
          message = obj.message() # エラーがないかをチェック
