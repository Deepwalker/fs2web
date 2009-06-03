from django.db import models as m
from django.conf import settings
from views import fsapi 

# Create your models here.

class Conference(m.Model):
    name = m.CharField("Name",max_length=254)
    number = m.IntegerField("Number",max_length=254)
    pin = m.IntegerField("Password",max_length=254,blank=True,null=True)
    participants = m.ManyToManyField("Phone")
    def start(self):
        participants = list(self.participants.all())
        if participants:
            for p in participants:
                print fsapi("bgapi","conference %s@default dial "%self.number + settings.DIALTEMPLATE%p.number)
    def __unicode__(self):
        return self.name

class Phone(m.Model):
    name = m.CharField("Name",max_length=254)
    number = m.IntegerField("Number",max_length=254)
    def __unicode__(self):
        return self.name
