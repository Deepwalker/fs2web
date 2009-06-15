from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$','conference.views.list'),
    (r'^(?P<cnf>[-.0-9a-zA-Z]+)/(?P<do>kick|mute|unmute|start)/(?P<id>\d+)/$','conference.views.list'),
    (r'^add/$','conference.views.add'),
    (r'^add/participants/(?P<object_id>\d+)/$','conference.views.add_partcipants'),
    (r'^delete/(?P<object_id>\d+)/$','conference.views.del_conf'),
)
