#vim:fileencoding=utf8

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from mysql_replicated2.decorators import use_master

from account.decorators import login_required
from notify import view_notification as view_n

@use_master
@login_required
def view_notification(request):
    kwargs = {
        "user": request.session_user,         
    }
    ids = request.GET.getlist('id')
    if ids:
        kwargs["id__in"] = ids
    types = request.GET.getlist('notice_type')
    if types:
        kwargs["notice_type__in"] = types
    media = request.GET.getlist('media')
    if media:
        kwargs["media__in"] = media  
    view_n(**kwargs)
    return HttpResponseRedirect(request.GET.get('r') or '/')
