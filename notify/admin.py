#:coding=utf8:

from django.contrib import admin

from models import *

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','notice_type','media')
    list_filter = ('notice_type', 'media')
    ordering = ('-ctime',)

class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('user','notice_type','media', 'send')
    list_filter = ('notice_type', 'media')
    ordering = ('user',)

admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationSetting, NotificationSettingAdmin)
