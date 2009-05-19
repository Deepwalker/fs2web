from django.db import models as m
from dialplan.models import Context

# Create your models here.
class FSDomain(m.Model):
    name = m.CharField(max_length=255)
    def __unicode__(self):
        return self.name


class FSUser(m.Model):
    "FreeSWITCH user"
    uid = m.CharField(max_length=255)
    password = m.CharField(max_length=255)
    accountcode = m.CharField(max_length=255)
    user_context = m.ForeignKey(Context)
    effective_caller_id_name = m.CharField(max_length=255)
    effective_caller_id_number = m.CharField(max_length=255)
    mailbox = m.CharField(max_length=255)
    mailbox_pwd = m.CharField(max_length=255)
    domain = m.ForeignKey(FSDomain)
    group = m.ForeignKey("FSGroup")
    def __unicode__(self):
        return self.uid + '/' + self.user_context.name

class Variable(m.Model):
    "Variable, in fact - type of variable"
    name = m.CharField(max_length=255)
    is_param = m.BooleanField()
    def __unicode__(self):
        return self.name+' ('+['var','param'][int(self.is_param)]+')'

class FSUVariable(m.Model):
    variable = m.ForeignKey(Variable)
    value = m.CharField(max_length=255)
    user = m.ForeignKey(FSUser)
    def __unicode__(self):
        return self.variable.name+' = '+self.value

class FSGroup(m.Model):
    "Group of FSUsers"
    name = m.CharField(max_length=255)
    users = m.ManyToManyField(FSUser,blank=True)
    domain = m.ForeignKey(FSDomain)
    def __unicode__(self):
        return self.name

TRANSPORT = (
    ("udp","udp"),
    ("tcp","tcp"),
)
class gateway(m.Model):
    "Gateway model"
    name = m.CharField(max_length=255)
    username = m.CharField(max_length=255)
    realm = m.CharField(max_length=255)
    from_user = m.CharField(max_length=255)
    from_domain = m.CharField(max_length=255)
    password = m.CharField(max_length=255)
    extension = m.CharField(max_length=255)
    proxy = m.CharField(max_length=255)
    register_proxy = m.CharField(max_length=255)
    expire_seconds = m.IntegerField()
    register = m.BooleanField()
    register_transport = m.CharField(max_length=4,choices=TRANSPORT)
    retry_seconds = m.IntegerField()
    caller_id_in_form = m.BooleanField()
    contact_params = m.CharField(max_length=255)
    ping = m.IntegerField()

    user = m.ForeignKey(FSUser,blank=True,null=True)
    domain = m.ForeignKey(FSDomain)
    def __unicode__(self):
        return self.name



