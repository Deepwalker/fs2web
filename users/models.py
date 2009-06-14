from django.db import models as m
from django.utils.translation import ugettext_lazy as _
from dialplan.models import Context

# Create your models here.
class FSDomain(m.Model):
    name = m.CharField(_(u"Name"),max_length=255)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _(u"Domain")
        verbose_name_plural = _(u"Domains")

class FSUser(m.Model):
    "FreeSWITCH user"
    uid = m.CharField(_(u"User number"),max_length=255)
    password = m.CharField(_(u"Password"),max_length=255)
    user_context = m.ForeignKey(Context,verbose_name=_(u"Context"))
    effective_caller_id_name = m.CharField(_(u"Caller name"),max_length=255)
    effective_caller_id_number = m.CharField(_(u"Caller number"),max_length=255)
    mailbox = m.CharField(_(u"Mailbox number"),max_length=255)
    mailbox_pwd = m.CharField(_(u"Mailbox password"),max_length=255)
    domain = m.ForeignKey(FSDomain,verbose_name=_(u"Domain"))
    group = m.ForeignKey("FSGroup",verbose_name=_(u"Group"))
    def __unicode__(self):
        return "%s (%s)"%(self.uid,self.user_context.name)
    class Meta:
        verbose_name = _(u"User")
        verbose_name_plural = _(u"Users")

class Variable(m.Model):
    "Variable, in fact - type of variable"
    name = m.CharField(_(u"Name"),max_length=255)
    is_param = m.BooleanField(_(u"Param?"))
    def __unicode__(self):
        return self.name+' ('+['var','param'][int(self.is_param)]+')'
    class Meta:
        verbose_name = _(u"Variable")
        verbose_name_plural = _(u"Variables")

class FSUVariable(m.Model):
    variable = m.ForeignKey(Variable,verbose_name=_(u"Variable"))
    value = m.CharField(_(u"Value"),max_length=255)
    user = m.ForeignKey(FSUser)
    def __unicode__(self):
        return self.variable.name+' = '+self.value
    class Meta:
        verbose_name = _(u"Variable")
        verbose_name_plural = _(u"Variables")

class FSGroup(m.Model):
    "Group of FSUsers"
    name = m.CharField(max_length=255)
    users = m.ManyToManyField(FSUser,blank=True)
    domain = m.ForeignKey(FSDomain)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _(u"Group")
        verbose_name_plural = _(u"Groups")

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



