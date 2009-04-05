from django.conf.urls.defaults import *
from django.views.generic import list_detail

from models import *

urlpatterns = patterns('',
    (r'get/$','dialplan.views.get_dialplan'),
    (r'edit/$','dialplan.views.edit_dialplan'),
    (r'save/$','dialplan.views.save_dialplan'),
)

