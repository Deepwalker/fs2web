# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import *
from django.core import serializers
from django.utils import simplejson

def pyser(i,d={}):
    res = dict([(f.name,f.value_from_object(i)) for f in i._meta.fields])
    res.update(d)
    return res

def all_ser():
    return simplejson.dumps(
      [pyser(i,{'exts':
        [pyser(j,{'conditions':
            [pyser(k,{'actions':
                [pyser(a,{'app_name':a.app.name} ) for a in k.action_set.all()]}) 
                for k in j.condition_set.all()]}) 
            for j in i.extension_set.all()]}) 
        for i in Context.objects.all()])

def get_dialplan(request):
    if len(request.GET):
        data = request.GET
    else:
        data = request.POST
    context = get_object_or_404(Context,name=data.get('Hunt-Context'))
    return render_to_response('dialplan.xml',{'context':context,'data':request.POST})

def edit_dialplan(request):
    #print context
    #context = get_object_or_404(Context,name=context)
    #return render_to_response('dialplan.html',{'context':context,'data':all_ser()})
    return render_to_response('dialplan.html',{'data':all_ser()})

def save_obj(obj,Model):
    def udict2dict(udict,filter):
        return dict([(str(k),udict[k]) for k in udict if k in filter])

    # Action hook
    if Model==Action:
        obj['app']=get_dpapp(obj['app_name'])

    objid = obj['id']
    if objid!='': q = Model.objects.filter(id=int(objid))
    else: q=[]
    if q:
        inst=q[0]
        for f in obj:
            setattr(inst,f,obj[f])
        inst.save()
    else:
        del obj['id']
        filter = [i.name for i in Model._meta.fields]
        inst=Model(**udict2dict(obj,filter))
        inst.save()
    return inst

_dp_next=[Extension,'exts','context',[Condition,'conditions','extension',[Action,'actions','condition',[]]]]
def save_objs(objs,Model,prnt_f,parent,next=[]):
    ids=[]
    pref=10
    for obj in objs:
        if parent and prnt_f:
            obj.update({prnt_f:parent})
        obj['pref']=pref
        pref+=10
        new_obj = save_obj(obj,Model)
        ids.append(int(new_obj.id))
        if next:
            next_obj = obj[next[1]]
            save_objs(next_obj, next[0], next[2], new_obj, next[3])

    # Delete removed objs
    if prnt_f and prnt_f:
        db_ids = Model.objects.filter(**{prnt_f:parent})
    else: db_ids = Model.objects.all()
    db_ids = [i.id for i in db_ids]
    for_rm = list(set(db_ids)-set(ids))
    print ids, db_ids, for_rm
    for rm in for_rm:
        o = Model.objects.filter(**{prnt_f:parent,'id':rm})[0]
        print "Remove ",o
        o.delete()
    

def save_dialplan(request):
    if len(request.GET):
        data = request.GET
    else:
        data = request.POST
    print data['data']
    dp = simplejson.loads(data['data'])
    print dp
    save_objs(dp,Context,'',None,_dp_next)

    return HttpResponse('Saved')


