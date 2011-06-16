#:coding=utf8:

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

import jsonfield

from beproud.django.notify.api import _get_media_map

__all__ = (
    'Notification',
    'NotifySetting',
)

media_map = _get_media_map()
MEDIA_CHOICES = [(name, data['verbose_name']) for name, data in media_map.iteritems()]

class NotificationManager(models.Manager):
    def get_for_target(self, target):
        return self.filter(
            target_content_type = ContentType.objects.get_for_model(target),
            target_object_id = target.pk,
        )

class Notification(models.Model):
    target_content_type = models.ForeignKey(ContentType, verbose_name=_('content type id'), db_index=True, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(_('target id'), db_index=True, null=True, blank=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')


    notify_type = models.CharField(_('notify type'), max_length=30, db_index=True)
    media = models.CharField(_('media'), max_length=30, choices=MEDIA_CHOICES, db_index=True)

    extra_data = jsonfield.JSONField(_('extra data'), null=True, blank=True)

    ctime = models.DateTimeField(_('created'), auto_now_add=True, db_index=True)

    objects = NotificationManager()

    def __unicode__(self):
        return "%s (%s, %s)" % (self.target, self.notify_type, self.media)

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
        return "%s (%s, %s, %s)" % (self.target, self.notify_type, self.media, send and 'send' or 'no send')

    class Meta:
        unique_together = ('target_content_type', 'target_object_id', 'notify_type', 'media')
