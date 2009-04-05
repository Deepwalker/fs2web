from django.conf.urls.defaults import *
from django.views.generic import list_detail

from models import *

urlpatterns = patterns('',
    (r'view/(?P<object_id>\d+)/$',list_detail.object_detail,{'queryset':FSUser.objects.all()}),
    (r'edit/$','users.views.edit_user'),
    (r'edit/(?P<object_id>\d+)/$','users.views.edit_user'),
    (r'get/$','users.views.get_user_info'),
)

