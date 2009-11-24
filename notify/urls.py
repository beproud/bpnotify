#vim:coding=utf8
from django.conf.urls.defaults import *
urlpatterns = patterns('notify.views',
    url(r'^view_notice$', 'view_notification', name="view_notification"),
)
