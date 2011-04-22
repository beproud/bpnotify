#:coding=utf8:

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import jsonfield

from beproud.django.notify.api import _get_media_map

__all__ = (
    'Notification',
    'NoticeSetting',
)

media_map = _get_media_map()
MEDIA_CHOICES = [(name, data['verbose_name']) for name, data in media_map.iteritems()]

class Notification(models.Model):
    target_content_type = models.ForeignKey(ContentType, verbose_name=_('content type id'))
    target_object_id = models.PositiveIntegerField(_('target id'))
    target = generic.GenericForeignKey('content_type', 'object_id')


    notify_type = models.CharField(_('notify type'), max_length=30, db_index=True)
    media = models.CharField(_('media'), max_length=30, choices=MEDIA_CHOICES, db_index=True)

    extra_data = jsonfield.JSONField(_('extra data'), null=True, blank=True)

    ctime = models.DateTimeField(_('created'), default=datetime.now)

    @models.permalink
    def get_absolute_url(self):
        return ('view_notification' (), {
            'id': self.id,
        })
    
    def __unicode__(self):
        return "%s (%s, %s)" % (self.target, self.notice_type, self.media)

    class Meta:
        ordering=('-ctime',)

class NotifySetting(models.Model):
    target_content_type = models.ForeignKey(ContentType, verbose_name=_('content type id'))
    target_object_id = models.PositiveIntegerField(_('target id'))
    target = generic.GenericForeignKey('content_type', 'object_id')

    notify_type = models.CharField(_('notify type'), max_length=30, db_index=True)
    media = models.CharField(_('media'), max_length=30, choices=MEDIA_CHOICES, db_index=True)
    send = models.BooleanField(_('send?'))

    def __unicode__(self):
        return "%s (%s, %s, %s)" % (self.target, self.notice_type, self.media, send and 'send' or 'no send')
