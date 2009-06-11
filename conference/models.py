from django.db import models as m
from django.conf import settings
from fsapi import *

# Create your models here.

class Conference(m.Model):
    name = m.CharField("Name",max_length=254)
    number = m.CharField("Number",max_length=254)
    pin = m.IntegerField("Password",max_length=254,blank=True,null=True)
    participants = m.ManyToManyField("Phone")
    def start(self):
        participants = list(self.participants.filter(auto_call=True))
        if participants:
            for p in participants:
                call_from_conference(self.number,p.number)
    def __unicode__(self):
        return self.name

class Phone(m.Model):
    name = m.CharField("Name",max_length=254)
    number = m.IntegerField("Number",max_length=254)
    auto_call = m.BooleanField("Auto call",default=True)
    def caller_id_name(self):
        return self.name
    def caller_id_number(self):
        return self.number
    def member(self):
        return self
    def __unicode__(self):
        return "%s %s"%(self.name,self.number)
