from xmlrpclib import ServerProxy
from django.conf import settings
#from django.views.decorators.cache import cache
import syslog

def fsapi(*args,**kwargs):
    #TODO caching 
    server = ServerProxy(settings.FS_CONNECT_STR)
    syslog.syslog(str(args)+"; "+str(kwargs))
    return server.freeswitch.api(*args,**kwargs)

def call_from_conference(conf,number,conf_cid=settings.CONFERENCE_CID,vars=''):
    #fsapi("bgapi","{%s}conference %s@default dial "%(vars,conf) + settings.DIALTEMPLATE%number+" %s %s"%(conf_cid,number))
    fsapi("bgapi","originate {%s}"%vars+settings.DIALTEMPLATE%number+" &conference(%s@default)"%conf)

