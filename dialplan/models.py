from django.db import models as m
from django.utils.translation import ugettext_lazy as _
#from users.models import PhoneNumber

# Create your models here.
class Context(m.Model):
    name = m.CharField(_(u"Name"),max_length=255)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _(u"Context")
        verbose_name_plural = _(u"Contexts")

class Extension(m.Model):
    name = m.CharField(_(u"Name"),max_length=255)
    continue_on = m.BooleanField(_(u"Continue on"))
    context = m.ForeignKey(Context)
    pref = m.IntegerField(_(u"Preference"))
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _(u"Extension")
        verbose_name_plural = _(u"Extensions")

BREAK = (
    ("on-false",_(u"on-false")),
    ("on-true",_(u"on-true")),
    ("always",_(u"always")),
    ("never",_(u"never")),
)

class Condition(m.Model):
    field = m.CharField(_(u"Field"),max_length=255)
    expression = m.CharField(_(u"Expression"),max_length=255)
    break_on = m.CharField(_(u"Break on"),max_length=10,choices=BREAK,default="on-false")
    extension = m.ForeignKey(Extension)
    pref = m.IntegerField(_(u"Preference"),)
    def __unicode__(self):
        return "%s === %s"%(self.field,self.expression)
    class Meta:
        ordering = ['pref']
        verbose_name = _(u"Condition")
        verbose_name_plural = _(u"Conditions")

class DPApp(m.Model):
    name = m.CharField(_(u"Name"),max_length=255)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _(u"Dialplan application")
        verbose_name_plural = _(u"Dialplan applications")

def get_dpapp(app):
    f = DPApp.objects.filter(name=app)
    if f:
        return f[0]
    else:
        new = DPApp(name=app)
        new.save()
        return new

class Action(m.Model):
    app = m.ForeignKey(DPApp)
    condition = m.ForeignKey(Condition)
    params = m.CharField(_(u"Name"),max_length=255)
    anti = m.BooleanField(_(u"Anti action"))
    pref = m.IntegerField(_(u"Preference"))
    def __unicode__(self):
        return "%s(%s)"%(self.app.name,self.params)
    class Meta:
        ordering = ['pref']
        verbose_name = _(u"Action")
        verbose_name_plural = _(u"Actions")

