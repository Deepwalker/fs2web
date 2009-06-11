from lxml import objectify as O
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from models import Conference
from fsapi import *
import syslog

class InviteParticipantFrom(forms.Form):
    conference = forms.CharField(widget=forms.widgets.HiddenInput())
    phone = forms.CharField()

def list(request,do="",id="",cnf="",param=""):
    r = O.fromstring(fsapi("conference","xml_list"))
    if do and id:
        fsapi("conference","%s %s %s"%(cnf,do,id))
        return HttpResponseRedirect('/confs/')

    if request.GET:
        form = InviteParticipantFrom(request.GET)
        if form.is_valid():
            conf = form.cleaned_data.get('conference')
            phone = form.cleaned_data.get('phone')
            call_from_conference(conf,phone)

    conferences = []
    if r.countchildren() > 0:
        for conf in r.conference:
            conf_name =conf.get('name') 
            conference = Conference.objects.filter(number=conf_name)
            members = dict([(str(m.number),m) for m in conference[0].participants.all()]) if conference else {}
            fs_members = [m for m in conf.members.member]
            for fm in fs_members:
                if str(fm.caller_id_name) in members:
                    fm.member = members[str(fm.caller_id_name)]
                    del members[str(fm.caller_id_name)]
                else:
                    fm.member = None
            fs_members.extend(members.values())
            conf_res = [conf_name, fs_members,InviteParticipantFrom({'conference':conf.get('name')}),
            conference[0] if conference else None] 
            conferences.append(conf_res)
    return render_to_response('confrences.html',{'confs':conferences})


