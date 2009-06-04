from lxml import objectify as O
from xmlrpclib import ServerProxy
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
import syslog

class InviteParticipantFrom(forms.Form):
    conference = forms.CharField(widget=forms.widgets.HiddenInput())
    phone = forms.CharField()

def fsapi(*args,**kwargs):
    server = ServerProxy("http://freeswitch:works@127.0.0.1:8080")
    return server.freeswitch.api(*args,**kwargs)

def list(request,do=None,id=None,cnf=None):
    r = O.fromstring(fsapi("conference","xml_list"))
    if do and id:
        fsapi("conference","%s %s %s"%(cnf,do,id))
        return HttpResponseRedirect('/confs/')

    if request.method == 'POST':
        form = InviteParticipantFrom(request.POST)
        if form.is_valid():
            conf = form.cleaned_data.get('conference')
            phone = form.cleaned_data.get('phone')
            fsapi("bgapi","conference %s@default dial "%conf + settings.DIALTEMPLATE%phone)

    if r.countchildren() > 0:
        conferences = r.conference
        members = [[conf.get('name'),
            [m for m in conf.members.member],InviteParticipantFrom({'conference':conf.get('name')})] 
                for conf in conferences]
    else:
        members = []
    return render_to_response('confrences.html',{'confs':members})


