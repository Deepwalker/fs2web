from django.db import models as m
#from users.models import PhoneNumber

# Create your models here.
class Context(m.Model):
    name = m.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Extension(m.Model):
    name = m.CharField(max_length=255)
    continue_on = m.BooleanField()
    context = m.ForeignKey(Context)
    pref = m.IntegerField()
    def __unicode__(self):
        return self.name

BREAK = (
    ("on-false","on-false"),
    ("on-true","on-true"),
    ("always","always"),
    ("never","never"),
)

class Condition(m.Model):
    field = m.CharField(max_length=255)
    expression = m.CharField(max_length=255)
    break_on = m.CharField(max_length=10,choices=BREAK,default="on-false")
    extension = m.ForeignKey(Extension)
    pref = m.IntegerField()
    def __unicode__(self):
        return "%s === %s"%(self.field,self.expression)
    class Meta:
        ordering = ['pref']

class DPApp(m.Model):
    name = m.CharField(max_length=255)
    def __unicode__(self):
        return self.name

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
    params = m.CharField(max_length=255)
    anti = m.BooleanField()
    pref = m.IntegerField()
    def __unicode__(self):
        return "%s(%s)"%(self.app.name,self.params)
    class Meta:
        ordering = ['pref']

