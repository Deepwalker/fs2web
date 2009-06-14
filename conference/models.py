from django.db import models as m
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from fsapi import *

# Create your models here.

class Conference(m.Model):
    name = m.CharField(_(u"Name"),max_length=254)
    number = m.CharField(_(u"Number"),max_length=254)
    pin = m.IntegerField(_(u"Password"),max_length=254,blank=True,null=True)
    participants = m.ManyToManyField("Phone",verbose_name=_(u"Phone"))
    is_active = m.BooleanField(_(u"Is active?"),default=False,editable=False)
    def start(self):
        participants = list(self.participants.filter(auto_call=True))
        if participants:
            for p in participants:
                call_from_conference(self.number,p.number)
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
        return "%s (%s)"%(self.name,self.number)
    class Meta:
        verbose_name = _(u"Phone")
        verbose_name_plural = _(u"Phones")
