from django.conf.urls.defaults import *
from django.views.generic import list_detail

#from users.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^user/', include('users.urls')),
    (r'^dialplan/', include('dialplan.urls')),

    (r'^confs/$','conference.views.list'),
    (r'^confs/(?P<cnf>[-.0-9a-zA-Z]+)/(?P<do>kick|mute|unmute)/(?P<id>\d+)/$','conference.views.list'),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^bin/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': 'bin/'}),

    # Uncomment the next line for to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
