# Create your views here.
from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.forms.models import modelformset_factory, inlineformset_factory

def get_user_info(request):
    if len(request.GET):
        data = request.GET
    else:
        data = request.POST

    if data.get('action')=='group_call':
        return get_group(data)
    else:
        return get_user(data)

def get_user(data):
    user = get_object_or_404(FSUser,uid=data.get('user'),domain__name=data['domain'])
    return render_to_response('user.xml',{'user':user,'data':data})

def get_group(data):
    group = get_object_or_404(FSGroup,name=data.get('group'))
    return render_to_response('group.xml',{'group':group,'data':data})

def get_gates(data):
    gtws = get_object_or_404()
    return render_to_response('gateway.xml',{'gateways':gtws,'data':data})

# Edit
def edit_user(request,object_id=None):
    FSUserFormSet = modelformset_factory(FSUser)
    FSUVarFormSet = inlineformset_factory(FSUser,FSUVariable)
    if request.method == 'POST': # If the form has been submitted...
        form = FSUserFormSet(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            return HttpResponseRedirect('/users/get/%i/'%object_id) # Redirect after POST
    else:
        form = FSUserFormSet()
        form.var_forms = FSUVarFormSet()

    return render_to_response('users/fsuser_edit.html', {
        'form': form,
        'object_id':object_id,
    })

