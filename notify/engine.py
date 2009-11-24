#:coding=utf8:
from datetime import datetime

from django.contrib.sites.models import Site
from django.conf import settings

import conf
from models import *

def render_notification(notification, template, extra_context={}):
    context = {
        'notification': notification,
    }
    context.update(notification.extra_data)
    context.update(extra_context)
    return render_notice_type(notification.notice_type, template, context)

def render_notice_type(notice_type, template, extra_context={}):
    from django.template.loader import render_to_string
    context = {
        'domain': settings.DOMAIN, 
    }
    context.update(extra_context)

    return render_to_string('notify/%s/%s' % (notice_type.lower(), template), context)

def send_notification(users, notice_type, extra_context={}, target_id=None, origin_id=None, ctime=None, exclude_media=[]):
    if 'celery' in settings.INSTALLED_APPS:
        import tasks
        return tasks.SendNotification.delay(
            users=users,
            notice_type=notice_type,
            extra_context=extra_context,
            target_id=target_id,
            origin_id=origin_id,
            ctime=ctime,
            exclude_media=exclude_media,
        )
    else:
        return send_notification_now(users, notice_type, extra_context, target_id, origin_id)

def send_notification_now(users, notice_type, extra_context={}, target_id=None, origin_id=None, ctime=None, exclude_media=[]):
    u"""
    通知を送る
    """
    if isinstance(users, User):
        users = [users]
    for user in users:
        for media in conf.NOTICE_MEDIA: # TODO ここのコードおかしいぞ
            if media[0] not in exclude_media and get_notification_setting(user, notice_type, media[0]):
                notification = Notification.objects.create(
                    user = user,
                    notice_type = notice_type,
                    media = media[0],
                    extra_data = extra_context,
                    target_id = target_id,
                    origin_id = origin_id,
                    ctime = ctime if ctime else datetime.now(),
                )

                if media[0] == 'EMAIL':
                    from mailer import send_mail
                    context = {
                        'notification': notification,
                    }
                    context.update(extra_context)
                    send_mail('notify/%s/email.txt' % notice_type.lower(), user, context)

def get_notification_setting(user, notice_type, media):
    u"""
    このユーザにこの通知をこのメディアで送るかを返す
    """
    send = False

    #NOTICE_TYPEをチェック
    type_ok = False
    if not conf.NOTICE_TYPES_DICT.has_key(notice_type):
        return False # TODO raise ?
    
    default_settings = conf.MEDIA_DEFAULTS.get(notice_type)
    if default_settings:
        send = bool(default_settings.get(media)) if media in default_settings else False

    try:
        send = NotificationSetting.objects.get(
            user=user,
            notice_type = notice_type,
            media = media,
        ).send
    except NotificationSetting.DoesNotExist:
        pass

    return send

def set_notification_setting(user, notice_type, media, send):
    try:
        setting = NotificationSetting.objects.get(
            user = user,
            notice_type = notice_type,
            media = media,
        )
        setting.send = send
    except NotificationSetting.DoesNotExist:
        setting = NotificationSetting(
            user = user,
            notice_type = notice_type,
            media = media,
            send = send,
        )
    return setting.save()

def view_notification(**kwargs):
    # signalなどに対応するため、一個一個削除
    for n in Notification.objects.filter(**kwargs):
        n.delete()
