#:coding=utf8:

from django.contrib import admin

from beproud.django.notify.models import Notification, NoticeSetting

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('target_content_type','target_object_id', 'notice_type','media')
    list_filter = ('target_content_type', 'notice_type', 'media')
    ordering = ('-ctime',)

class NotifySettingAdmin(admin.ModelAdmin):
    list_display = ('target','notice_type','media','send')
    list_filter = ('target_content_type','notice_type', 'media')
    ordering = ('target_content_type','target_object_id')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotifySetting, NotifySettingAdmin)
