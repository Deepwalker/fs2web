from xmlrpclib import ServerProxy
from django.conf import settings

def fsapi(*args,**kwargs):
    server = ServerProxy("http://freeswitch:works@127.0.0.1:8080")
    return server.freeswitch.api(*args,**kwargs)

def call_from_conference(conf,number,conf_cid=settings.CONFERENCE_CID):
    fsapi("bgapi","conference %s@default dial "%conf + settings.DIALTEMPLATE%number+" %s %s"%(conf_cid,number))

