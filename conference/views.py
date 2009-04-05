# Create your views here.
#import xml.etree.ElementTree as ET
from lxml import objectify as O
from xmlrpclib import ServerProxy
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect

def fsapi(*args,**kwargs):
    server = ServerProxy("http://freeswitch:works@127.0.0.1:8080")
    return server.freeswitch.api(*args,**kwargs)

def list(request,do=None,id=None,cnf=None):
    r = O.fromstring(fsapi("conference","xml_list"))
    if do and id:
        print do,id,cnf
        print 'FS:',fsapi("conference","%s %s %s"%(cnf,do,id))
        return HttpResponseRedirect('/confs/')

    if r.countchildren() > 0:
        conferences = r.conference
        members = [[conf.get('name'),
            [m for m in conf.members.member]] for conf in conferences]
    else:
        members = []
    return render_to_response('confrences.html',{'confs':members})


