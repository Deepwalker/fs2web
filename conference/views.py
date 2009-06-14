from lxml import objectify as O
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.views.generic import list_detail
from models import Conference
from fsapi import *

class InviteParticipantFrom(forms.Form):
    conference = forms.CharField(widget=forms.widgets.HiddenInput())
    phone = forms.CharField()

def list(request,do="",id="",cnf="",param=""):
    r = O.fromstring(fsapi("conference","xml_list"))
    if do=="start":
        conference = Conference.objects.get(id=int(cnf))
        conference.start()
        return HttpResponseRedirect('/confs/')

    if do and id:
        fsapi("conference","%s %s %s"%(cnf,do,id))
        return HttpResponseRedirect('/confs/')

    if request.GET:
        form = InviteParticipantFrom(request.GET)
        if form.is_valid():
            conf = form.cleaned_data.get('conference')
            phone = form.cleaned_data.get('phone')
            call_from_conference(conf,phone)
            return HttpResponseRedirect('/confs/')

    conferences = []
    active_confs=[]
    if r.countchildren() > 0:
        for conf in r.conference:
            conf_name =conf.get('name') 
            conference = Conference.objects.filter(number=conf_name)
            if conference:
                members = dict([(str(m.number),m) for m in conference[0].participants.all()])
                conference[0].is_active = True
                conference[0].save()
                active_confs.append(conference[0].id)
            else:
                members = {}
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
    Conference.objects.exclude(id__in=active_confs).update(is_active=False)
    return list_detail.object_list(request,queryset=Conference.objects.filter(is_active=False),
        template_name='confrences.html',extra_context={'confs':conferences})
    #return render_to_response('confrences.html',{'confs':conferences})


