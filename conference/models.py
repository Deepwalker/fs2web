from django.db import models as m
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from fsapi import *

# Create your models here.

class Conference(m.Model):
    name = m.CharField(_(u"Name"),max_length=254,blank=False)
    number = m.CharField(_(u"Number"),max_length=254,blank=False)
    pin = m.IntegerField(_(u"Password"),max_length=254,blank=True,null=True)
    participants = m.ManyToManyField("Phone",verbose_name=_(u"Phone"),through='Participant')
    is_active = m.BooleanField(_(u"Is active?"),default=False,editable=False)
    def start(self):
        #participants = list(self.participants.filter(auto_call=True))
        # TODO: auto_call filter
        participants = self.participant_set.all()
        if participants:
            for p in participants:
                call_from_conference(self.number,p.phone.number,vars='participant=%s'%p.id)
    def participants_form(self):
        return AddParticipant(instance=self)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _(u"Conference")
        verbose_name_plural = _(u"Conferences")

class Phone(m.Model):
    name = m.CharField(_(u"Name"),max_length=254)
    number = m.IntegerField(_(u"Number"),max_length=254)
    auto_call = m.BooleanField(_(u"Auto call"),default=True)
    def caller_id_name(self):
        return self.name
    def caller_id_number(self):
        return self.number
    def member(self):
        return self
    def __unicode__(self):
        return "%s (%s)%s"%(self.name,self.number,"" if self.auto_call else "!")
    class Meta:
        verbose_name = _(u"Phone")
        verbose_name_plural = _(u"Phones")

class Participant(m.Model):
    conference = m.ForeignKey(Conference)
    phone = m.ForeignKey(Phone)
    active = m.BooleanField(_(u"Active"),default=False,editable=False)
    mute = m.BooleanField(_(u"Mute"),default=False,editable=False)
    talk = m.BooleanField(_(u"Talk"),default=False,editable=False)
    deaf = m.BooleanField(_(u"Deaf"),default=False,editable=False)

# Forms
class AddParticipant(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['participants']
    def save(self):
        print self.cleaned_data
        for p in self.cleaned_data['participants']:
            Participant.objects.get_or_create(conference=self.instance,phone=p)
        Participant.objects.filter(conference=self.instance).\
            exclude(phone__in=self.cleaned_data['participants']).delete()
        

class InviteParticipantForm(forms.Form):
    conference = forms.CharField(widget=forms.widgets.HiddenInput())
    phone = forms.CharField()

class AddConference(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name','number']
